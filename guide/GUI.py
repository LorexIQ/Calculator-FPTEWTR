from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.figure as fg
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg


class customButton(QtWidgets.QPushButton):
    def __init__(self, unit, function):
        super(customButton, self).__init__()
        self._text = unit[1][unit[0]]
        self._function = function
        self._initUi(unit[0])

    def _initUi(self, unit):
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(12)
        self.setText(unit)
        self.setFixedSize(85, 30)
        self.setFont(font)
        self.clicked.connect(lambda: self._function(self._text))

    def set_info(self, text):
        self._text = text

    def get_info(self):
        return self._text


class Ui_Guide(object):
    def setupUi(self, Form, info):
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setBold(False)
        font.setWeight(50)

        Form.setFixedSize(480, 240)
        Form.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setWindowIcon(QtGui.QIcon(':/baseData/icon/main_litle.png'))
        Form.setWindowTitle(info[0])
        scrollArea = QtWidgets.QScrollArea(Form)
        scrollArea.setGeometry(QtCore.QRect(20, 20, 121, 201))
        scrollArea.setStyleSheet('QScrollArea {border: 1.5px solid #000;}'
                                 'QScrollBar {background : #fff; width: 10px;}'
                                 'QScrollBar::handle {background : #93cac4;}'
                                 'QScrollBar::handle:hover {background : #97e0d8;}')
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        verticalLayoutWidget = QtWidgets.QWidget()
        verticalLayoutWidget.setStyleSheet('QWidget {background: #fff;}'
                                           'QPushButton {background: #93cac4; border: 1px solid #000;}'
                                           'QPushButton:hover {background: #97e0d8;}')
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        for i in info[1]:
            button = customButton((i, info[1]), self.changeButton)
            verticalLayout.addWidget(button)
        scrollArea.setWidget(verticalLayoutWidget)
        self._textBrowser = QtWidgets.QTextBrowser(Form)
        self._textBrowser.setGeometry(QtCore.QRect(160, 20, 301, 201))
        self._textBrowser.setStyleSheet('border: 1.5px solid #000;')
        self._textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def changeButton(self, text):
        self._textBrowser.setHtml(QtCore.QCoreApplication.translate("Form", u"%s" % text, None))

    @staticmethod
    def _Latex_to_Pixmap(Latex, fs):
        figure = mpl.figure.Figure()
        figure.patch.set_facecolor('#97ff88')
        figure.set_canvas(FigureCanvasAgg(figure))
        renderer = figure.canvas.get_renderer()
        ax = figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        t = ax.text(0, 0, Latex, ha='left', va='bottom', fontsize=fs)
        fwidth, fheight = figure.get_size_inches()
        fig_bbox = figure.get_window_extent(renderer)
        text_bbox = t.get_window_extent(renderer)
        figure.set_size_inches(text_bbox.width * fwidth / fig_bbox.width, text_bbox.height * fheight / fig_bbox.height)
        buf, size = figure.canvas.print_to_buffer()
        pixmap = QtGui.QPixmap(QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1], QtGui.QImage.Format_ARGB32)))
        return pixmap
