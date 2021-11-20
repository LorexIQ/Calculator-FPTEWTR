from PyQt5 import QtCore, QtGui, QtWidgets


class CustonLineEdit:
    def __init__(self):
        self.state = False

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
        self.editState(1)
        self.lineEdit = QtWidgets.QLineEdit(centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(x + 75, y + 2, 126, 41))
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("border: 0;"
                                    "background-color: rgba(0,0,0,0);")
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged.connect(self.format_line)
        label_unit = QtWidgets.QLabel(centralwidget)
        label_unit.setGeometry(QtCore.QRect(x + 200, y + 1, 51, 41))
        label_unit.setFont(font)
        label_unit.setAlignment(QtCore.Qt.AlignCenter)
        label_unit.setObjectName("label_unit")
        label_object = QtWidgets.QLabel(centralwidget)
        label_object.setGeometry(QtCore.QRect(x, y + 6, 71, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_object.sizePolicy().hasHeightForWidth())
        font.setPointSize(font_size)
        label_object.setSizePolicy(sizePolicy)
        label_object.setFont(font)
        label_object.setAlignment(QtCore.Qt.AlignCenter)
        label_object.setObjectName("label_object")
        label_unit.setText(title_type)
        label_object.setText(title)

    # 1 - Ничего не введено
    # 2 - Ввод корректен
    # 3 - Ошибка формата
    def editState(self, state):
        self.state = False
        if state == 1:
            self.background.setPixmap(QtGui.QPixmap("imgs/normal.jpg"))
        elif state == 2:
            self.background.setPixmap(QtGui.QPixmap("imgs/ok.jpg"))
            self.state = True
        else:
            self.background.setPixmap(QtGui.QPixmap("imgs/error.jpg"))

    def format_line(self):
        t = self.lineEdit.text()
        if t == '':
            self.editState(1)
        elif t.isdigit() and int(t) != 0:
            self.editState(2)
        else:
            self.editState(3)


class Ui_MainWindow(object):
    def __init__(self):
        self.status_mode = 1

    def setupUi(self, MainWindow):
        def initWindowMode(info_edit_lines):
            window = QtWidgets.QWidget(self.centralwidget)
            window.setGeometry(0, 50, 545, 435)
            array_lines = []
            for i in info_edit_lines:
                array_lines.append(CustonLineEdit())
                array_lines[-1].initUi(*i, window)
            return window, array_lines

        def initButtonMode(title, widget, layout, css):
            font = QtGui.QFont()
            font.setFamily("Open Sans Condensed")
            font.setPointSize(14)
            font.setBold(False)
            font.setWeight(50)
            button = QtWidgets.QPushButton(widget)
            button.setObjectName(title)
            button.setMinimumSize(QtCore.QSize(150, 35))
            button.setStyleSheet(css)
            button.setText(title)
            button.setFont(font)
            button.clicked.connect(self.change_mode)
            layout.addWidget(button)
            return button

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(200, 15, 309, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.with_reinf_button = initButtonMode('WITH REINF', self.widget, self.horizontalLayout,
                                                "background-color: #97ff88; border: 1px solid #000;")
        self.without_reinf_button = initButtonMode('WITHOUT REINF', self.widget, self.horizontalLayout,
                                                   "background-color: #fff; border: 1px solid #000;")

        self.with_reinf, self.with_reinf_lines = initWindowMode([[(20, 20), 'a', 'мм', 16],
                                                                 [(20, 70), 'b', 'мм', 16],
                                                                 [(275, 70), 'b', 'мм', 16],
                                                                 [(20, 120), 'N', 'кН', 16],
                                                                 [(20, 170), 'M_x.sup', 'кН.м', 12],
                                                                 [(275, 170), 'M_y.sup', 'кН.м', 12],
                                                                 [(20, 220), 'M_x.inf', 'кН.м', 12],
                                                                 [(275, 220), 'M_y.inf', 'кН.м', 12],
                                                                 [(20, 270), 's_w', 'мм', 16],
                                                                 [(20, 320), 'R_bt', 'МПа', 16],
                                                                 [(20, 370), 'h_0', 'мм', 16]])

        self.without_reinf, self.without_reinf_lines = initWindowMode([[(20, 20), 'a', 'мм', 16],
                                                                       [(20, 70), 'b', 'мм', 16],
                                                                       [(275, 70), 'b', 'мм', 16],
                                                                       [(20, 120), 'N', 'кН', 16],
                                                                       [(20, 170), 'M_sup', 'кН.м', 16],
                                                                       [(275, 170), 'M_sup', 'кН.м', 16],
                                                                       [(20, 220), 'x_0', 'мм', 16],
                                                                       [(20, 270), 'R_bt', 'МПа', 16],
                                                                       [(20, 320), 'h_0', 'мм', 16]])
        self.with_reinf.hide()

        self.start_calculations = QtWidgets.QPushButton(self.centralwidget)
        self.start_calculations.setGeometry(350, 450, 200, 40)
        self.start_calculations.setText('Тест')
        self.start_calculations.clicked.connect(self.submit_enter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_mode(self):
        pass

    def submit_enter(self):
        for i in self.array_lines:
            if i.state is False:
                return False
        return True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
