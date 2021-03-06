import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from calculations.calculationsf import Calculate
from guide import Guide
from images import Scheme
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


class ResultMenu(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args[6:])
        self._objects = args[:6]
        self._timed_line = ''
        self._title_file = ''
        self._initUi()

    def _initUi(self):
        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setPointSize(16)
        self._font.setBold(False)
        self._font.setWeight(50)

        self.setGeometry(0, 50, 856, 510)

        self._back = QtWidgets.QPushButton(self)
        self._back.setGeometry(328, 435, 200, 40)
        self._back.setStyleSheet("background-color: #fffaea; border: 1px solid #000")
        self._font.setPointSize(16)
        self._back.setFont(self._font)
        self._back.clicked.connect(self._close_win)

        button = QtWidgets.QPushButton(self)
        button.setGeometry(20, 435, 40, 40)
        button.setStyleSheet('QPushButton {image: url(:/baseData/file/copy.png);}'
                             'QPushButton:disabled {image: url(:/baseData/file/copy_disabled.png);}')
        button.clicked.connect(self._saveFile)

        self.hide()

    def initUiBrowser(self, mode, msg, formuls, laung):
        self._ScrollArea = QtWidgets.QScrollArea(self)
        self._ScrollArea.setGeometry(20, 20, 816, 395)
        self._verticalLayoutWidget = QtWidgets.QWidget()
        verticalLayout = QtWidgets.QVBoxLayout(self._verticalLayoutWidget)
        self._verticalLayoutWidget.setMinimumSize(816, 395)

        if mode in [1, 2]:
            if mode == 1:
                color = '#97fe88'
            else:
                color = '#ffff84'
            self._verticalLayoutWidget.setStyleSheet('background: %s;' % color)

            label = QtWidgets.QLabel()
            label.setText(msg)
            self._font.setPointSize(16)
            label.setFont(self._font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            verticalLayout.addWidget(label)

            label = QtWidgets.QLabel()
            label.setText(laung)
            self._font.setPointSize(14)
            label.setFont(self._font)
            verticalLayout.addWidget(label)

            for formula in formuls:
                label = QtWidgets.QLabel()
                pixmap = self._Latex_to_Pixmap(formula, 12, color)
                label.setFixedHeight(pixmap.size().height() + 10)
                label.setPixmap(pixmap)
                verticalLayout.addWidget(label)
        elif mode == 3:
            self._verticalLayoutWidget.setStyleSheet('background: #f25961;')
            label = QtWidgets.QLabel()
            label.setText(msg)
            self._font.setPointSize(16)
            label.setFont(self._font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            verticalLayout.addWidget(label)

        self._ScrollArea.setWidget(self._verticalLayoutWidget)

    def _saveFile(self):
        file_link = QFileDialog.getSaveFileName(self, self._title_file[3], './',
                                                self._title_file[4] + ' (*.png)')
        if file_link[0] != '':
            self._verticalLayoutWidget.grab().save(file_link[0], 'png')

    def setLabels(self, new_title, new_title_file):
        self._back.setText(new_title)
        self._title_file = new_title_file

    def call(self):
        for object_red in self._objects:
            object_red.setEnabled(False)
        self._objects[-1].hide()
        self._timed_line = self._objects[2].toolTip()
        self._objects[2].setToolTip('')
        self.show()

    def _close_win(self):
        for object_red in self._objects:
            object_red.setEnabled(True)
        self._objects[-1].show()
        self._objects[2].setToolTip(self._timed_line)
        self.hide()

    @staticmethod
    def _Latex_to_Pixmap(Latex, fs, color):
        figure = Figure()
        figure.patch.set_facecolor(color)
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


class CustomComboBox:
    def __init__(self, place):
        self._object_name = ''
        self._place = place

    def initUi(self, set_coord, title, values=None):
        x, y = set_coord
        self._object_name = title
        self._values = values

        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setPointSize(16)
        self._font.setBold(False)
        self._font.setWeight(50)

        self._combo = QtWidgets.QComboBox(self._place)
        self._combo.setFont(self._font)
        self._combo.setGeometry(x + 69, y, 181, 45)
        self._combo.setMaxVisibleItems(3)
        self._combo.setStyleSheet('QComboBox {border: 0; background-image: url('
                                  ':/baseData/comboBox/background.png); padding-left: 10px;} '
                                  'QComboBox::drop-down {image: url(:/baseData/comboBox/background-down.png);}'
                                  'QComboBox::down-arrow {image: url(:/baseData/comboBox/pin.png); '
                                  'padding-top: 4px;}'
                                  'QListView {color: #606060; background-color: #fff; selection-background-color: '
                                  '#93cac4; selection-color: #000; padding-left: 8px; show-decoration-selected: 1;} '
                                  'QComboBox QAbstractItemView {outline: none;}'
                                  'QScrollBar {background: #fff; width: 10px;}'
                                  'QScrollBar::handle {background: #93cac4; border: 1px solid #000;}'
                                  'QScrollBar::handle:hover {background: #97e0d8;}')

        self._label_bombo = QtWidgets.QLabel(self._place)
        self._label_bombo.setGeometry(x, y, 69, 45)
        self._label_bombo.setAlignment(QtCore.Qt.AlignCenter)
        self._label_bombo.setStyleSheet('background-image: url(:/baseData/comboBox/labael.png);')

        if values is not None:
            for value in self._values:
                self._value = value
                self._combo.addItem(value)

    def get_text(self):
        return self._values[str(self._combo.currentText())]

    def getObject(self):
        return self._object_name

    def set_text(self, value):
        for i in self._values:
            if value == self._values[i]:
                self._combo.setCurrentText(i)
                break

    def editUnit(self, new_unit, size=16):
        self._font.setPointSize(size)
        self._label_bombo.setFont(self._font)
        self._label_bombo.setText(new_unit)


class CustomLineEdit:
    def __init__(self):
        self._state = False
        self._enable = True

    def initUi(self, centralwidget, set_coord, title, font_size, span=None):
        x, y = set_coord
        self._span = span

        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setPointSize(16)
        self._font.setBold(False)
        self._font.setWeight(50)

        self._label_object = QtWidgets.QLabel(centralwidget)
        self._label_object.setGeometry(QtCore.QRect(x, y, 69, 45))
        self._font.setPointSize(font_size)
        self._label_object.setFont(self._font)
        self._label_object.setAlignment(QtCore.Qt.AlignCenter)
        self._label_object.setText(title)
        self._editState(1)
        self._lineEdit = QtWidgets.QLineEdit(centralwidget)
        self._lineEdit.setGeometry(QtCore.QRect(x + 69, y, 132, 45))
        self._font.setPointSize(16)
        self._lineEdit.setFont(self._font)
        self._lineEdit.setStyleSheet("background-image: url(:/baseData/lineEdit/edit_line.png);"
                                     "border: 0; padding: 8px;")
        self._lineEdit.setMaxLength(10)
        self._lineEdit.textChanged.connect(self._format_line)
        self._label_unit = QtWidgets.QLabel(centralwidget)
        self._label_unit.setGeometry(QtCore.QRect(x + 201, y, 49, 45))
        self._label_unit.setFont(self._font)
        self._label_unit.setStyleSheet("background-image: url(:/baseData/lineEdit/unit.png);")
        self._label_unit.setAlignment(QtCore.Qt.AlignCenter)

    def _editState(self, state):
        self._state = False
        if state == 1:
            self._label_object.setStyleSheet('background-image: url(:/baseData/lineEdit/normal.png);')
        elif state == 2:
            self._label_object.setStyleSheet('background-image: url(:/baseData/lineEdit/ok.png);')
            self._state = True
        elif state == 3:
            self._label_object.setStyleSheet('background-image: url(:/baseData/lineEdit/error.png);')

    def editUnit(self, new_unit, size=16):
        self._font.setPointSize(size)
        self._label_unit.setFont(self._font)
        self._label_unit.setText(new_unit)

    def _format_line(self):
        t = self._lineEdit.text()
        if t == '':
            self._editState(1)
        elif t.isdigit() and (int(t) != 0 if self._span is None else self._span[0] <= int(t) <= self._span[1]):
            self._editState(2)
        else:
            self._editState(3)

    def getObject(self):
        return self._label_object.text()

    def get_text(self):
        return self._lineEdit.text()

    def get_state(self):
        return self._state

    def set_text(self, new_value):
        self._lineEdit.setText(new_value)


class WinProgram(object):
    def __init__(self):
        self._status_mode = 1

    def setupUi(self, MainWindow):
        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setBold(False)
        self._font.setWeight(50)

        self._initLaunguage()

        def initWindowMode(info_edit_lines):
            window = QtWidgets.QWidget(self._centralwidget)
            window.setGeometry(0, 50, 856, 495)
            array_lines = []
            for i in info_edit_lines:
                if type(i[0]) is tuple:
                    array_lines.append(CustomLineEdit())
                    array_lines[-1].initUi(window, *i)
                else:
                    array_lines.append(CustomComboBox(window))
                    array_lines[-1].initUi(*i[1:])
            return window, array_lines

        def initButtonMode(title, widget_in, layout, css):
            self._font.setPointSize(14)
            button = QtWidgets.QPushButton(widget_in)
            button.setMinimumSize(QtCore.QSize(150, 35))
            button.setStyleSheet(css)
            button.setFont(self._font)
            button.clicked.connect(lambda: self._change_mode(title))
            layout.addWidget(button)
            return button

        def initButtonFile(pos, score, img):
            button = QtWidgets.QPushButton(self._centralwidget)
            button.setGeometry(*pos, 40, 40)
            button.setStyleSheet('QPushButton {image: url(%s.png);}'
                                 'QPushButton:disabled {image: url(%s_disabled.png);}' % (img, img))
            button.clicked.connect(lambda: self._activeFileButtons(score))
            return button

        def initBunner(place):
            site = QtWidgets.QLabel(
                '<a href="https://github.com/LorexIQ/Calculator-FPTEWTR"><img src=":/baseData/site.png"/></a>', place)
            site.setGeometry(20, 335, 505, 80)
            site.setOpenExternalLinks(True)

        def initMiniScheme(place, link):
            with_img_scheme = QtWidgets.QPushButton(place)
            with_img_scheme.setGeometry(545, 20, 291, 395)
            with_img_scheme.setStyleSheet("QPushButton {background-image: url(:/baseData/scheme/%s.png); border: 0;}"
                                          "QPushButton:pressed {border: 0;}"
                                          "QPushButton:hover {background-image: url(:/baseData/scheme/%s_blur.png)}" %
                                          (link, link))
            with_img_scheme.clicked.connect(lambda: self._call_image_scheme(':/baseData/schemeFull/%s' % link + ('_ru'
                                                                            if self._changed == self._info_ru
                                                                            else '_en') + '.png'))

        def initVkIcon(title, link, pos):
            site = QtWidgets.QLabel(
                '<a href="%s"><img src=":/baseData/info/vk.png"/></a>' % link,
                self._centralwidget)
            site.setToolTip(title)
            site.setGeometry(pos[0], pos[1], 40, 40)
            site.setOpenExternalLinks(True)

        self._win_guide, self._win_scheme = None, None
        MainWindow.setFixedSize(856, 545)
        MainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        MainWindow.setWindowIcon(QtGui.QIcon(':/baseData/icon/main_litle.png'))
        self._centralwidget = QtWidgets.QWidget(MainWindow)
        self._font.setPointSize(11)
        QtWidgets.QToolTip.setFont(self._font)
        self._info_button = QtWidgets.QPushButton(self._centralwidget)
        self._info_button.setStyleSheet('QPushButton {image: url(:/baseData/info/info.png)}'
                                        'QPushButton:disabled {image: url(:/baseData/info/info_disabled.png)}')
        self._info_button.setGeometry(801, 20, 35, 35)
        self._info_button.clicked.connect(self._call_guide)
        widget = QtWidgets.QWidget(self._centralwidget)
        widget.setGeometry(QtCore.QRect(274, 15, 309, 41))
        horizontalLayout = QtWidgets.QHBoxLayout(widget)
        horizontalLayout.setSpacing(2)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self._with_reinf_button = initButtonMode('WITH REINF', widget, horizontalLayout,
                                                 "background-color: #97ff88; border: 1px solid #000;")
        self._without_reinf_button = initButtonMode('WITHOUT REINF', widget, horizontalLayout,
                                                    "background-color: #fff; border: 1px solid #000;")

        beton = {'B10': 0.56, 'B15': 0.75, 'B20': 0.9, 'B25': 1.05, 'B30': 1.15, 'B35': 1.3, 'B40': 1.4, 'B45': 1.5,
                 'B50': 1.6, 'B55': 1.7, 'B60': 1.8}
        fittings = {'A240': 170, 'A300': 215, 'A400': 285}

        self._with_reinf, self._with_reinf_lines = initWindowMode((((20, 20), 'h_0', 16, (70, 400)),
                                                                   ((20, 70), 'a', 16, (200, 800)),
                                                                   ((275, 70), 'b', 16, (200, 800)),
                                                                   ((20, 120), 'N', 16),
                                                                   ((20, 170), 'M_x.sup', 12, (0, 400)),
                                                                   ((275, 170), 'M_y.sup', 12, (0, 400)),
                                                                   ((20, 220), 'M_x.inf', 12, (0, 400)),
                                                                   ((275, 220), 'M_y.inf', 12, (0, 400)),
                                                                   (True, (275, 270), 'R_sw', fittings),
                                                                   (True, (20, 270), 'R_bt', beton)))
        initMiniScheme(self._with_reinf, 'with_reinf')
        initBunner(self._with_reinf)

        self._without_reinf, self._without_reinf_lines = initWindowMode((((20, 20), 'h_0', 16, (70, 400)),
                                                                         ((20, 70), 'a', 16, (200, 800)),
                                                                         ((275, 70), 'b', 16, (200, 800)),
                                                                         ((20, 120), 'N', 16),
                                                                         ((20, 170), 'M_sup', 14, (0, 400)),
                                                                         ((275, 170), 'M_inf', 14, (0, 400)),
                                                                         ((20, 220), 'x_0', 16),
                                                                         (True, (20, 270), 'R_bt', beton)))
        initMiniScheme(self._without_reinf, 'without_reinf')
        initBunner(self._without_reinf)
        self._without_reinf.hide()

        self._start_calculations = QtWidgets.QPushButton(self._centralwidget)
        self._start_calculations.setGeometry(328, 485, 200, 40)
        self._start_calculations.setStyleSheet("background-color: #99d9ea; border: 1px solid #000")
        self._font.setPointSize(14)
        self._start_calculations.setFont(self._font)
        self._start_calculations.clicked.connect(self._submit_enter)

        self._launguage_button = QtWidgets.QCheckBox(self._centralwidget)
        self._launguage_button.setGeometry(796, 485, 40, 40)
        self._launguage_button.setStyleSheet('QCheckBox::indicator:checked {image: url(:/baseData/launguage/en.png);}'
                                             'QCheckBox::indicator:unchecked {image: url(:/baseData/launguage/ru.png);}'
                                             'QCheckBox::indicator:disabled:checked {image: url('
                                             ':/baseData/launguage/en_disabled.png);}'
                                             'QCheckBox::indicator:disabled:unchecked {image: url('
                                             ':/baseData/launguage/ru_disabled.png);}')
        self._launguage_button.stateChanged.connect(self._changeLaunguage)

        self._copy_button = initButtonFile((20, 485), 1, ':/baseData/file/copy')
        self._paste_button = initButtonFile((63, 485), 2, ':/baseData/file/paste')

        self._result_menu = ResultMenu(self._with_reinf_button, self._without_reinf_button, self._info_button,
                                       self._launguage_button, self._copy_button, self._paste_button,
                                       self._centralwidget)

        initVkIcon('?????????????? ??????????????', 'https://vk.com/whedmitryel', (691, 485))
        initVkIcon('???????????????????? ??????????????????', 'https://vk.com/obitouchiha111', (736, 485))

        self._changeLaunguage()
        MainWindow.setCentralWidget(self._centralwidget)
        MainWindow.setWindowTitle('FPTEWTR')
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    @staticmethod
    def _create_set(objects):
        timed = []
        for i in objects:
            value = float(i.get_text()) if i.get_text() != '' else None
            if int(value) == value:
                value = int(value)
            timed.append(value)
        return tuple(timed)

    def _change_mode(self, title):
        def change_states(place_1, place_2):
            place_1[0].show()
            place_1[1].setStyleSheet("background-color: #97ff88; border: 1px solid #000;")
            place_2[0].hide()
            place_2[1].setStyleSheet("background-color: #fff; border: 1px solid #000;")

        if title == 'WITH REINF':
            change_states((self._with_reinf, self._with_reinf_button),
                          (self._without_reinf, self._without_reinf_button))
            self._info_button.setToolTip(self._changed['with'])
            self._status_mode = 1
        elif title == 'WITHOUT REINF':
            change_states((self._without_reinf, self._without_reinf_button),
                          (self._with_reinf, self._with_reinf_button))
            self._info_button.setToolTip(self._changed['without'])
            self._status_mode = 2

    def _submit_enter(self):
        array_lines = self._with_reinf_lines if self._status_mode == 1 else self._without_reinf_lines
        for i in array_lines:
            if type(i) is not CustomComboBox and i.get_state() is False:
                QtWidgets.QMessageBox.critical(self._centralwidget, self._changed['error'][0],
                                               self._changed['error'][1], QtWidgets.QMessageBox.Ok)
                return False
        result_tuple = self._create_set(array_lines)
        calc = Calculate(self._changed['calculation_class'])
        if self._status_mode == 1:
            self._call_result_menu(calc.calculate_with_reinf(result_tuple), calc.get_status(),
                                   calc.get_solution_progress_inr())
        elif self._status_mode == 2:
            self._call_result_menu(calc.calculate_without_reinf(result_tuple), calc.get_status(),
                                   calc.get_solution_progress_less_r())

    def _call_result_menu(self, msg, type_screen, array_formuls):
        self._result_menu.initUiBrowser(type_screen, msg, array_formuls, self._changed['calculation_class']['calc'])
        self._result_menu.call()

    @staticmethod
    def _readFileLaunguage(name):
        with open('launguage/' + name, 'rb') as file:
            info = pickle.load(file)
        return info

    def _initLaunguage(self):
        self._info_ru = self._readFileLaunguage('ru.lng')
        self._info_en = self._readFileLaunguage('en.lng')

    def _changeLaunguage(self):
        self._changed = self._info_en if self._launguage_button.isChecked() else self._info_ru
        self._info_button.setToolTip(self._changed['with'])
        self._with_reinf_button.setText(self._changed['with_button'])
        self._without_reinf_button.setText(self._changed['without_button'])
        self._start_calculations.setText(self._changed['start_button'])
        for i in self._with_reinf_lines:
            called = self._changed['with_edit_unit'][i.getObject()]
            i.editUnit(called[0], called[1])
        for i in self._without_reinf_lines:
            called = self._changed['without_edit_unit'][i.getObject()]
            i.editUnit(called[0], called[1])
        self._result_menu.setLabels(self._changed['back'], self._changed['file'])

    @staticmethod
    def _readLines(objects):
        array_values = []
        for i in objects:
            array_values.append(i.get_text())
        return array_values

    def _readFile(self):
        file_link = None
        if self._status_mode == 1:
            file_link = QFileDialog.getOpenFileName(self._centralwidget, self._changed['file'][1], './',
                                                    self._changed['file'][2] + ' (*.calcI)')
        elif self._status_mode == 2:
            file_link = QFileDialog.getOpenFileName(self._centralwidget, self._changed['file'][1], './',
                                                    self._changed['file'][2] + ' (*.calcL)')
        if file_link is not None:
            file_calc = open(str(file_link[0]), "rb")
            values = pickle.load(file_calc)
            file_calc.close()
            return values

    def _writeFile(self, array_value):
        f_name = None
        if self._status_mode == 1:
            file_link = QFileDialog.getSaveFileName(self._centralwidget, self._changed['file'][0], './',
                                                    self._changed['file'][2] + ' (*.calcI)')
            f_name = str(file_link[0])
        elif self._status_mode == 2:
            file_link = QFileDialog.getSaveFileName(self._centralwidget, self._changed['file'][0], './',
                                                    self._changed['file'][2] + ' (*.calcL)')
            f_name = str(file_link[0])
        file_calc = open(f_name, "wb")
        pickle.dump(array_value, file_calc)

    def _activeFileButtons(self, type_button):
        worked = self._with_reinf_lines if self._status_mode == 1 else self._without_reinf_lines
        if type_button == 1:
            try:
                self._writeFile(self._readLines(worked))
            except:
                QtWidgets.QMessageBox.critical(self._centralwidget, self._changed['error'][2],
                                               self._changed['error'][4], QtWidgets.QMessageBox.Ok)
        elif type_button == 2:
            try:
                array_new_values = self._readFile()
                for line, value in zip(worked, array_new_values):
                    line.set_text(value)
            except:
                QtWidgets.QMessageBox.critical(self._centralwidget, self._changed['error'][3],
                                               self._changed['error'][4], QtWidgets.QMessageBox.Ok)

    def _call_guide(self):
        self.exit()
        self._win_guide = Guide(self._changed['guide'])
        self._win_guide.show()
        self._win_guide.activateWindow()

    def _call_image_scheme(self, link):
        self._win_scheme = Scheme(link)
        self._win_scheme.show()
        self._win_scheme.activateWindow()

    def exit(self, mode=False):
        if self._win_guide is not None:
            self._win_guide.close()
        if mode and self._win_scheme is not None:
            self._win_scheme.close()
