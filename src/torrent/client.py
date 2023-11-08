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
    封装了TorrentClient类,使用start()开始下载,stop()取消下载，pause()暂停下载，restart()继续下载
"""

MAX_PEER_CONNECTIONS = 516


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
        self.paused = False
        self.before_time = None
        self.before_bytes = None
        self.first_connect = True
        self.download_speed = 0.0
        self.download_Progress = 0.0

    def _empty_queue(self):
        while not self.available_peers.empty():
            self.available_peers.get_nowait()

    def stop(self):
        """
        取消下载
        :return:
        """
        self.abort = True
        logging.info(f'Download Canceled')
        for peer in self.peers:
            peer.stop()
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
        interval = 30 * 60  # Tracker服务器通信的默认间隔
        i = 1

        while True:
            if self.piece_manager.finished:
                logging.info('Torrent fully downloaded!')
                break
            if self.abort:
                logging.info('Aborting download...')
                break
            if self.paused:
                await asyncio.sleep(0.5)
                continue
            current = round(time.time())
            tracker_tasks = []
            responses = []
            try:
                for tracker in self.trackers:
                    if tracker.can_connect:
                    # if ((not tracker.previous) or (tracker.previous + interval < current)) and tracker.can_connect:
                        logging.info(f"向tracker服务器{tracker.announce}发送第{i}次请求")
                        i += 1
                        no_interval = True
                        task = asyncio.create_task(
                            asyncio.wait_for(
                                tracker.connect(
                                    first=previous if previous else False,
                                    uploaded=0,
                                    downloaded=self.piece_manager.bytes_downloaded
                                ),
                                timeout=8  # 设置tracker的最长相应时间为8s，超过不再连接
                            )
                        )
                        tracker_tasks.append(task)
                responses = await asyncio.gather(*tracker_tasks, return_exceptions=True)  # 等待所有的tracker返回response
            except (ConnectionError, TimeoutError):
                logging.info("Tracker unable to connect")

            try:
                index = 0
                for response in responses:
                    if response:
                        if isinstance(response, TimeoutError):  # 超时
                            logging.warning("A tracker request timed out.")
                        elif isinstance(response, Exception):  # 其他错误
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
            await asyncio.sleep(12)
        await self.stop()

    def update_download_speed(self):
        """
             返回当前的下载速度
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
        self.download_speed = show_speed

    async def return_download_time(self):
        while not self.piece_manager.finished:
            self.update_download_speed()
            await asyncio.sleep(1)
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

    def find_download_place(self, pah: str):
        """
        指定下载位置
        :return:无
        """
        self.piece_manager.download_place(pah)

    def pause(self):
        """
        暂停下载
        :return: 无
        """
        self.paused = True
        for peer in self.peers:
            peer.pause()
        logging.info(f'Download Paused')

    def restart(self):
        """
        继续下载
        :return: 无
        """
        self.paused = False
        for peer in self.peers:
            peer.restart()
        logging.info(f'Download Restarted')

    async def download_progress(self):
        """
        下载进度
        :return:
        """
        while not self.piece_manager.finished:
            self.download_Progress = self.piece_manager.download_progress()
            logging.info(f'下载进度：{self.download_Progress:.2f}')
            await asyncio.sleep(1)
        self.stop()

