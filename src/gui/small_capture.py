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
    def setupUi(self, small_capture):
        if not small_capture.objectName():
            small_capture.setObjectName(u"small_capture")
        small_capture.resize(215, 138)
        self.verticalLayout = QVBoxLayout(small_capture)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(small_capture)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(small_capture)

        QMetaObject.connectSlotsByName(small_capture)
    # setupUi

    def retranslateUi(self, small_capture):
        small_capture.setWindowTitle(QCoreApplication.translate("small_capture", u"Form", None))
        self.label.setText(QCoreApplication.translate("small_capture", u"TextLabel", None))
    # retranslateUi

