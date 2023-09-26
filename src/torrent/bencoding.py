# @author 郑卯杨
# @date 2023/9/24
# @description 实现解码器和译码器
from collections import OrderedDict
from typing import Union

# Tokens

TOKEN_INTEGER = b'i'

TOKEN_STRING_SEPERATOR = b':'

TOKEN_LIST = b'l'

TOKEN_DICT = b'd'

TOKEN_END = b'e'


class Decode:
    """
        解码 bencode 格式的二进制数据
    """

    def __init__(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Argument 'data' must be of type bytes")
        self._data = data
        self._index = 0

    def decode(self):

        token = self._peek()
        if token is None:
            raise EOFError("Unexpected end of file")
        elif token == TOKEN_INTEGER:
            self._consume()
            return self._decode_int()
        elif token == TOKEN_LIST:
            self._consume()
            return self._decode_list()
        elif token == TOKEN_DICT:
            self._consume()
            return self._decode_dict()
        elif token == TOKEN_END:
            return None
        elif token in b'0123456789':
            return self._decode_str()
        else:
            raise RuntimeError(f"Invalid token read at {self._index}")

    def _peek(self) -> Union[bytes, None]:
        """
        返回当前位置的第一个字符
        :return 读完了就返回None,否则返回bytes
        """
        if len(self._data) > self._index:
            return self._data[self._index:self._index + 1]
        return None

    def _consume(self) -> None:
        self._index += 1

    def _read_until(self, token: bytes) -> bytes:
        try:
            occurence = self._data.index(token, self._index)
            result = self._data[self._index:occurence]
            self._index = occurence + 1
            return result
        except ValueError:
            raise RuntimeError("Unable to find token {0}".format(str(token)))

    def _read(self, length: int) -> bytes:
        if self._index + length > len(self._data):
            raise IndexError(f"Cannot read {length} bytes from current position {self._index}")
        result = self._data[self._index:self._index + length]
        self._index += length
        return result

    def _decode_int(self) -> int:
        return int(self._read_until(TOKEN_END))

    def _decode_str(self) -> bytes:
        length = int(self._read_until(TOKEN_STRING_SEPERATOR))
        return self._read(length)

    def _decode_list(self):
        res = []
        while self._peek() != TOKEN_END:
            res.append(self.decode())
        self._consume()
        return res

    def _decode_dict(self):
        res = OrderedDict()
        while self._peek() != TOKEN_END:
            key = self.decode()
            obj = self.decode()
            res[key] = obj
        self._consume()
        return res


class Encode:
    """
    编码为bencoding格式
    支持的python类型:
    int
    str
    list
    dict or ordered_dict
    """

    def __init__(self, data):
        self._data = data

    def encode(self) -> bytes:
        return self._encode_next(self._data)

    def _encode_next(self, data):
        if type(data) == str:
            return self._encode_str(data)
        elif type(data) == int:
            return self._encode_int(data)
        elif type(data) == bytes:
            return self._encode_bytes(data)
        elif type(data) == list:
            return self._encode_list(data)
        elif type(data) == dict or type(data) == OrderedDict:
            return self._encode_dict(data)
        else:
            return None

    def _encode_int(self, value: int):
        return str.encode('i' + str(value) + 'e', 'utf-8')

    def _encode_str(self, value: str):
        return str.encode(str(len(value)) + ':' + value, 'utf-8')

    def _encode_bytes(self, value: str):
        result = bytearray()
        result += str.encode(str(len(value)))
        result += b':'
        result += value
        return result

    def _encode_list(self, data):
        result = bytearray('l', 'utf-8')
        result += b''.join([self._encode_next(item) for item in data])
        result += b'e'
        return result

    def _encode_dict(self, data: dict) -> bytes:
        result = bytearray('d', 'utf-8')
        for k, v in data.items():
            key = self._encode_next(k)
            value = self._encode_next(v)
            if key and value:
                result += key
                result += value
            else:
                raise RuntimeError('Bad dict')
        result += b'e'
        return result
