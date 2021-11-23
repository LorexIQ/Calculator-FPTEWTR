from PyQt5 import QtCore, QtGui, QtWidgets
from calculations.calculationsf import Calculate
from guide import Guide
import pickle


class ResultMenu(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args[6:])
        self._objects = args[:6]
        self._timed_line = ''
        self._initUi()

    def _initUi(self):
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)

        self.setGeometry(0, 50, 856, 510)
        self._img_result = QtWidgets.QLabel(self)
        self._img_result.setGeometry(20, 20, 816, 395)
        self._title = QtWidgets.QLabel(self)
        self._title.setGeometry(40, 40, 776, 355)
        self._title.setAlignment(QtCore.Qt.AlignCenter)
        font.setPointSize(20)
        self._title.setFont(font)

        self._back = QtWidgets.QPushButton(self)
        self._back.setGeometry(328, 435, 200, 40)
        self._back.setStyleSheet("background-color: #fffaea; border: 1px solid #000")
        font.setPointSize(16)
        self._back.setFont(font)
        self._back.clicked.connect(self.close_win)

        self.hide()

    def setLabelBackButton(self, new_title):
        self._back.setText(new_title)

    def change_img(self, img):
        if img == 1:
            self._img_result.setPixmap(QtGui.QPixmap('imgs/result/ok.jpg'))
        elif img == 2:
            self._img_result.setPixmap(QtGui.QPixmap('imgs/result/warming.jpg'))
        elif img == 3:
            self._img_result.setPixmap(QtGui.QPixmap('imgs/result/critical.jpg'))

    def set_title(self, title):
        self._title.setText(title)

    def call(self):
        for object_red in self._objects:
            object_red.setEnabled(False)
        self._timed_line = self._objects[2].toolTip()
        self._objects[2].setToolTip('')
        self.show()

    def close_win(self):
        for object_red in self._objects:
            object_red.setEnabled(True)
        self._objects[2].setToolTip(self._timed_line)
        self.hide()


class CustonLineEdit:
    def __init__(self):
        self._state = False
        self._enable = True

    def initUi(self, set_coord, title, font_size, centralwidget):
        x, y = set_coord
        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setPointSize(16)
        self._font.setBold(False)
        self._font.setWeight(50)
        self._background = QtWidgets.QLabel(centralwidget)
        self._background.setGeometry(QtCore.QRect(x, y, 250, 45))
        self._editState(1)
        self._lineEdit = QtWidgets.QLineEdit(centralwidget)
        self._lineEdit.setGeometry(QtCore.QRect(x + 75, y + 2, 126, 41))
        self._lineEdit.setFont(self._font)
        self._lineEdit.setStyleSheet("border: 0;"
                                     "background-color: rgba(0,0,0,0);")
        self._lineEdit.setMaxLength(10)
        self._lineEdit.textChanged.connect(self._format_line)
        self._label_unit = QtWidgets.QLabel(centralwidget)
        self._label_unit.setGeometry(QtCore.QRect(x + 200, y, 51, 45))
        self._label_unit.setFont(self._font)
        self._label_unit.setAlignment(QtCore.Qt.AlignCenter)
        self._label_object = QtWidgets.QLabel(centralwidget)
        self._label_object.setGeometry(QtCore.QRect(x, y, 71, 45))
        self._font.setPointSize(font_size)
        self._label_object.setFont(self._font)
        self._label_object.setAlignment(QtCore.Qt.AlignCenter)
        self._label_object.setText(title)
        self._background.setToolTip('test')

    def _editState(self, state):
        self._state = False
        if state == 1:
            self._background.setPixmap(QtGui.QPixmap("imgs/lineEdit/normal.jpg"))
        elif state == 2:
            self._background.setPixmap(QtGui.QPixmap("imgs/lineEdit/ok.jpg"))
            self._state = True
        elif state == 3:
            self._background.setPixmap(QtGui.QPixmap("imgs/lineEdit/error.jpg"))
        elif state == 4:
            self._state = True
            self._background.setPixmap(QtGui.QPixmap("imgs/lineEdit/falsed.jpg"))

    def editUnit(self, new_unit, size=16):
        self._font.setPointSize(size)
        self._label_unit.setFont(self._font)
        self._label_unit.setText(new_unit)

    def _format_line(self):
        t = self._lineEdit.text()
        if t == '':
            self._editState(1)
        elif t.isdigit() and int(t) != 0:
            self._editState(2)
        else:
            self._editState(3)

    def change_enabled(self):
        if self._enable:
            self._lineEdit.setEnabled(False)
            self._editState(4)
            self._enable = False
        else:
            self._lineEdit.setEnabled(True)
            self._enable = True
            self._format_line()

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
                array_lines.append(CustonLineEdit())
                array_lines[-1].initUi(*i, window)
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

        def initCheckBox(height, place, lines):
            lines[-1].change_enabled()
            selector = QtWidgets.QCheckBox(place)
            selector.setGeometry(275, height, 45, 45)
            selector.setStyleSheet('QCheckBox::indicator:checked {image: url(imgs/checkbox/checked.jpg);}'
                                   'QCheckBox::indicator:unchecked {image: url(imgs/checkbox/unchecked.jpg);}')
            selector.stateChanged.connect(lines[-1].change_enabled)

        def initButtonFile(pos, score, img):
            button = QtWidgets.QPushButton(self._centralwidget)
            button.setGeometry(*pos, 40, 40)
            button.setStyleSheet('QPushButton {image: url(%s.png);}'
                                 'QPushButton:disabled {image: url(%s_disabled.png);}' % (img, img))
            button.clicked.connect(lambda: self._activeFileButtons(score))
            return button

        self._win_guide = None
        MainWindow.setFixedSize(856, 545)
        MainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        MainWindow.setWindowIcon(QtGui.QIcon('imgs/icon/main_litle.png'))
        self._centralwidget = QtWidgets.QWidget(MainWindow)
        self._font.setPointSize(11)
        QtWidgets.QToolTip.setFont(self._font)
        self._info_button = QtWidgets.QPushButton(self._centralwidget)
        self._info_button.setStyleSheet('QPushButton {image: url(imgs/info/info.png)}'
                                        'QPushButton:disabled {image: url(imgs/info/info_disabled.png)}')
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

        self._with_reinf, self._with_reinf_lines = initWindowMode([[(20, 20), 'h', 16],
                                                                   [(20, 70), 'a', 16],
                                                                   [(275, 70), 'b', 16],
                                                                   [(20, 120), 'N', 16],
                                                                   [(20, 170), 'M_x.sup', 12],
                                                                   [(275, 170), 'M_y.sup', 12],
                                                                   [(20, 220), 'M_x.inf', 12],
                                                                   [(275, 220), 'M_y.inf', 12],
                                                                   [(20, 270), 's_w', 16],
                                                                   [(20, 320), 'R_bt', 16],
                                                                   [(20, 370), 'h_0', 16]])
        initCheckBox(370, self._with_reinf, self._with_reinf_lines)
        with_img_scheme = QtWidgets.QLabel(self._with_reinf)
        with_img_scheme.setGeometry(545, 20, 291, 395)
        with_img_scheme.setPixmap(QtGui.QPixmap("imgs/scheme/with_scheme.jpg"))

        self._without_reinf, self._without_reinf_lines = initWindowMode([[(20, 20), 'h', 16],
                                                                         [(20, 70), 'a', 16],
                                                                         [(275, 70), 'b', 16],
                                                                         [(20, 120), 'N', 16],
                                                                         [(20, 170), 'M_sup', 14],
                                                                         [(275, 170), 'M_inf', 14],
                                                                         [(20, 220), 'x_0', 16],
                                                                         [(20, 270), 'R_bt', 16],
                                                                         [(20, 320), 'h_0', 16]])
        initCheckBox(320, self._without_reinf, self._without_reinf_lines)
        without_img_scheme = QtWidgets.QLabel(self._without_reinf)
        without_img_scheme.setGeometry(545, 20, 291, 395)
        without_img_scheme.setPixmap(QtGui.QPixmap("imgs/scheme/without_scheme.jpg"))
        self._without_reinf.hide()

        self._start_calculations = QtWidgets.QPushButton(self._centralwidget)
        self._start_calculations.setGeometry(328, 485, 200, 40)
        self._start_calculations.setStyleSheet("background-color: #99d9ea; border: 1px solid #000")
        self._font.setPointSize(14)
        self._start_calculations.setFont(self._font)
        self._start_calculations.clicked.connect(self._submit_enter)

        self._launguage_button = QtWidgets.QCheckBox(self._centralwidget)
        self._launguage_button.setGeometry(796, 485, 40, 40)
        self._launguage_button.setStyleSheet('QCheckBox::indicator:checked {image: url(imgs/launguage/en.png);}'
                                             'QCheckBox::indicator:unchecked {image: url(imgs/launguage/ru.png);}'
                                             'QCheckBox::indicator:disabled:checked {image: url('
                                             'imgs/launguage/en_disabled.png);}'
                                             'QCheckBox::indicator:disabled:unchecked {image: url('
                                             'imgs/launguage/ru_disabled.png);}')
        self._launguage_button.stateChanged.connect(self._changeLaunguage)

        self._copy_button = initButtonFile((20, 485), 1, 'imgs/file/copy')
        self._paste_button = initButtonFile((63, 485), 2, 'imgs/file/paste')

        self._result_menu = ResultMenu(self._with_reinf_button, self._without_reinf_button, self._info_button,
                                       self._launguage_button, self._copy_button, self._paste_button,
                                       self._centralwidget)

        self._changeLaunguage()
        MainWindow.setCentralWidget(self._centralwidget)
        MainWindow.setWindowTitle('FPTEWTR')
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    @staticmethod
    def _create_set(lines):
        timed = []
        for i in lines:
            timed.append(int(i.get_text()) if i.get_text() != '' else None)
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
            if i.get_state() is False:
                QtWidgets.QMessageBox.critical(self._centralwidget, self._changed['error'][0],
                                               self._changed['error'][1], QtWidgets.QMessageBox.Ok)
                return False
        result_tuple = self._create_set(array_lines)
        calc = Calculate(self._changed['calculation_class'])
        if self._status_mode == 1:
            self._call_result_menu(*(calc.calculate_with_reinf(result_tuple), calc.get_status()))
        elif self._status_mode == 2:
            self._call_result_menu(*(calc.calculate_without_reinf(result_tuple), calc.get_status()))

    def _call_result_menu(self, msg, type_screen):
        self._result_menu.change_img(type_screen)
        self._result_menu.set_title(msg)
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
        self._result_menu.setLabelBackButton(self._changed['back'])

    @staticmethod
    def _readLines(lines):
        array_values = []
        for i in lines:
            array_values.append(i.get_text())
        return array_values

    def _readFile(self):  # Функция чтения файла
        file_link = '<ссылка на файл полученная через QFileDialog>'
        mode = self._status_mode  # 1 - with, 2 - without
        values = []  # Массив с новыми данными
        # Сделай защиту, чтобы нельзя было прочитать файл сохранения with в поля without.
        # Можно сделать первым значением в файле сохранения, переменную str: with | without.
        # Можно сравнить _status_mode и первую переменную в файлах
        return values

    def _writeFile(self, array_value):  # Функция записи файла
        pass

    def _activeFileButtons(self, type_button):  # Функция определения кнопок по идее готова. Дальше сам. Удали коменты
        worked = self._with_reinf_lines if self._status_mode == 1 else self._without_reinf_lines
        if type_button == 1:
            self._writeFile(self._readLines(worked))
        elif type_button == 2:
            array_new_values = self._readFile()
            for line, value in zip(worked, array_new_values):
                line.set_text(value)

    def _call_guide(self):
        self.exit()
        self._win_guide = Guide(self._changed['guide'])
        self._win_guide.show()
        self._win_guide.activateWindow()

    def exit(self):
        if self._win_guide is not None:
            self._win_guide.close()
