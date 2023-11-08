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
    # 创建一个用于处理M3U8的界面
    def __init__(self):
        super().__init__()
        self.ui = Ui_m3u8()
        self.ui.setupUi(self)
        self.ui.pushButton_path.clicked.connect(self.select_path)
        self.ui.pushButton.clicked.connect(self.start_m3u8)

    def select_path(self):
        # 打开文件对话框以选择保存路径
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_m3u8(self):
        # 获取输入的M3U8 URL、保存路径和名称，然后启动下载
        m3u8_url = self.ui.lineEdit_m3u8.text()
        path = self.ui.pushButton_path.text()
        name = self.ui.lineEdit_name.text()
        # print(m3u8_url)
        # print(path)
        # print(name)
        jiekou(m3u8_url, path, name)


class small_capture_ui(QWidget, Ui_small_capture):
    # 创建一个小型捕获完成界面
    def __init__(self):
        super().__init__()
        self.ui = Ui_small_capture()
        self.ui.setupUi(self)
        self.ui.label.setText("下载完成！")


class capture_ui(QWidget, Ui_Capture):
    # 创建一个用于视频捕获的界面
    def __init__(self):
        super().__init__()
        self.ui = Ui_Capture()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_capture)
        self.ui.pushButton_path.clicked.connect(self.select_path)

    def select_path(self):
        # 打开文件对话框以选择保存路径
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_capture(self):
        url = self.ui.lineEdit.text()
        path = self.ui.pushButton_path.text()
        # 调用捕获函数并传入URL和路径，开始下载
        # print(url)
        # print(path)
        capture(url, path)
        self.ui = small_capture_ui()
        self.ui.ui.label.setText("下载完成！")
        self.ui.show()
        # print("ok")


class torrent_tread_start(QThread):
    # 创建一个用于处理种子下载的线程
    signal_speed = Signal(float)
    signal_progress = Signal(float)
    signal_done = Signal(bool)

    def __init__(self, file, path):
        super().__init__()
        self.file = file
        self.path = path
        # 创建TorrentClient并传入Torrent文件
        self.client = TorrentClient(Torrent(self.file))

    async def speed(self, client):
        while not client.piece_manager.finished:
            # 发射下载速度信号
            self.signal_speed.emit(client.download_speed)
            await asyncio.sleep(1)
        client.stop()

    async def progress(self, client):
        while not client.piece_manager.finished:
            # 发射下载速度信号
            self.signal_progress.emit(client.download_Progress)
            await asyncio.sleep(1)
        client.stop()

    def restart_(self):
        # 重新开始下载
        self.client.restart()

    def pause_(self):
        # 暂停下载
        self.client.pause()

    def stop_(self):
        #停止下载
        self.client.stop()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # 查找下载位置
        # self.client = TorrentClient(Torrent(self.file))
        self.client.find_download_place(self.path)
        # 创建异步任务
        task = loop.create_task(self.client.start())
        task2 = loop.create_task(self.client.return_download_time())
        task3 = loop.create_task(self.client.download_progress())
        task4 = loop.create_task(self.speed(self.client))
        task5 = loop.create_task(self.progress(self.client))

        def signal_handler(*_):
            logging.info('Exiting, please wait until everything is shutdown...')
            self.client.stop()
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
        done_window = small_capture_ui()
        done_window.show()
        self.signal_progress.emit(100)


class torrent_ui(QWidget, Ui_torrent):
    # 创建一个用于处理种子下载的界面
    def __init__(self):
        super().__init__()
        self.thread_ = None
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
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "",
                                                      "Torrent Files (*.torrent)")
        self.ui.pushButton.setText(torrent_file)

    def download_place(self):
        # 打开文件对话框以选择保存路径
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start(self):
        self.thread_ = torrent_tread_start(self.ui.pushButton.text(), self.ui.pushButton_path.text())
        self.thread_.signal_progress.connect(self.callback_progress)
        self.thread_.signal_speed.connect(self.callback_speed)
        self.thread_.start()

    def callback_progress(self, result):
        # 更新下载进度条
        self.ui.progressBar.setValue(result)

    def callback_speed(self, result):
        # 更新下载速度标签
        self.ui.label_2.setText(f"下载速度：   {result:.2f} KB/S")

    def restart(self):
        # 重新开始下载
        self.thread_.restart_()

    def pause(self):
        # 暂停下载
        self.thread_.pause_()

    def stop(self):
        # 停止下载并关闭界面
        self.thread_.stop_()
        self.close()


class main_ui(QWidget, Ui_MainWindow):
    # 创建主界面
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

#主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_ui()
    window.show()
    app.exec()
