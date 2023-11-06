# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'torrent.ui'
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

class Ui_torrent(object):
    def setupUi(self, torrent):
        if not torrent.objectName():
            torrent.setObjectName(u"torrent")
        torrent.resize(537, 413)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        torrent.setWindowIcon(icon)
        self.layoutWidget = QWidget(torrent)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 40, 483, 171))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(-1)

        self.verticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(torrent)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(70, 280, 399, 24))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)

        self.retranslateUi(torrent)

        QMetaObject.connectSlotsByName(torrent)
    # setupUi

    def retranslateUi(self, torrent):
        torrent.setWindowTitle(QCoreApplication.translate("torrent", u"torrent\u6587\u4ef6\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("torrent", u"Torrent\u6587\u4ef6\u9009\u62e9\u5668", None))
        self.pushButton.setText(QCoreApplication.translate("torrent", u"\u9009\u62e9.torrent\u6587\u4ef6", None))
    # retranslateUi

