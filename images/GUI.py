from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Image(object):
    @staticmethod
    def setupUi(Form, img):
        pixmap = QtGui.QPixmap(img)
        Form.setFixedSize(pixmap.size().width(), pixmap.size().height())
        Form.setWindowTitle(' ')
        Form.setWindowIcon(QtGui.QIcon(':/baseData/icon/main_litle.png'))
        Form.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        image = QtWidgets.QLabel(Form)
        image.setPixmap(pixmap)

        QtCore.QMetaObject.connectSlotsByName(Form)
