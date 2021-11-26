from PyQt5 import QtWidgets
from images.GUI import Ui_Image


class Scheme(QtWidgets.QDialog, Ui_Image):
    def __init__(self, info, parent=None):
        super(Scheme, self).__init__(parent)
        self.setupUi(self, info)
