# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MegnetLink_to_Torrent.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_magnetlink(object):
    def setupUi(self, magnetlink):
        if not magnetlink.objectName():
            magnetlink.setObjectName(u"magnetlink")
        magnetlink.resize(539, 382)
        self.gridLayout = QGridLayout(magnetlink)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_2 = QPushButton(magnetlink)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 4, 0, 1, 1)

        self.textBrowser = QTextBrowser(magnetlink)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 5, 0, 1, 1)

        self.pushButton = QPushButton(magnetlink)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        self.lineEdit = QLineEdit(magnetlink)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)

        self.label = QLabel(magnetlink)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.retranslateUi(magnetlink)

        QMetaObject.connectSlotsByName(magnetlink)
    # setupUi

    def retranslateUi(self, magnetlink):
        magnetlink.setWindowTitle(QCoreApplication.translate("magnetlink", u"Form", None))
        self.pushButton_2.setText(QCoreApplication.translate("magnetlink", u"\u786e\u8ba4\u8f6c\u6362", None))
        self.pushButton.setText(QCoreApplication.translate("magnetlink", u"\u9009\u62e9\u4e0b\u8f7d\u8def\u5f84", None))
#if QT_CONFIG(whatsthis)
        self.lineEdit.setWhatsThis(QCoreApplication.translate("magnetlink", u"\u8f93\u5165\u78c1\u529b\u94fe\u63a5", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("magnetlink", u"\u8f93\u5165\u78c1\u529b\u94fe\u63a5", None))
        self.label.setText(QCoreApplication.translate("magnetlink", u"\u78c1\u529b\u94fe\u63a5\u8f6ctorrent\u6587\u4ef6", None))
    # retranslateUi

