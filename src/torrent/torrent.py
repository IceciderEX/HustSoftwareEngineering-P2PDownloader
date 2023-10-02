# @author 郑卯杨
# @date 2023/9/24
# @description 实现Torrent类,存储解析.torrent后的OrderedDict数据
from hashlib import sha1
from typing import List

from . import bencoding


class Torrent:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            meta_info = f.read()  # bytes
            self.meta_info = bencoding.Decode(meta_info).decode()  # OrderedDict
            info_hash = bencoding.Encode(self.meta_info[b'info']).encode()  # bytes
            self.info_hash: bytes = sha1(info_hash).digest()  # str size=20
            if b'files' in self.meta_info[b'info']:
                raise RuntimeError("Do not support multiple files now!")

    @property
    def announce(self) -> str:
        return self.meta_info[b'announce'].decode('utf-8')

    @property
    def length(self) -> int:
        return self.meta_info[b'info'][b'length']

    @property
    def pieces(self) -> List[bytes]:
        """
        :return: 列表的每一项是对应的piece使用sha1算法计算出的hash
        """
        res = []
        offset = 0
        data = self.meta_info[b'info'][b'pieces']
        while offset < len(data):
            res.append(data[offset:offset + 20])
            offset += 20
        return res

    @property
    def piece_length(self) -> int:
        return self.meta_info[b'info'][b'piece length']

    @property
    def name(self) -> str:
        return self.meta_info[b'info'][b'name'].decode('utf-8')
