import logging
from hashlib import sha1
from typing import List

from src.torrent import bencoding

"""
    @filename torrent.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块对解析bencoding格式二进制文件后生成的OrderedDict进行了封装
    实现了封装类Torrent,通过torrent的属性访问
"""


class Torrent:
    def __init__(self, filepath: str):
        """
        :param filepath: 需要解析的.torrent文件路径
        :raise RuntimeError: 如果该torrent文件是多文件下载模式,抛出异常，停止本次下载
        """
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            meta_info = f.read()  # bytes
            # OrderedDict，包括announce, announce-list, info(name, length, piece length, pieces)...
            self.meta_info = bencoding.Decode(meta_info).decode()

            # 由info进行bencode.encode得到infohash(bytes)
            info_hash = bencoding.Encode(self.meta_info[b'info']).encode()
            # 再由sha1加密算法得到infohash(string)
            self.info_hash: bytes = sha1(info_hash).digest()  # str size = 20
            self.info_bytes = info_hash
            if b'files' in self.meta_info[b'info']:
                raise RuntimeError("Do not support multiple files now!")
            logging.info(f"announce={self.meta_info[b'announce'].decode('utf-8')}")

    @property
    def announce(self) -> str:
        """
        :return: 返回Tracker服务器的announce
        """
        return self.meta_info[b'announce'].decode('utf-8')

    @property
    def length(self) -> int:
        """
        :return: 返回 下载文件的总大小
        """
        return self.meta_info[b'info'][b'length']

    @property
    def pieces(self) -> List[bytes]:
        """
        :return: 返回一个列表,列表的每一项是对应的piece使用sha1算法计算出的hash值
        """
        res = []
        offset = 0
        data = self.meta_info[b'info'][b'pieces']
        length = len(data)
        while offset < length:
            res.append(data[offset:offset + 20])
            offset += 20
        return res

    @property
    def piece_length(self) -> int:
        """
        :return: 返回每一个piece的length
        """
        return self.meta_info[b'info'][b'piece length']

    @property
    def name(self) -> str:
        """
        :return: 返回要下载的文件的名字
        """
        return self.meta_info[b'info'][b'name'].decode('utf-8')
