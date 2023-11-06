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
from src.movie.test import MainWindow
from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent
from src.videos_audios_capture.capture import capture
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

class m3u8_ui(QWidget,Ui_m3u8):
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
        print(m3u8_url)
        print(path)
        print(name)
        jiekou(m3u8_url, path, name)

class small_capture_ui(QWidget,Ui_small_capture):
    def __init__(self):
        super().__init__()
        self.ui = Ui_small_capture()
        self.ui.setupUi(self)
        #self.ui.label.setText("下载失败")

class capture_ui(QWidget,Ui_Capture):
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
        print(url)
        print(path)
        capture(url, path)
            #self.ui = small_capture_ui()
            #self.ui.label.setText("ok")
            #self.ui.show()
        print("ok")


class torrent_ui(QWidget,Ui_torrent):
    def __init__(self):
        super().__init__()
        self.ui = Ui_torrent()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.open_torrent_file_dialog)

    def open_torrent_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Torrent Files (*.torrent)")  # 设置文件过滤器，只允许选择.torrent文件
        file_dialog.setViewMode(QFileDialog.List)
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "", "Torrent Files (*.torrent)")

        if torrent_file:
            logging.basicConfig(level=logging.INFO)
            loop = asyncio.get_event_loop()
            client = TorrentClient(Torrent(torrent_file))
            task = loop.create_task(client.start())
<<<<<<< HEAD
=======
            task2 = loop.create_task(client.return_download_time())
>>>>>>> origin/icecider_magnetlink

            def signal_handler(*_):
                logging.info('Exiting, please wait until everything is shutdown...')
                client.stop()
                task.cancel()

            signal.signal(signal.SIGINT, signal_handler)

            try:
                loop.run_until_complete(task)
<<<<<<< HEAD
=======
                loop.run_until_complete(task2)
>>>>>>> origin/icecider_magnetlink
            except CancelledError:
                logging.warning('Event loop was canceled')


class main_ui(QWidget,Ui_MainWindow):
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_ui()
    window.show()
<<<<<<< HEAD
    app.exec()




=======
    app.exec()
>>>>>>> origin/icecider_magnetlink
