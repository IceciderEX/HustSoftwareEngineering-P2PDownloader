import asyncio
import logging
import time
from asyncio import Queue
from typing import List

from src.torrent.manager import PieceManager
from src.torrent.torrent import Torrent
from src.torrent.tracker import Tracker
from src.torrent.connection import Connection

"""
    @filename client.py
    @date 2023/10/10
    @version 1.0
    
    该模块集成了所有模块,真正地开始下载
    封装了TorrentClient类,使用start()开始下载,stop()停止下载
"""

MAX_PEER_CONNECTIONS = 40


class TorrentClient:
    def __init__(self, torrent: Torrent):
        self.tracker = Tracker(torrent)
        self.available_peers = Queue()
        self.peers: List[Connection] = []
        self.piece_manager = PieceManager(torrent)
        self.abort = False

    def _empty_queue(self):
        while not self.available_peers.empty():
            self.available_peers.get_nowait()

    def stop(self):
        self.abort = True
        for peer in self.peers:
            peer.stop()
        self.piece_manager.close()
        self.tracker.close()

    def _on_block_retrieved(self, peer_id: bytes, piece_index: int, block_offset: int, data: bytes):
        self.piece_manager.block_received(peer_id, piece_index, block_offset, data)

    async def start(self):
        """
        开始下载持有的torrent文件

        当文件被全部下载或中止时停止
        """
        self.peers = [Connection(self.available_peers,
                                 self.tracker.torrent.info_hash,
                                 self.tracker.peer_id,
                                 self.piece_manager,
                                 self._on_block_retrieved)
                      for _ in range(MAX_PEER_CONNECTIONS)]

        previous = None
        interval = 2 * 60  # Tracker服务器通信的默认间隔
        i = 0
        while True:
            if self.piece_manager.finished:
                logging.info('Torrent fully downloaded!')
                break
            if self.abort:
                logging.info('Aborting download...')
                break

            current = round(time.time())
            if (not previous) or (previous + interval < current) or self.available_peers.empty():
                logging.info(f"向tracker服务器发送第{i}次请求")
                i += 1
                response = await self.tracker.connect(
                    first=previous if previous else False,
                    uploaded=0,
                    downloaded=self.piece_manager.bytes_downloaded)

                if response:
                    previous = current
                    interval = response.interval
                    self._empty_queue()
                    for peer in response.peers:
                        self.available_peers.put_nowait(peer)
            else:
                logging.info("client sleep 5s")
                await asyncio.sleep(5)
        self.stop()
