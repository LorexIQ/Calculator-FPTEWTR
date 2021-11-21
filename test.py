from GUI import Ui_MainWindow
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import sys

class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()
        self.win = Ui_MainWindow()
        self.win.setupUi(self)
        self.win._centralwidget.setGeometry(120, 0, 800, 444)
        self.initCssUi()
        self.show()

    def initCssUi(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec())