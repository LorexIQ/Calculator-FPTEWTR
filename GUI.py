from PyQt5 import QtCore, QtGui, QtWidgets


class ResultMenu(QtWidgets.QWidget):
    def __init__(self, button_1, button_2, info, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.button_1 = button_1
        self.button_2 = button_2
        self.info = info
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

        back = QtWidgets.QPushButton(self)
        back.setGeometry(328, 435, 200, 40)
        back.setText('BACK')
        back.setStyleSheet("background-color: #fffaea; border: 1px solid #000")
        font.setPointSize(16)
        back.setFont(font)
        back.clicked.connect(self.close_win)

        self.hide()

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
        self.button_1.setEnabled(False)
        self.button_2.setEnabled(False)
        self.info.hide()
        self.show()

    def close_win(self):
        self.button_1.setEnabled(True)
        self.button_2.setEnabled(True)
        self.info.show()
        self.hide()


class CustonLineEdit:
    def __init__(self):
        self._state = False
        self._enable = True

    def get_state(self):
        return self._state

    def initUi(self, set_coord, title, title_type, font_size, centralwidget):
        x, y = set_coord
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.background = QtWidgets.QLabel(centralwidget)
        self.background.setGeometry(QtCore.QRect(x, y, 250, 45))
        self.background.setText("")
        self.background.setObjectName("background")
        self._editState(1)
        self.lineEdit = QtWidgets.QLineEdit(centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(x + 75, y + 2, 126, 41))
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("border: 0;"
                                    "background-color: rgba(0,0,0,0);")
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged.connect(self._format_line)
        label_unit = QtWidgets.QLabel(centralwidget)
        label_unit.setGeometry(QtCore.QRect(x + 200, y + 1, 51, 41))
        label_unit.setFont(font)
        label_unit.setAlignment(QtCore.Qt.AlignCenter)
        label_unit.setObjectName("label_unit")
        label_object = QtWidgets.QLabel(centralwidget)
        label_object.setGeometry(QtCore.QRect(x, y + 6, 71, 31))
        font.setPointSize(font_size)
        label_object.setFont(font)
        label_object.setAlignment(QtCore.Qt.AlignCenter)
        label_object.setObjectName("label_object")
        label_unit.setText(title_type)
        label_object.setText(title)
        self.background.setToolTip('test')

    # 1 - Ничего не введено
    # 2 - Ввод корректен
    # 3 - Ошибка формата
    # 4 - Выключено
    def _editState(self, state):
        self._state = False
        if state == 1:
            self.background.setPixmap(QtGui.QPixmap("imgs/lineEdit/normal.jpg"))
        elif state == 2:
            self.background.setPixmap(QtGui.QPixmap("imgs/lineEdit/ok.jpg"))
            self._state = True
        elif state == 3:
            self.background.setPixmap(QtGui.QPixmap("imgs/lineEdit/error.jpg"))
        elif state == 4:
            self._state = True
            self.background.setPixmap(QtGui.QPixmap("imgs/lineEdit/falsed.jpg"))

    def _format_line(self):
        t = self.lineEdit.text()
        if t == '':
            self._editState(1)
        elif t.isdigit() and int(t) != 0:
            self._editState(2)
        else:
            self._editState(3)

    def change_enabled(self):
        if self._enable:
            self.lineEdit.setEnabled(False)
            self._editState(4)
            self._enable = False
        else:
            self.lineEdit.setEnabled(True)
            self._enable = True
            self._format_line()


class WinProgram(object):
    def __init__(self):
        self._status_mode = 1

    def setupUi(self, MainWindow):
        self._font = QtGui.QFont()
        self._font.setFamily("Open Sans Condensed")
        self._font.setBold(False)
        self._font.setWeight(50)

        self._info = {'with': 'h - толщина плиты\n'
                              'ho - высота рабочей поверхности\n'
                              'a / b - сечение колонн, примыкающих к полу снизу и сверху \n'
                              'N - нагрузка, передаваемая от пола на колонну \n'
                              'M_x.sup / M_y.sup и M_x.inf /  M_y.inf - моменты в сечениях колонн по верхнему и\n'
                              'нижнему краям плиты в направлении колонны с размерами «a» и «b» соответственно\n'
                              's_w - класс требований к сдвигу арматуры, класс бетона\n'
                              'r_b - осевое растяжение',
                      'without': 'h - толщина плиты\n'
                                 'ho - высота рабочей поверхности\n'
                                 'a / b - сечение колонн, примыкающих к полу снизу и сверху\n'
                                 'N - нагрузка, передаваемая с пола на колонну\n'
                                 'х0 - центр колонны расположен в точке x0 от  свободный край плиты\n'
                                 'M_sup / M_inf - моменты сечения колонны по верхней и нижней границам плиты\n'
                                 'r_b - осевое растяжение'}

        def initWindowMode(info_edit_lines):
            window = QtWidgets.QWidget(self._centralwidget)
            window.setGeometry(0, 50, 856, 435)
            array_lines = []
            for i in info_edit_lines:
                array_lines.append(CustonLineEdit())
                array_lines[-1].initUi(*i, window)
            return window, array_lines

        def initButtonMode(title, widget_in, layout, css):
            self._font.setPointSize(14)
            button = QtWidgets.QPushButton(widget_in)
            button.setObjectName(title)
            button.setMinimumSize(QtCore.QSize(150, 35))
            button.setStyleSheet(css)
            button.setText(title)
            button.setFont(self._font)
            button.clicked.connect(lambda: self._change_mode(title))
            layout.addWidget(button)
            return button

        def initCheckBox(height, place, lines):
            lines[-1].change_enabled()
            selector = QtWidgets.QCheckBox(place)
            selector.setGeometry(275, height, 45, 45)
            selector.setStyleSheet('QCheckBox::indicator {width:  45px; height: 45px;}'
                                   'QCheckBox::indicator:checked {image: url(imgs/checkbox/checked.jpg);}'
                                   'QCheckBox::indicator:unchecked {image: url(imgs/checkbox/unchecked.jpg);}')
            selector.stateChanged.connect(lines[-1].change_enabled)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(856, 545)
        MainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self._centralwidget = QtWidgets.QWidget(MainWindow)
        self._centralwidget.setObjectName("centralwidget")
        self._font.setPointSize(11)
        QtWidgets.QToolTip.setFont(self._font)
        self._info_label = QtWidgets.QLabel(self._centralwidget)
        self._info_label.setPixmap(QtGui.QPixmap('imgs/info.png'))
        self._info_label.setGeometry(801, 20, 35, 35)
        widget = QtWidgets.QWidget(self._centralwidget)
        widget.setGeometry(QtCore.QRect(274, 15, 309, 41))
        widget.setObjectName("widget")
        horizontalLayout = QtWidgets.QHBoxLayout(widget)
        horizontalLayout.setSpacing(2)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setObjectName("horizontalLayout")
        self._with_reinf_button = initButtonMode('WITH REINF', widget, horizontalLayout,
                                                 "background-color: #97ff88; border: 1px solid #000;")
        self._without_reinf_button = initButtonMode('WITHOUT REINF', widget, horizontalLayout,
                                                    "background-color: #fff; border: 1px solid #000;")
        self._info_label.setToolTip(self._info['with'])

        self._with_reinf, self._with_reinf_lines = initWindowMode([[(20, 20), 'h', 'мм', 16],
                                                                   [(20, 70), 'a', 'мм', 16],
                                                                   [(275, 70), 'b', 'мм', 16],
                                                                   [(20, 120), 'N', 'кН', 16],
                                                                   [(20, 170), 'M_x.sup', 'кН.м', 12],
                                                                   [(275, 170), 'M_y.sup', 'кН.м', 12],
                                                                   [(20, 220), 'M_x.inf', 'кН.м', 12],
                                                                   [(275, 220), 'M_y.inf', 'кН.м', 12],
                                                                   [(20, 270), 's_w', 'мм', 16],
                                                                   [(20, 320), 'R_bt', 'МПа', 16],
                                                                   [(20, 370), 'h_0', 'мм', 16]])
        initCheckBox(370, self._with_reinf, self._with_reinf_lines)
        with_img_scheme = QtWidgets.QLabel(self._with_reinf)
        with_img_scheme.setGeometry(545, 20, 291, 395)
        with_img_scheme.setPixmap(QtGui.QPixmap("imgs/with_scheme.jpg"))

        self._without_reinf, self._without_reinf_lines = initWindowMode([[(20, 20), 'h', 'мм', 16],
                                                                         [(20, 70), 'a', 'мм', 16],
                                                                         [(275, 70), 'b', 'мм', 16],
                                                                         [(20, 120), 'N', 'кН', 16],
                                                                         [(20, 170), 'M_sup', 'кН.м', 14],
                                                                         [(275, 170), 'M_sup', 'кН.м', 14],
                                                                         [(20, 220), 'x_0', 'мм', 16],
                                                                         [(20, 270), 'R_bt', 'МПа', 16],
                                                                         [(20, 320), 'h_0', 'мм', 16]])
        initCheckBox(320, self._without_reinf, self._without_reinf_lines)
        without_img_scheme = QtWidgets.QLabel(self._without_reinf)
        without_img_scheme.setGeometry(545, 20, 291, 395)
        without_img_scheme.setPixmap(QtGui.QPixmap("imgs/without_scheme.jpg"))
        self._without_reinf.hide()

        start_calculations = QtWidgets.QPushButton(self._centralwidget)
        start_calculations.setGeometry(328, 485, 200, 40)
        start_calculations.setText('CALCULATE')
        start_calculations.setStyleSheet("background-color: #99d9ea; border: 1px solid #000")
        self._font.setPointSize(14)
        start_calculations.setFont(self._font)
        start_calculations.clicked.connect(self._submit_enter)

        self._result_menu = ResultMenu(self._with_reinf_button, self._without_reinf_button, self._info_label,
                                       self._centralwidget)

        MainWindow.setCentralWidget(self._centralwidget)
        MainWindow.setWindowTitle('FPTEWTR')
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    @staticmethod
    def _create_set(lines):
        timed = []
        for i in lines:
            timed.append(int(i.lineEdit.text()) if i.lineEdit.text() != '' else None)
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
            self._info_label.setToolTip(self._info['with'])
            self._status_mode = 1
        elif title == 'WITHOUT REINF':
            change_states((self._without_reinf, self._without_reinf_button),
                          (self._with_reinf, self._with_reinf_button))
            self._info_label.setToolTip(self._info['without'])
            self._status_mode = 2

    def _submit_enter(self):
        array_lines = self._with_reinf_lines if self._status_mode == 1 else self._without_reinf_lines
        for i in array_lines:
            if i.get_state() is False:
                QtWidgets.QMessageBox.critical(self._centralwidget, 'Ошибка введённых данных!',
                                               "Заполнены не все поля или введён неверный тип данных",
                                               QtWidgets.QMessageBox.Ok)
                return False
        result_tuple = self._create_set(array_lines)  # <---- Финальный кортёж
        if self._status_mode == 1:
            self._call_result_menu(*('1', 1))  # Вызови функцию с прутками и передай туда result_tuple
        elif self._status_mode == 2:
            self._call_result_menu(*('2', 2))  # Вызови функцию без прутков и передай туда result_tuple
        # Функции вернут строки. Придуймай, чтобы возвращали ещё и цифру состояния в кортеже:
        # 1 - Ok
        # 2 - Warming
        # 3 - Critical
        # Передай результат в функцию call_result_menu(*(str, int))
        # По Окончанию, комментарии сотри

    def _call_result_menu(self, msg, type_screen):
        self._result_menu.change_img(type_screen)
        self._result_menu.set_title(msg)
        self._result_menu.call()
