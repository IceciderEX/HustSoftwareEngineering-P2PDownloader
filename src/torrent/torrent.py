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
            self.meta_info = bencoding.Decode(
                meta_info).decode()  # OrderedDict
            info_hash = bencoding.Encode(
                self.meta_info[b'info']).encode()  # bytes
            self.info_hash: bytes = sha1(info_hash).digest()  # str size=20
            if b'files' in self.meta_info[b'info']:
                raise RuntimeError("Do not support multiple files now!")
            logging.info(
                f"announce={self.meta_info[b'announce'].decode('utf-8')}")

    @property
    def announce(self) -> str:
        """
        :return: 返回Tracker服务器的announce
        """
        # TODO
        pass

    @property
    def length(self) -> int:
        """
        :return: 返回 下载文件的总大小
        """
        # TODO
        pass

    @property
    def pieces(self) -> List[bytes]:
        """
        :return: 返回一个列表,列表的每一项是对应的piece使用sha1算法计算出的hash值
        """
        # TODO
        pass

    @property
    def piece_length(self) -> int:
        """
        :return: 返回每一个piece的length
        """
        # TODO
        pass

    @property
    def name(self) -> str:
        """
        :return: 返回要下载的文件的名字
        """
        # TODO
        pass
