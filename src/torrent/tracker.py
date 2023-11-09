import logging
import random
import re
import socket
import struct
import urllib.parse
import aiohttp
import asyncudp
from aiohttp import ClientSession
from asyncudp import Socket
from typing import Optional
from src.torrent import bencoding
from src.torrent.torrent import Torrent

"""
    @filename tracker.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块实现了和Tracker服务器的通信,目前支持http协议和udp协议
    实现了封装类Tracker,和Tracker服务器通信
    实现了封装类TrackerResponse,通过peers属性访问peers的 (ip,port)
"""


def _decode_port(port):
    """
    按照网络大端存储模式解析无符号短整型
    """
    return struct.unpack(">H", port)[0]


class TrackerResponse:
    def __init__(self, response):
        self.response = response

    @property
    def failure(self):
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self) -> int:
        """
        可选参数,客户端在向跟踪器发送常规请求之间应等待的时间间隔（以秒为单位）
        """
        return self.response.get(b'interval', 0)

    @property
    def complete(self) -> int:
        """
        可选参数,有多少个完整的结点
        """
        return self.response.get(b'complete', 0)

    @property
    def incomplete(self) -> int:
        """
        可选参数,有多少个不完整的结点
        """
        return self.response.get(b'incomplete', 0)

    @property
    def peers(self) -> []:
        """
         :return: 返回一个列表,列表中的每一项是peer的信息 (ip,port)
        """
        peers = self.response[b'peers']
        if type(peers) == list:
            logging.debug('Dictionary model peers are returned by tracker')
            raise NotImplementedError()
        else:
            logging.debug('Binary model peers are returned by tracker')
            # TODO 返回解析后的peers信息(紧凑模式)
            pass


def _calculate_peer_id():
    return '-PC0223-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])


class Tracker:
    def __init__(self, torrent: Torrent):
        """
        :param torrent: Torrent类的实例
        """
        self.torrent = torrent
        self.peer_id = _calculate_peer_id()  # urlen编码的 20 字节字符串
        self.http_client: Optional[ClientSession] = None

    async def connect(self, first: bool = False, downloaded: int = 0, uploaded: int = 0) -> TrackerResponse:
        """根据announce的类型来决定是使用http协议还是udp协议

        :param first: 是否是第一次下载
        :param downloaded: 已经下载的字节数
        :param uploaded:  上传的字节数
        :return: TrackerResponse: 对通信结果的封装
        :raise: ConnectionError: Unable to connect to tracker
        """
        if self.http_client is None:
            self.http_client = aiohttp.ClientSession()
        # TODO 填充params,使代码能与 Tracker正常通信
        params = {}
        url = self.torrent.announce + "?" + urllib.parse.urlencode(params)
        logging.info('Connecting to tracker at: ' + url)
        async with self.http_client.get(url) as resp:
            if not resp.status == 200:
                raise ConnectionError('Unable to connect to tracker')
            data = await resp.read()  # bencoded dictionary
            return TrackerResponse(bencoding.Decode(data).decode())

    async def close(self) -> None:
        """
        关闭掉异步资源
        """
        await self.http_client.close()
