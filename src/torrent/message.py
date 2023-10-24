import logging
import struct
import bitstring

"""
    @filename message.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块实现了通信要用到的所有信息类
    每一个信息类都包含:
        类成员函数encode: 编码为bytes类型
        静态函数decode: 解码bytes类型,并返回一个对应类
"""


class MsgId:
    """
    枚举类,定义了通信状态
    """
    Choke = 0
    Unchoke = 1
    Interested = 2
    NotInterested = 3
    Have = 4
    Bitfield = 5
    Request = 6
    Piece = 7
    Cancel = 8


class Message:
    """
    所有通信消息的基类,
    类成员函数encode: 编码为 bytes类型
    静态函数decode 解码bytes类型,并返回一个cls
    """

    def encode(self) -> bytes:
        pass

    @classmethod
    def decode(cls, data: bytes):
        pass


class HandShake(Message):
    length = 49 + 19

    def __init__(self, info_hash: bytes, peer_id: bytes):
        if isinstance(info_hash, str):
            info_hash = info_hash.encode('utf-8')
        if isinstance(peer_id, str):
            peer_id = peer_id.encode('utf-8')
        self.info_hash = info_hash
        self.peer_id = peer_id

    def encode(self):
        return struct.pack('>B19s8x20s20s',
                           19, b'BitTorrent protocol', self.info_hash, self.peer_id)

    @classmethod
    def decode(cls, data: bytes):
        length = 49 + 19
        if len(data) != length:
            logging.error(f"HandShake Decode: data length {len(data)}")
            raise RuntimeError(f"HandShake Decode receive wrong data, len:{len(data)}")

        unpack_data = struct.unpack('>B19s8x20s20s', data)
        return HandShake(unpack_data[2], unpack_data[3])


class KeepAlive:
    pass


class Choke(Message):

    def encode(self):
        return struct.pack('>Ib',
                           1, MsgId.Choke)


class UnChoke(Message):

    def encode(self):
        return struct.pack('>Ib', 1, MsgId.Unchoke)


class Interested(Message):

    def encode(self):
        return struct.pack('>Ib', 1, MsgId.Interested)

    def __str__(self):
        return "Interested"


class NotInterested(Message):

    def encode(self):
        return struct.pack('>Ib', 1, MsgId.NotInterested)


class Have(Message):
    def __init__(self, index) -> None:
        self.index = index

    def encode(self):
        return struct.pack('>IbI', 5, MsgId.Have, self.index)

    @classmethod
    def decode(cls, data: bytes):
        unpack_data = struct.unpack('>IbI', data)
        return Have(unpack_data[-1])


class BitField(Message):
    def __init__(self, bitfield):
        self.bitfield = bitstring.BitArray(bytes=bitfield)

    def encode(self) -> bytes:
        return struct.pack(f'>Ib{len(self.bitfield)}s',
                           1 + len(self.bitfield), MsgId.Bitfield, self.bitfield)

    @classmethod
    def decode(cls, data: bytes):
        length = struct.unpack('>I', data[:4])[0]
        bitfield = struct.unpack(f'>{length - 1}s', data[5:])[0]
        return BitField(bitfield)


REQUEST_SIZE = 2 ** 14


class Request(Message):
    """
    Request是向Peer请求块信息的类
    """

    def __init__(self, index: int, begin: int, length: int = REQUEST_SIZE):
        self.index = index
        self.begin = begin
        self.length = length

    def encode(self):
        return struct.pack('>IbIII',
                           13,
                           MsgId.Request,
                           self.index,
                           self.begin,
                           self.length)

    @classmethod
    def decode(cls, data: bytes):
        unpack_data = struct.unpack('>IbIII', data)
        return Request(unpack_data[2], unpack_data[3], unpack_data[4])


class Piece(Message):
    length = 9

    def __init__(self, index: int, begin: int, block: bytes):
        self.index = index
        self.begin = begin
        self.block = block

    def encode(self):
        message_length = Piece.length + len(self.block)
        return struct.pack(f'>IbII{len(self.block)}s',
                           message_length,
                           MsgId.Piece,
                           self.index,
                           self.begin,
                           self.block)

    @classmethod
    def decode(cls, data: bytes):
        length = struct.unpack('>I', data[:4])[0]
        unpack_data = struct.unpack(f'>IbII{length - Piece.length}s',
                                    data[:length + 4])
        return Piece(unpack_data[2], unpack_data[3], unpack_data[4])

    def __str__(self):
        return 'Piece'


class Cancel(Message):
    """
    Message format:
         <len=0013><id=8><index><begin><length>
    """

    def __init__(self, index, begin, length: int = REQUEST_SIZE):
        self.index = index
        self.begin = begin
        self.length = length

    def encode(self):
        return struct.pack('>IbIII',
                           13,
                           MsgId.Cancel,
                           self.index,
                           self.begin,
                           self.length)

    @classmethod
    def decode(cls, data: bytes):
        unpack_data = struct.unpack('>IbIII', data)
        return Cancel(unpack_data[2], unpack_data[3], unpack_data[4])
