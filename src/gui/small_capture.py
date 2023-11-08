# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'small_capture.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_small_capture(object):
    # 设置界面的基本属性
    def setupUi(self, small_capture):
        if not small_capture.objectName():
            small_capture.setObjectName(u"small_capture")
        small_capture.resize(154, 96)

        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        small_capture.setWindowIcon(icon)  # 设置窗口图标

        self.verticalLayout = QVBoxLayout(small_capture)
        self.verticalLayout.setObjectName(u"verticalLayout")  # 创建垂直布局

        # 创建标签，用于显示文本内容
        self.label = QLabel(small_capture)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        self.label.setFont(font)  # 设置标签的字体和大小
        self.label.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐

        self.verticalLayout.addWidget(self.label)  # 将标签添加到垂直布局中

        self.retranslateUi(small_capture)  # 设置UI元素的文本内容

        QMetaObject.connectSlotsByName(small_capture)  # 连接信号和槽

    def retranslateUi(self, small_capture):
        small_capture.setWindowTitle(QCoreApplication.translate("small_capture", u"reptiles", None))
        self.label.setText(QCoreApplication.translate("small_capture", u"TextLabel", None))

