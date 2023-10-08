# @author 郑卯杨
# @date 2023/9/27
# @description 实现结点之间的通信
import asyncio
from .manager import PieceManager
from .message import *
from asyncio import Queue, StreamReader, StreamWriter, CancelledError
from typing import Optional, Callable


class PeerStreamIterator:
    CHUNK_SIZE = 10 * 1024

    def __init__(self, reader: StreamReader, initial: bytes = None):
        self.reader = reader
        self.buffer = initial if initial else b''

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.reader.read(PeerStreamIterator.CHUNK_SIZE)
            if data:
                self.buffer += data
                message = self.parse()
                if message:
                    return message
            else:
                if self.buffer:
                    message = self.parse()
                    if message:
                        return message
                raise StopAsyncIteration()
        except ConnectionResetError:
            logging.debug('Connection closed by peer')
            raise StopAsyncIteration()
        except Exception:
            logging.exception("Error when iterating over stream!")
            raise StopAsyncIteration()

    def parse(self):
        header_length = 4
        if len(self.buffer) == 4:
            return KeepAlive()
        if len(self.buffer) > 4:
            message_length = struct.unpack('>I', self.buffer[:4])[0]
            if len(self.buffer) >= message_length:
                def _consume():
                    self.buffer = self.buffer[header_length + message_length:]

                def _data():
                    return self.buffer[:header_length + message_length]

                msg_id = struct.unpack('>b', self.buffer[4:5])[0]
                match msg_id:
                    case MsgId.Choke:
                        _consume()
                        return Choke()
                    case MsgId.Unchoke:
                        _consume()
                        return UnChoke()
                    case MsgId.Interested:
                        _consume()
                        return Interested()
                    case MsgId.NotInterested:
                        _consume()
                        return NotInterested()
                    case MsgId.Bitfield:
                        data = _data()
                        _consume()
                        return BitField.decode(data)
                    case MsgId.Have:
                        data = _data()
                        _consume()
                        return Have.decode(data)
                    case MsgId.Request:
                        data = _data()
                        _consume()
                        return Request.decode(data)
                    case MsgId.Piece:
                        data = _data()
                        _consume()
                        return Piece.decode(data)
                    case MsgId.Cancel:
                        data = _data()
                        _consume()
                        return Cancel.decode(data)
                    case _:
                        logging.info("decode unknown message")
            else:
                logging.debug('Not enough in buffer in order to parse')
        return None


class ProtocolError(BaseException):
    pass


STOPPED = "stopped"
CHOKED = "Choked"
INTERESTED = "Interested"
PENDING = 'pending_request'


class Connection:
    def __init__(self, queue: Queue, info_hash: bytes,
                 peer_id: bytes, piece_manager: PieceManager,
                 on_block_cb: Optional[Callable] = None):
        self.my_state = []
        self.peer_state = []
        self.queue = queue
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.remote_id: Optional[bytes] = None
        self.writer: Optional[StreamWriter] = None
        self.reader: Optional[StreamReader] = None
        self.piece_manager = piece_manager
        self.on_block_cb = on_block_cb
        self.future = asyncio.ensure_future(self._start())

    async def _handshake(self) -> bytes:
        """
        发送并解析handshake消息
        """
        self.writer.write(HandShake(self.info_hash, self.peer_id).encode())
        await self.writer.drain()

        buf = b''
        tries = 1
        while len(buf) < HandShake.length and tries < 10:
            # 只要成功读取一个handshake就会跳出循环
            tries += 1
            buf = await self.reader.read(PeerStreamIterator.CHUNK_SIZE)

        response = HandShake.decode(buf[:HandShake.length])
        if not response:
            raise ProtocolError("Unable to receive and parse a handshake")
        if response.info_hash != self.info_hash:
            raise ProtocolError("Handshake with invalid info_hash")

        self.remote_id = response.peer_id
        logging.info("Handshake with peer was successful")
        return buf[HandShake.length:]

    async def _send_interested(self) -> None:
        message = Interested()
        logging.info(f"Sending message: {message}")
        self.writer.write(message.encode())
        await self.writer.drain()

    async def _next_request(self):
        block = self.piece_manager.next_request(self.remote_id)
        if block:
            message = Request(block.piece, block.offset, block.length)

            logging.info(f'Requesting block {block.offset / REQUEST_SIZE} for piece {block.piece} '
                         f'of {block.length} bytes from peer {self.remote_id}')
            self.writer.write(message.encode())
            await self.writer.drain()

    def stop(self):
        self.my_state.append(STOPPED)
        if not self.future.done():
            self.future.cancel()

    def cancel(self):
        logging.info(f"Closing peer {self.remote_id}")
        if not self.future.done():
            self.future.cancel()
        if self.writer:
            self.writer.close()
        self.queue.task_done()

    async def _start(self):
        while STOPPED not in self.my_state:
            ip, port = await self.queue.get()
            logging.info(f"Got assigned peer with {ip}:{port}")
            try:
                self.reader, self.writer = await asyncio.open_connection(ip, port)
                logging.info(f"Connecting to peer {ip}")
                buffer = await self._handshake()
                self.my_state.append(CHOKED)
                await self._send_interested()
                self.my_state.append(INTERESTED)
                async for message in PeerStreamIterator(self.reader, buffer):
                    if STOPPED in self.my_state:
                        break
                    if type(message) is BitField:
                        self.piece_manager.add_peer(self.remote_id, message.bitfield)
                    elif type(message) is Interested:
                        self.peer_state.append(INTERESTED)
                    elif type(message) is NotInterested:
                        if INTERESTED in self.peer_state:
                            self.peer_state.remove(INTERESTED)
                    elif type(message) is Choke:
                        self.my_state.append(CHOKED)
                    elif type(message) is UnChoke:
                        if CHOKED in self.my_state:
                            self.my_state.remove(CHOKED)
                    elif type(message) is Have:
                        self.piece_manager.update_peer(self.remote_id, message.index)
                    elif type(message) is KeepAlive:
                        pass
                    elif type(message) is Piece:
                        self.my_state.remove(PENDING)
                        self.on_block_cb(
                            peer_id=self.remote_id,
                            piece_index=message.index,
                            block_offset=message.begin,
                            data=message.block)
                    elif type(message) is Request:
                        logging.info('Ignoring the received Request message.')
                    elif type(message) is Cancel:
                        logging.info('Ignoring the received Cancel message.')

                    if CHOKED not in self.my_state:
                        if INTERESTED in self.my_state:
                            if PENDING not in self.my_state:
                                self.my_state.append(PENDING)
                                await self._next_request()

            except ProtocolError:
                logging.exception("protocol error")
            except (ConnectionRefusedError, TimeoutError):
                logging.warning('Unable to connect to peer')
            except (ConnectionResetError, CancelledError):
                logging.warning('Connection closed')
            except Exception:
                logging.exception('An error occurred')
                self.cancel()
                # raise e
            self.cancel()
