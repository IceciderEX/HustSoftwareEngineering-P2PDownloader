# @author 郑卯杨
# @date 2023/10/2
# @description 实现了TorrentClient类
import asyncio
import logging
import time
from asyncio import Queue
from typing import List

import aiohttp

from src.torrent.manager import PieceManager
from src.torrent.torrent import Torrent
from src.torrent.tracker import Tracker
from src.torrent.connection import Connection

MAX_PEER_CONNECTIONS = 40


class DownloadSpeedTracker:
    def __init__(self):
        self.start_time = time.time()
        self.downloaded_data = 0

    def update_downloaded_data(self, data_size):
        self.downloaded_data = data_size

    def get_download_speed(self):
        current_time = time.time()
        time.sleep(3.0)
        elapsed_time = 3

        if elapsed_time > 0:
            download_speed = self.downloaded_data / elapsed_time  # 下载速度，单位为字节/秒
            return download_speed

        return 0  # 若时间间隔为0，则速度为0


class TorrentClient:
    def __init__(self, torrent: Torrent):
        self.tracker = Tracker(torrent)
        self.available_peers = Queue()
        self.peers: List[Connection] = []
        self.piece_manager = PieceManager(torrent)
        self.abort = False
        self.download_speed_tracker = DownloadSpeedTracker()
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
        Start downloading the torrent held by this client.

        This results in connecting to the tracker to retrieve the list of
        peers to communicate with. Once the torrent is fully downloaded or
        if the download is aborted this method will complete.
        """
        self.peers = [Connection(self.available_peers,
                                 self.tracker.torrent.info_hash,
                                 self.tracker.peer_id,
                                 self.piece_manager,
                                 self._on_block_retrieved)
                      for _ in range(MAX_PEER_CONNECTIONS)]

        previous = None  # 上一次announce call的时间
        interval = 2 * 10  # announce call 默认间隔

        while True:
            now_time = time.time()
            now_bytes = self.piece_manager.bytes_downloaded
            self.update_download_speed(now_time, now_bytes)
            if self.piece_manager.finished:
                logging.info('Torrent fully downloaded!')
                break
            if self.abort:
                logging.info('Aborting download...')
                break

            current = time.time()
            if (not previous) or (previous + interval < current):
                response = None
                try:
                    response = await self.tracker.connect(
                        first=previous if previous else False,
                        uploaded=0,
                        downloaded=self.piece_manager.bytes_downloaded)
                except ConnectionRefusedError:
                    logging.info("Tracker refused connection")
                except aiohttp.ClientConnectorError:
                    logging.info("Tracker refused connection")

                if response:
                    previous = current
                    interval = response.interval
                    self._empty_queue()
                    for peer in response.peers:
                        self.available_peers.put_nowait(peer)

            else:
                await asyncio.sleep(5)
        self.stop()

    def update_download_speed(self, now_time, now_bytes):
        if self.before_time is None:
            self.before_time = now_time
            self.before_bytes = now_bytes
            return 0
        # 更新下载速度
        downloaded_bytes = now_bytes - self.before_bytes
        downloaded_time = now_time - self.before_time
        # self.download_speed_tracker.update_downloaded_data(downloaded_bytes)

        # 获取下载速度
        download_speed = downloaded_bytes / downloaded_time
        logging.info(f'Download speed: {download_speed / 1024:.2f} KB/s')
