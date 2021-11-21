from GUI import WinProgram
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()
        self._win = WinProgram()
        self._win.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec())
