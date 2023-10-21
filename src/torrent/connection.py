import asyncio
import logging

from src.torrent.manager import PieceManager
from src.torrent.message import *
from asyncio import Queue, StreamReader, StreamWriter, CancelledError
from typing import Optional, Callable

"""
    @filename connection.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0

    该模块负责和结点的通信
    实现了和Peer通信的最小单元Connection,能够不断地获取等待中的Peer并与之通信
    实现了异步流迭代器PeerStreamIterator,方便解析数据
    实现了自定义异常ProtocolError
"""


class PeerStreamIterator:
    """
    接受与Peer通信时回传的信息,并根据信息的类型封装成不同的Message类,返回给上一级调用
    """
    CHUNK_SIZE = 10 * 1024

    def __init__(self, reader: StreamReader, initial: bytes = None):
        self.reader = reader
        self.buffer = initial if initial else b''

    def __aiter__(self):
        return self

    async def __anext__(self):
        """
        :return: Message
        :raise: ConnectionResetError: Connection closed by peer
        :raise: TimeoutError: Time out
        :raise: StopAsyncIteration: stop iteration
        """
        while True:
            try:
                data = await asyncio.wait_for(self.reader.read(PeerStreamIterator.CHUNK_SIZE), timeout=10)
                if data:
                    self.buffer += data
                    message = self.parse()
                    if message:
                        return message
                else:
                    logging.debug('No data read from stream')
                    if self.buffer:
                        message = self.parse()
                        if message:
                            return message
                    raise StopAsyncIteration()
            except ConnectionResetError:
                logging.debug('Connection closed by peer')
                raise StopAsyncIteration()
            except CancelledError:
                raise StopAsyncIteration()
            except StopAsyncIteration as e:
                raise e
            except TimeoutError:
                raise TimeoutError()
            except Exception:
                logging.exception('Error when iterating over stream!')
                raise StopAsyncIteration()
        # raise StopAsyncIteration()

    def parse(self):
        """
        :return: 根据Peer回传的信息解码并封装成不同的Message类
        """

        header_length = 4

        if len(self.buffer) > 4:
            message_length = struct.unpack('>I', self.buffer[:4])[0]
            if message_length == 0:
                return KeepAlive()
            if len(self.buffer) >= message_length:
                def _consume():
                    self.buffer = self.buffer[header_length + message_length:]

                def _data():
                    return self.buffer[:header_length + message_length]

                msg_id = struct.unpack('>b', self.buffer[4:5])[0]
                if msg_id == MsgId.Choke:
                    _consume()
                    return Choke()
                elif msg_id == MsgId.Unchoke:
                    _consume()
                    return UnChoke()
                elif msg_id == MsgId.Interested:
                    _consume()
                    return Interested()
                elif msg_id == MsgId.NotInterested:
                    _consume()
                    return NotInterested()
                elif msg_id == MsgId.Bitfield:
                    data = _data()
                    _consume()
                    return BitField.decode(data)
                elif msg_id == MsgId.Have:
                    data = _data()
                    _consume()
                    return Have.decode(data)
                elif msg_id == MsgId.Request:
                    data = _data()
                    _consume()
                    return Request.decode(data)
                elif msg_id == MsgId.Piece:
                    data = _data()
                    _consume()
                    return Piece.decode(data)
                elif msg_id == MsgId.Cancel:
                    data = _data()
                    _consume()
                    return Cancel.decode(data)
                else:
                    logging.info("decode unknown message")
            else:
                logging.debug('Not enough in buffer in order to parse')
        return None


class ProtocolError(BaseException):
    pass


STOPPED = "stopped"
CHOKED = "choked"
INTERESTED = "interested"
PENDING = 'pending_request'
PAUSED = "paused"

TIME_OUT = 12


class Connection:
    """
    Connection是执行通信任务的最小单元,通过封装为协程来实现任务队列的自动管理调用
    """
    PAUSE_TIME = 3600  # 一小时

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
        self.on_block_cb = on_block_cb  # 接收到Block数据时的回调函数
        self.future = asyncio.ensure_future(self._start())  # 协程任务
        self.alive = False
        self.pause_event = asyncio.Event()

    async def _handshake(self) -> bytes:
        """发送并解析handshake消息

        :return: data[HandShake.length:]
        :raise: ProtocolError: invalid handshake
        """
        self.writer.write(HandShake(self.info_hash, self.peer_id).encode())
        await self.writer.drain()

        buf = b''
        tries = 1
        while len(buf) < HandShake.length and tries < 30:
            # 接受返回的handshake，只要成功读取一个handshake就会跳出循环
            tries += 1
            buf = await self.reader.read(PeerStreamIterator.CHUNK_SIZE)

        response = HandShake.decode(buf[:HandShake.length])
        if not response:
            raise ProtocolError("Unable to receive and parse a handshake")
        if response.info_hash != self.info_hash:
            raise ProtocolError("Handshake with invalid info_hash")

        self.remote_id = response.peer_id
        logging.debug(f"Handshake with peer was successful")
        return buf[HandShake.length:]

    async def _send_interested(self) -> None:
        """
        :return: 向Peer发送Interested信息
        """
        message = Interested()
        logging.debug(f"Sending message: {message}")
        self.writer.write(message.encode())
        await self.writer.drain()

    async def _next_request(self):
        """
        :return: 获取下一个需要请求的块并向Peer发送请求
        """
        block = self.piece_manager.next_request(self.remote_id)
        if block:
            message = Request(block.piece, block.offset, block.length)

            logging.debug(f'Requesting block {block.offset / REQUEST_SIZE} for piece {block.piece} '
                          f'of {block.length} bytes from peer {self.remote_id}')
            self.writer.write(message.encode())
            await self.writer.drain()
            logging.debug(f"gain block {block.offset / REQUEST_SIZE} for piece {block.piece} successfully")

    def stop(self):
        """
        停止
        """
        self.my_state.append(STOPPED)
        self.alive = False
        if not self.future.done():
            self.future.cancel()

    async def cancel(self):
        """
        cancel 等待所有资源被释放完
        """
        logging.info(f"Closing peer {self.remote_id}")
        self.alive = False
        if not self.future.done():
            self.future.cancel()
            try:
                await self.future
            except asyncio.CancelledError:
                pass
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.queue.task_done()

    async def _start(self):
        """实现和Peer的通信,交流,数据传输,数据解析

        :raise: (ConnectionRefusedError, TimeoutError):Unable to connect to peer
        :raise: (ConnectionResetError, CancelledError):Connection closed
        :raise: RuntimeError:A runtime error occured
        :raise Exception:An unknown error occurred
        """

        while STOPPED not in self.my_state:
            ip, port = await self.queue.get()
            if ip == '255.255.255.255':  # 广播IP
                continue
            logging.info(f"Got assigned peer with {ip}:{port}")
            try:
                # self.reader, self.writer = await asyncio.open_connection(ip, port)
                self.reader, self.writer = await asyncio.wait_for(asyncio.open_connection(ip, port),
                                                                  timeout=TIME_OUT)  # 设置最大等待时间为5s
                logging.info(f"Connecting to peer {ip}:{port}")
                buffer = await asyncio.wait_for(self._handshake(), timeout=TIME_OUT)
                self.my_state.append(CHOKED)
                await asyncio.wait_for(self._send_interested(), timeout=TIME_OUT)
                self.my_state.append(INTERESTED)
                self.alive = True
                async for message in PeerStreamIterator(self.reader, buffer):
                    if STOPPED in self.my_state:
                        break
                    if PAUSED in self.my_state:
                        await self.pause_event.wait()  # 暂停时等待暂停事件
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
                                await asyncio.wait_for(self._next_request(), timeout=TIME_OUT)

            except ProtocolError:
                logging.exception("protocol error")
            except (ConnectionRefusedError, TimeoutError):
                logging.warning('Unable to connect to peer')
            except (ConnectionResetError, CancelledError):
                logging.warning('Connection closed')
            except RuntimeError:
                logging.warning("A runtime error occured")
            except OSError:
                logging.warning("指定的网络名格式无效/信号灯超时")
            except Exception:
                logging.exception('An unknown error occurred')
                # await self.cancel()
                # raise e
            await self.cancel()

    def pause(self):
        self.my_state.append(PAUSED)
        self.pause_event.clear()

    def restart(self):
        if PAUSED in self.my_state:
            self.my_state.remove(PAUSED)
            self.pause_event.set()
