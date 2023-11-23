<<<<<<< HEAD
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
    QSpacerItem, QVBoxLayout, QWidget)
=======
from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QGridLayout, QLabel, QProgressBar,
                               QPushButton)

>>>>>>> f380bd248a44e99d1dc87085ebda5125608c9d1f

class Ui_torrent(object):
    def setupUi(self, torrent):
        if not torrent.objectName():
            torrent.setObjectName(u"torrent")
<<<<<<< HEAD
        torrent.resize(400, 300)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        torrent.setWindowIcon(icon)
        self.layoutWidget = QWidget(torrent)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 20, 401, 171))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u5f69\u4e91"])
=======
        torrent.resize(537, 413)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        torrent.setWindowIcon(icon)
        self.gridLayout = QGridLayout(torrent)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(torrent)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
>>>>>>> f380bd248a44e99d1dc87085ebda5125608c9d1f
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(-1)

<<<<<<< HEAD
        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton = QPushButton(self.layoutWidget)
=======
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.pushButton_start = QPushButton(torrent)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.gridLayout.addWidget(self.pushButton_start, 5, 0, 1, 1)

        self.pushButton_restart = QPushButton(torrent)
        self.pushButton_restart.setObjectName(u"pushButton_restart")

        self.gridLayout.addWidget(self.pushButton_restart, 5, 1, 1, 1)

        self.pushButton_pause = QPushButton(torrent)
        self.pushButton_pause.setObjectName(u"pushButton_pause")

        self.gridLayout.addWidget(self.pushButton_pause, 6, 0, 1, 1)

        self.pushButton_stop = QPushButton(torrent)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout.addWidget(self.pushButton_stop, 6, 1, 1, 1)

        self.progressBar = QProgressBar(torrent)
        self.progressBar.setObjectName(u"progressBar")
        font1 = QFont()
        font1.setPointSize(12)
        self.progressBar.setFont(font1)
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 2)

        self.pushButton_path = QPushButton(torrent)
        self.pushButton_path.setObjectName(u"pushButton_path")

        self.gridLayout.addWidget(self.pushButton_path, 2, 0, 1, 2)

        self.pushButton = QPushButton(torrent)
>>>>>>> f380bd248a44e99d1dc87085ebda5125608c9d1f
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)

<<<<<<< HEAD
        self.verticalLayout.addWidget(self.pushButton)

=======
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 2)

        self.label_2 = QLabel(torrent)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 2)
>>>>>>> f380bd248a44e99d1dc87085ebda5125608c9d1f

        self.retranslateUi(torrent)

        QMetaObject.connectSlotsByName(torrent)
<<<<<<< HEAD
    # setupUi

    def retranslateUi(self, torrent):
        torrent.setWindowTitle(QCoreApplication.translate("torrent", u"torrent\u6587\u4ef6\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("torrent", u"torrent\u6587\u4ef6\u9009\u62e9\u5668", None))
        self.pushButton.setText(QCoreApplication.translate("torrent", u"\u9009\u62e9.torrent\u6587\u4ef6", None))
    # retranslateUi

=======

    def retranslateUi(self, torrent):
        torrent.setWindowTitle(QCoreApplication.translate("torrent", u"torrent\u6587\u4ef6\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("torrent", u"Torrent\u6587\u4ef6\u9009\u62e9\u5668", None))
        self.pushButton_start.setText(QCoreApplication.translate("torrent", u"\u5f00\u59cb", None))
        self.pushButton_restart.setText(QCoreApplication.translate("torrent", u"\u7ee7\u7eed", None))
        self.pushButton_pause.setText(QCoreApplication.translate("torrent", u"\u6682\u505c", None))
        self.pushButton_stop.setText(QCoreApplication.translate("torrent", u"\u53d6\u6d88", None))
        self.pushButton_path.setText(
            QCoreApplication.translate("torrent", u"\u9009\u62e9\u4e0b\u8f7d\u8def\u5f84", None))
        self.pushButton.setText(QCoreApplication.translate("torrent", u"\u9009\u62e9.torrent\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("torrent", u"TextLabel", None))
>>>>>>> f380bd248a44e99d1dc87085ebda5125608c9d1f
