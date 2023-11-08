# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    # 设置界面的基本属性
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(524, 362)  # 设置窗口尺寸
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)  # 设置窗口图标
        self.verticalLayout = QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")  # 创建垂直布局

        # 创建标题标签
        self.label = QLabel(MainWindow)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(-1)

        self.verticalLayout.addWidget(self.label)  # 将标签添加到垂直布局中

        # 创建按钮，用于启动Torrent文件下载
        self.pushButton = QPushButton(MainWindow)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)  # 创建可切换状态的按钮，并初始化为未选中状态

        self.verticalLayout.addWidget(self.pushButton)

        # 创建按钮，用于打开M3U8视频播放器
        self.pushButton_m3u8 = QPushButton(MainWindow)
        self.pushButton_m3u8.setObjectName(u"pushButton_m3u8")

        self.verticalLayout.addWidget(self.pushButton_m3u8)

        # 创建按钮，用于启动网页抓取音视频
        self.pushButton_reptiles = QPushButton(MainWindow)
        self.pushButton_reptiles.setObjectName(u"pushButton_reptiles")

        self.verticalLayout.addWidget(self.pushButton_reptiles)

        # 创建按钮，用于打开音乐视频播放器
        self.pushButton_mp3 = QPushButton(MainWindow)
        self.pushButton_mp3.setObjectName(u"pushButton_mp3")

        self.verticalLayout.addWidget(self.pushButton_mp3)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"p2p", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"P2P\u4e0b\u8f7d\u5668", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Torrent\u6587\u4ef6\u4e0b\u8f7d", None))
        self.pushButton_m3u8.setText(QCoreApplication.translate("MainWindow", u"M3U8\u89c6\u9891\u64ad\u653e", None))
        self.pushButton_reptiles.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u9875\u6355\u83b7\u97f3\u89c6\u9891", None))
        self.pushButton_mp3.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u4e50\u89c6\u9891\u64ad\u653e\u5668", None))

