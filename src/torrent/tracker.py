# @author 郑卯杨
# @date 2023/9/25
# @description 实现了和tracker服务器通信的Tracker类,以及封装了response信息的TrackerResponse
import logging
import random
import re
import socket
import struct
import urllib.parse
from struct import unpack

import aiohttp
import asyncudp

from . import bencoding
from .torrent import Torrent


def _decode_port(port):
    """
    按照网络大端存储模式解析无符号短整型
    """
    return unpack(">H", port)[0]


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
    def peers(self):
        """
        紧凑模式下peers是一个二进制字节串,每个peer 6字节
        4字节ip,2字节端口
        """

        peers = self.response[b'peers']
        if type(peers) == list:
            logging.debug('Dictionary model peers are returned by tracker')
            raise NotImplementedError()
        else:
            logging.debug('Binary model peers are returned by tracker')

            peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
            return [(socket.inet_ntoa(p[:4]), _decode_port(p[4:]))
                    for p in peers]


def _calculate_peer_id():
    return '-PC0223-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])


class Tracker:
    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = _calculate_peer_id()  # urlen编码的 20 字节字符串
        self.http_client = aiohttp.ClientSession()
        self.use_udp = self.torrent.announce.startswith("udp")

    async def connect(self, first: bool = False, downloaded: int = 0, uploaded: int = 0):
        # param type = int float str
        params = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': [x for x in range(6881, 6890)][random.randint(0, 8)],
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': self.torrent.length - downloaded,
            'compact': 1
        }
        print(self.torrent.announce)
        print(self.torrent.announce.startswith("udp"))

        if first:
            params['event'] = 'started'
        if self.use_udp:
            match = re.search(r'udp://([^:/]+:\d+)/', self.torrent.announce)
            if match:
                tracker_address = match.group(1)
                print(tracker_address)
                print(tracker_address.split(":"))
                remote_ip, remote_port = tracker_address.split(":")
                remote_port = int(remote_port)
                print(remote_ip, remote_port)
                print(type(remote_ip))
                print(type(remote_port))
            else:
                raise ConnectionError('Unable to connect to tracker')
            connect_request = struct.pack('>QII', 0x41727101980, 0, 99)
            sock = await asyncudp.create_socket(remote_addr=(remote_ip, remote_port))
            sock.sendto(connect_request)
            datagram, remote_addr = await sock.recvfrom()

            # print(bencoding.Decode(data).decode())
        else:
            url = self.torrent.announce + "?" + urllib.parse.urlencode(params)
            logging.info('Connecting to tracker at: ' + url)
            async with self.http_client.get(url) as resp:
                if not resp.status == 200:
                    raise ConnectionError('Unable to connect to tracker')
                data = await resp.read()  # bencoded dictionary
                return TrackerResponse(bencoding.Decode(data).decode())

    def close(self):
        if not self.use_udp:
            self.http_client.close()
