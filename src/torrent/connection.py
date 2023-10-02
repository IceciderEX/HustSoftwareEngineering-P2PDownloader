# @author 郑卯杨
# @date 2023/9/27
# @description 实现结点之间的通信
import struct
from .message import *


class PeerStreamIterator:
    CHUNK_SIZE = 10 * 1024

    def __init__(self, reader, initial: bytes = None):
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


class Connection:
    pass
