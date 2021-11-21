from GUI import WinProgram
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()
        self._win = WinProgram()
        self._win.setupUi(self)
        self.show()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Down:
            self.focusNextPrevChild(True)
        elif e.key() == Qt.Key_Up:
            self.focusNextPrevChild(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec())
