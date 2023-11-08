import sys
import asyncio
import logging
import signal
from asyncio import CancelledError

from src.gui.mainwindow import Ui_MainWindow
from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

class TorrentFileSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Torrent 文件选择器")  # 设置窗口标题
        self.setGeometry(100, 100, 400, 200)  # 设置窗口位置和大小

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建选择.torrent文件按钮
        self.select_torrent_button = QPushButton("选择 .torrent 文件", self)
        self.select_torrent_button.clicked.connect(self.open_torrent_file_dialog)  # 连接按钮的点击事件到打开文件对话框函数
        layout.addWidget(self.select_torrent_button)

        self.central_widget.setLayout(layout)  # 将布局设置为中央窗口部件的布局

    def open_torrent_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Torrent Files (*.torrent)")  # 设置文件过滤器，只允许选择.torrent文件
        file_dialog.setViewMode(QFileDialog.List)
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "", "Torrent Files (*.torrent)")

        if torrent_file:
            logging.basicConfig(level=logging.INFO)
            loop = asyncio.get_event_loop()  # 获取事件循环
            client = TorrentClient(Torrent(torrent_file))  # 创建TorrentClient实例，传入选择的.torrent文件
            task = loop.create_task(client.start())  #创建异步任务以开始下载

            def signal_handler(*_):
                logging.info('Exiting, please wait until everything is shutdown...')
                client.stop()  # 响应信号，停止下载
                task.cancel()  # 取消异步任务

            signal.signal(signal.SIGINT, signal_handler)

            try:
                loop.run_until_complete(task)
            except CancelledError:
                logging.warning('Event loop was canceled')  # 如果事件循环被取消，记录警告信息
