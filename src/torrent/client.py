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
    封装了TorrentClient类,使用start()开始下载,stop()停止下载
"""

MAX_PEER_CONNECTIONS = 5160


class TorrentClient:
    def __init__(self, torrent: Torrent):
        self.trackers = []
        for tracker in torrent.trackers:
            self.trackers.append(Tracker(torrent, tracker))
        self.tracker = Tracker(torrent, torrent.announce)
        self.available_peers = Queue()
        self.peers: List[Connection] = []
        self.piece_manager = PieceManager(torrent)
        self.abort = False
        self.before_time = None
        self.before_bytes = None
        self.first_connect = True

    def _empty_queue(self):
        while not self.available_peers.empty():
            self.available_peers.get_nowait()

    def stop(self):
        self.abort = True
        for peer in self.peers:
            peer.stop()
        self.piece_manager.close()
        for tracker in self.trackers:
            tracker.close()

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
        first_connect = True

        while True:
            if self.piece_manager.finished:
                logging.info('Torrent fully downloaded!')
                break
            if self.abort:
                logging.info('Aborting download...')
                break

            current = round(time.time())

            # List to store tasks for each tracker request
            tracker_tasks = []

            # Iterate through each tracker and create a task for each request
            responses = []

            try:
                for tracker in self.trackers:
                    if tracker.can_connect:
                    # if ((not tracker.previous) or (tracker.previous + interval < current)) and tracker.can_connect:
                        logging.info(f"向tracker服务器{tracker.announce}发送第{i}次请求")
                        i += 1
                        no_interval = True
                        # Create a task for each tracker request
                        task = asyncio.create_task(
                            asyncio.wait_for(
                                tracker.connect(
                                    first=previous if previous else False,
                                    uploaded=0,
                                    downloaded=self.piece_manager.bytes_downloaded
                                ),
                                timeout=5 # Timeout set to 5 seconds
                            )
                        )
                        tracker_tasks.append(task)

                    # if not no_interval:
                    #     logging.info("client sleep 5s")
                    #     await asyncio.sleep(5)

                    # Wait for all tracker requests to complete concurrently
                responses = await asyncio.gather(*tracker_tasks, return_exceptions=True)
            except (ConnectionError, TimeoutError):
                logging.info("UDP unable to connect")

            # Wait for all tracker requests to complete concurrently
            try:
                index = 0
                for response in responses:
                    if response:
                        if isinstance(response, TimeoutError):
                            # Handle TimeoutError, e.g., log the error
                            logging.warning("A tracker request timed out.")
                        elif isinstance(response, Exception):
                            # Handle other exceptions, e.g., log the error
                            logging.error(f"An error occurred in a tracker request: {response}")
                        else:
                            tracker = self.trackers[index]
                            tracker.previous = current
                            interval = response.interval
                            self._empty_queue()
                            for peer in response.peers:
                                self.available_peers.put_nowait(peer)
                        index += 1
            except ConnectionError:
                logging.info("UDP unable to connect")
            await asyncio.sleep(7)
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
        logging.info(f'Peers: {self.return_peers()}')
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
        return count
