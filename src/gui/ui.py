import sys
import os
import asyncio
import logging
import signal
from asyncio import CancelledError

from src.gui.Capture import Ui_Capture
from src.gui.small_capture import Ui_small_capture
from src.gui.mainwindow import Ui_MainWindow
from src.gui.torrent import Ui_torrent
from src.gui.m3u8 import Ui_m3u8
from src.gui.MegnetLink import Ui_magnetlink
from src.m3u8.m3u8 import jiekou
from src.movie.videoplayer import MainWindow
from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent
from src.torrent.manager import PieceManager
from src.videos_audios_capture.capture import capture
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtCore import QThread, Signal


class m3u8_ui(QWidget, Ui_m3u8):
    def __init__(self):
        super().__init__()
        self.ui = Ui_m3u8()
        self.ui.setupUi(self)
        self.ui.pushButton_path.clicked.connect(self.select_path)
        self.ui.pushButton.clicked.connect(self.start_m3u8)

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_m3u8(self):
        m3u8_url = self.ui.lineEdit_m3u8.text()
        path = self.ui.pushButton_path.text()
        name = self.ui.lineEdit_name.text()
        # print(m3u8_url)
        # print(path)
        # print(name)
        jiekou(m3u8_url, path, name)


class magnetlink_ui(QWidget, Ui_magnetlink):
    def __init__(self):
        super().__init__()
        self.ui = Ui_magnetlink()
        self.ui.setupUi(self)
        self.ui.pushButton_path.clicked.connect(self.select_path)
        self.ui.pushButton.clicked.connect(self.start_m3u8)

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_m3u8(self):
        m3u8_url = self.ui.lineEdit_m3u8.text()
        path = self.ui.pushButton_path.text()
        name = self.ui.lineEdit_name.text()
        # print(m3u8_url)
        # print(path)
        # print(name)
        jiekou(m3u8_url, path, name)


class small_capture_ui(QWidget, Ui_small_capture):
    def __init__(self):
        super().__init__()
        self.ui = Ui_small_capture()
        self.ui.setupUi(self)
        # self.ui.label.setText("下载失败")


class capture_ui(QWidget, Ui_Capture):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Capture()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_capture)
        self.ui.pushButton_path.clicked.connect(self.select_path)

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_capture(self):
        url = self.ui.lineEdit.text()
        path = self.ui.pushButton_path.text()
        # print(url)
        # print(path)
        capture(url, path)
        self.ui = small_capture_ui()
        self.ui.ui.label.setText("下载完成！")
        self.ui.show()
        # print("ok")


class torrent_tread_start(QThread):
    signal_speed = Signal(float)
    signal_progress = Signal(float)

    def __init__(self, file, path):
        super().__init__()
        self.file = file
        self.path = path

    async def speed(self, client):
        while not client.piece_manager.finished:
            self.signal_speed.emit(client.download_speed)
            await asyncio.sleep(1)
        client.stop()

    async def progress(self, client):
        while not client.piece_manager.finished:
            self.signal_progress.emit(client.download_Progress)
            await asyncio.sleep(1)
        client.stop()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TorrentClient(Torrent(self.file))
        client.find_download_place(self.path)
        task = loop.create_task(client.start())
        task2 = loop.create_task(client.return_download_time())
        task3 = loop.create_task(client.download_progress())
        task4 = loop.create_task(self.speed(client))
        task5 = loop.create_task(self.progress(client))

        def signal_handler(*_):
            logging.info('Exiting, please wait until everything is shutdown...')
            client.stop()
            task.cancel()

            signal.signal(signal.SIGINT, signal_handler)

        try:
            loop.run_until_complete(task)
            loop.run_until_complete(task2)
            loop.run_until_complete(task3)
            loop.run_until_complete(task4)
            loop.run_until_complete(task5)
        except CancelledError:
            logging.warning('Event loop was canceled')


class torrent_ui(QWidget, Ui_torrent):
    def __init__(self):
        super().__init__()
        self.ui = Ui_torrent()
        self.ui.setupUi(self)
        self.ui.label_2.setText("下载速度：")
        self.ui.pushButton.clicked.connect(self.open_torrent_file_dialog)
        self.ui.pushButton_path.clicked.connect(self.download_place)
        self.ui.pushButton_pause.clicked.connect(self.pause)
        self.ui.pushButton_restart.clicked.connect(self.restart)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)
        self.ui.progressBar.setValue(0)

    def open_torrent_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Torrent Files (*.torrent)")  # 设置文件过滤器，只允许选择.torrent文件
        file_dialog.setViewMode(QFileDialog.List)
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "", "Torrent Files (*.torrent)")
        self.ui.pushButton.setText(torrent_file)

        # if torrent_file:
        #     logging.basicConfig(level=logging.INFO)
        #     loop = asyncio.get_event_loop()
        #     client = TorrentClient(Torrent(torrent_file))
        #     task = loop.create_task(client.start())
        # #     task2 = loop.create_task(client.return_download_time())
        # #
        # #     def signal_handler(*_):
        # #         logging.info('Exiting, please wait until everything is shutdown...')
        # #         client.stop()
        # #         task.cancel()
        # #
        #     # signal.signal(signal.SIGINT, signal_handler)
        #
        #     # try:
        #     loop.run_until_complete(task)
        # #         loop.run_until_complete(task2)
        # #     except CancelledError:
        # #         logging.warning('Event loop was canceled')

    def download_place(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start(self):
        self.thread_ = torrent_tread_start(self.ui.pushButton.text(), self.ui.pushButton_path.text())
        self.thread_.signal_progress.connect(self.callback_progress)
        self.thread_.signal_speed.connect(self.callback_speed)
        self.thread_.start()
        # loop = asyncio.get_event_loop()
        # client = TorrentClient(Torrent(self.ui.pushButton.text()))
        # task = loop.create_task(client.start())
        # loop.run_until_complete(task)
        # progressBar_value = PieceManager.download_progress(self)
        # self.ui.progressBar.setValue(self, progressBar_value)

    def callback_progress(self, result):
        self.ui.progressBar.setValue(result)

    def callback_speed(self, result):
        self.ui.label_2.setText(f"下载速度：   {result:.2f} KB/S")

    def restart(self):
        client = TorrentClient(Torrent(self.ui.pushButton.text()))
        client.restart()

    def pause(self):
        client = TorrentClient(Torrent(self.ui.pushButton.text()))
        client.pause()

    def stop(self):
        client = TorrentClient(Torrent(self.ui.pushButton.text()))
        client.stop()


class main_ui(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.torrent_botton)
        self.ui.pushButton_mp3.clicked.connect(self.mp3_botton)
        self.ui.pushButton_reptiles.clicked.connect(self.capture_botton)
        self.ui.pushButton_m3u8.clicked.connect(self.m3u8_botton)

    def m3u8_botton(self):
        self.ui = m3u8_ui()
        self.ui.show()

    def torrent_botton(self):
        self.ui = torrent_ui()
        self.ui.show()

    def mp3_botton(self):
        self.ui = MainWindow()
        self.ui.show()

    def capture_botton(self):
        self.ui = capture_ui()
        self.ui.show()

    def magnetlink(self):
        self.ui = magnetlink_ui()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_ui()
    window.show()
    app.exec()
