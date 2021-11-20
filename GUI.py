from PyQt5 import QtCore, QtGui, QtWidgets


class CustonLineEdit:
    def __init__(self):
        self.state = False

    def initUi(self, set_coord, title, title_type, centralwidget):
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
        self.lineEdit.setStyleSheet("border: 0;\n"
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
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 444)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        info_edit_lines = [[(40, 70), 'h', 'm'],
                           [(40, 120), 'k', 'mm'],
                           [(40, 170), 'l', 'H']]
        self.array_lines = []

        for i in info_edit_lines:
            self.array_lines.append(CustonLineEdit())
            self.array_lines[-1].initUi(*i, self.centralwidget)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(240, 10, 195, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.start_calculations = QtWidgets.QPushButton(self.centralwidget)
        self.start_calculations.setText('Тест')
        self.start_calculations.clicked.connect(self.submit_enter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def submit_enter(self):
        for i in self.array_lines:
            if i.state is False:
                return False
        return True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
