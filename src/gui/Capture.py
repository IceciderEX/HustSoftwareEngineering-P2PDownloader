# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Capture.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Capture(object):
    def setupUi(self, Capture):
        if not Capture.objectName():
            Capture.setObjectName(u"Capture")
        Capture.resize(351, 261)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Capture.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Capture)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(Capture)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
<<<<<<< HEAD
        font.setFamilies([u"\u534e\u6587\u7ec6\u9ed1"])
=======
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
>>>>>>> origin/icecider_magnetlink
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setIndent(-1)

        self.verticalLayout.addWidget(self.label_2)

        self.label = QLabel(Capture)
        self.label.setObjectName(u"label")
        font1 = QFont()
<<<<<<< HEAD
        font1.setFamilies([u"\u7b49\u7ebf"])
=======
        font1.setFamilies([u"\u534e\u6587\u6977\u4f53"])
>>>>>>> origin/icecider_magnetlink
        font1.setPointSize(12)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Capture)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit)

        self.label_3 = QLabel(Capture)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)

        self.pushButton_path = QPushButton(Capture)
        self.pushButton_path.setObjectName(u"pushButton_path")

        self.verticalLayout.addWidget(self.pushButton_path)

        self.pushButton = QPushButton(Capture)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.retranslateUi(Capture)

        QMetaObject.connectSlotsByName(Capture)
    # setupUi

    def retranslateUi(self, Capture):
        Capture.setWindowTitle(QCoreApplication.translate("Capture", u"Capture", None))
        self.label_2.setText(QCoreApplication.translate("Capture", u"\u7f51\u9875\u6355\u83b7\u97f3\u89c6\u9891", None))
        self.label.setText(QCoreApplication.translate("Capture", u"\u7f51\u5740\uff1a", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Capture", u"\u8bf7\u8f93\u5165\u60f3\u8981\u6355\u83b7\u7684\u7f51\u5740", None))
        self.label_3.setText(QCoreApplication.translate("Capture", u"\u4e0b\u8f7d\u5730\u5740\uff1a", None))
        self.pushButton_path.setText(QCoreApplication.translate("Capture", u"\u9009\u62e9\u4e0b\u8f7d\u5730\u5740", None))
        self.pushButton.setText(QCoreApplication.translate("Capture", u"\u5f00\u59cb\u6355\u83b7", None))
    # retranslateUi

