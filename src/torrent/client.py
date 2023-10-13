import asyncio
import logging
import time
from asyncio import Queue, sleep
from typing import List

from src.torrent.manager import PieceManager
from src.torrent.torrent import Torrent
from src.torrent.tracker import Tracker
from src.torrent.connection import Connection

"""
    @filename client.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块集成了所有模块,真正地开始下载
    封装了TorrentClient类,使用start()开始下载,stop()取消下载，pause()暂停下载，resume()继续下载
    做图形化界面时start()是开始接口，stop()为取消接口
"""

MAX_PEER_CONNECTIONS = 516


class TorrentClient:
    def __init__(self, torrent: Torrent):
        self.tracker = Tracker(torrent)
        self.available_peers = Queue()
        self.peers: List[Connection] = []
        self.piece_manager = PieceManager(torrent)
        self.abort = False
        self.before_time = None
        self.before_bytes = None

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
        interval = 1  # Tracker服务器通信的默认间隔
        i = 1
        while True:
            if self.piece_manager.finished:
                logging.info('Torrent fully downloaded!')
                break
            if self.abort:
                logging.info('Aborting download...')
                break
            current = round(time.time())
            # if (not previous) or (previous + interval < current) or self.available_peers.empty():
            if (not previous) or (previous + interval < current) or self.return_peers() < 0:
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

    def update_download_speed(self):
        """
             返回当前下载速度
        """
        now_time = time.time()
        now_bytes = self.piece_manager.block_download_bytes
        if self.before_time is None:
            self.before_time = now_time
            self.before_bytes = now_bytes
            return 0

        # 更新下载速度
        downloaded_bytes = now_bytes - self.before_bytes
        downloaded_time = now_time - self.before_time

        self.before_time = now_time
        self.before_bytes = now_bytes
        # 获取下载速度
        download_speed = 0
        if downloaded_time != 0:
            download_speed = downloaded_bytes / downloaded_time
        show_speed = download_speed / 1024
        if show_speed >= 1024:
            show_speed = show_speed / 1024
            logging.info(f'Download speed: {show_speed:.2f} MB/s')
            return show_speed
        else:
            logging.info(f'Download speed: {show_speed:.2f} KB/s')
            return show_speed

    async def return_download_time(self):
        while not self.piece_manager.finished:
            self.update_download_speed()
            await asyncio.sleep(3)
        self.stop()

    def return_peers(self):
        """
            返回仍然保持连接的peer个数
        """
        count = 0
        for peer in self.peers:
            if peer.alive:
                count += 1
        logging.info(f'Peers: {count}')
        return count

    def find_download_place(self, pah: str):
        """
        指定下载位置
        :return:
        """
        self.piece_manager.download_place(str)
    