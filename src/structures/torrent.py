# @author 郑卯杨
# @date 2023/9/24
# @description 实现Torrent类，解码.torrent文件并返回相关信息
from hashlib import sha1
from typing import List
import bencodepy


class Torrent:
    def __init__(self, filepath):
        self.filepath = filepath
        with (open(filepath, 'rb') as f):
            meta_info = f.read()  # bytes read from file
            self.meta_info = bencodepy.decode(meta_info)  # OrderedDict
            info_dict = bencodepy.encode(self.meta_info[b'info'])  # bytes

            self.info_hash: bytes = sha1(info_dict).digest()  # info_dict's sha1 bytes
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