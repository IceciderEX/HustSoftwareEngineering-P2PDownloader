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

            peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
            return [(socket.inet_ntoa(p[:4]), _decode_port(p[4:]))
                    for p in peers]


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
        self.sock: Optional[Socket] = None
        self.use_udp = self.torrent.announce.startswith("udp")

    async def connect(self, first: bool = False, downloaded: int = 0, uploaded: int = 0) -> TrackerResponse:
        """根据announce的类型来决定是使用http协议还是udp协议

        :param first: 是否是第一次下载
        :param downloaded: 已经下载的字节数
        :param uploaded:  上传的字节数
        :return: TrackerResponse: 对通信结果的封装
        :raise: ConnectionError: Unable to connect to tracker
        """
        if self.use_udp:
            match = re.search(r'udp://([^:/]+:\d+)/', self.torrent.announce)
            if match:
                tracker_address = match.group(1)
                remote_ip, remote_port = tracker_address.split(":")
                remote_port = int(remote_port)
                print(remote_ip, remote_port)
            else:
                raise ConnectionError('Unable to connect to udp tracker')
            if self.sock is None:
                self.sock = await asyncudp.create_socket(remote_addr=(remote_ip, remote_port))
            connect_request = struct.pack('>QII', 0x41727101980, 0, 99)
            print("send udp connect request")
            self.sock.sendto(connect_request)
            datagram, remote_addr = await self.sock.recvfrom()
            print(datagram)
            action, transaction_id, connection_id = struct.unpack('>IIQ', datagram)
            if not action == 0 and not transaction_id == 99:
                raise ConnectionError('Unable to connect to tracker')
            announce_request = struct.pack(
                '>QII20s20sQQQIIIiH',
                connection_id,  # Connection ID
                1,  # Action (Announce请求)
                99,  # Transaction ID
                self.torrent.info_hash,  # Info hash
                self.peer_id.encode('utf-8'),  # Peer ID
                0,  # Downloaded
                0,  # Left
                0,  # Uploaded
                1 if first else 0,  # Event (0表示无事件,1 started)
                0,  # IP address (0表示默认)
                0,  # key
                -1,  # num want -1 default
                random.randint(1023, 8888)  # Port
            )
            # print("announce request")
            self.sock.sendto(announce_request)
            datagram, remote_addr = await self.sock.recvfrom()
            # print(len(datagram))
            try:
                action, transaction_id, interval, leechers, seeders = struct.unpack('>IIIII', datagram[:20])
                # print(f"{action=},{transaction_id=},{interval=},{leechers=},{seeders=}")
                dict_data = {b"action": action, b"transaction_id": transaction_id, b"interval": interval,
                             b"leechers": leechers,
                             b"seeders": seeders, b"peers": datagram[20:]}
                print(len(datagram[20:]))
                return TrackerResponse(dict_data)
            except Exception as e:
                raise ConnectionError('Unable to connect to tracker')
        else:
            if self.http_client is None:
                self.http_client = aiohttp.ClientSession()
            params = {
                'info_hash': self.torrent.info_hash,
                'peer_id': self.peer_id,
                # 'port': [x for x in range(6881, 6890)][random.randint(0, 8)],
                'port': 5552,
                'uploaded': uploaded,
                'downloaded': downloaded,
                'left': self.torrent.length - downloaded,
                'compact': 1
            }
            if first:
                params['event'] = 'started'
            url = self.torrent.announce + "?" + urllib.parse.urlencode(params)
            logging.info('Connecting to tracker at: ' + url)
            async with self.http_client.get(url) as resp:
                if not resp.status == 200:
                    raise ConnectionError('Unable to connect to tracker')
                data = await resp.read()  # bencoded dictionary
                return TrackerResponse(bencoding.Decode(data).decode())

    def close(self) -> None:
        """
        关闭掉异步资源
        """
        if self.use_udp:
            self.sock.close()
        else:
            self.http_client.close()
