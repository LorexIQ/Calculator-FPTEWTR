from PyQt5 import QtWidgets
from guide.GUI import Ui_Guide


class Guide(QtWidgets.QDialog, Ui_Guide):
    def __init__(self, info, parent=None):
        super(Guide, self).__init__(parent)
        self.setupUi(self, info)
