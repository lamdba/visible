
from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import MyView


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        #~ self.canvas = QtWidgets.QGraphicsView(self.centralWidget)
        self.canvas = MyView(self.centralWidget)
        self.canvas.setGeometry(QtCore.QRect(119, 0, 762, 700))
        self.canvas.setObjectName("canvas")
        self.button_design = QtWidgets.QPushButton(self.centralWidget)
        self.button_design.setGeometry(QtCore.QRect(0, 0, 122, 700))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.button_design.setFont(font)
        self.button_design.setMouseTracking(True)
        self.button_design.setIconSize(QtCore.QSize(64, 64))
        self.button_design.setObjectName("button_design")
        self.button_test = QtWidgets.QPushButton(self.centralWidget)
        self.button_test.setGeometry(QtCore.QRect(879, 0, 122, 700))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.button_test.setFont(font)
        self.button_test.setIconSize(QtCore.QSize(64, 64))
        self.button_test.setObjectName("button_test")
        self.button_cursor = QtWidgets.QToolButton(self.centralWidget)
        self.button_cursor.setGeometry(QtCore.QRect(30, 20, 61, 61))
        self.button_cursor.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/res/cursor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cursor.setIcon(icon1)
        self.button_cursor.setIconSize(QtCore.QSize(32, 32))
        self.button_cursor.setObjectName("button_cursor")
        self.button_en = QtWidgets.QToolButton(self.centralWidget)
        self.button_en.setGeometry(QtCore.QRect(30, 90, 61, 61))
        self.button_en.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_en.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/en.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_en.setIcon(icon2)
        self.button_en.setIconSize(QtCore.QSize(64, 64))
        self.button_en.setObjectName("button_en")
        self.button_in = QtWidgets.QToolButton(self.centralWidget)
        self.button_in.setGeometry(QtCore.QRect(30, 160, 61, 61))
        self.button_in.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/res/in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_in.setIcon(icon3)
        self.button_in.setIconSize(QtCore.QSize(64, 64))
        self.button_in.setObjectName("button_in")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(890, 30, 51, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(940, 20, 61, 61))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.button_next = QtWidgets.QPushButton(self.centralWidget)
        self.button_next.setGeometry(QtCore.QRect(900, 90, 81, 31))
        self.button_next.setObjectName("button_next")
        self.button_continue = QtWidgets.QToolButton(self.centralWidget)
        self.button_continue.setGeometry(QtCore.QRect(900, 140, 81, 31))
        self.button_continue.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/res/continue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_continue.setIcon(icon4)
        self.button_continue.setIconSize(QtCore.QSize(32, 32))
        self.button_continue.setObjectName("button_continue")
        self.button_pause = QtWidgets.QToolButton(self.centralWidget)
        self.button_pause.setGeometry(QtCore.QRect(900, 140, 81, 31))
        self.button_pause.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/res/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_pause.setIcon(icon5)
        self.button_pause.setIconSize(QtCore.QSize(32, 32))
        self.button_pause.setObjectName("button_pause")
        self.button_connect = QtWidgets.QToolButton(self.centralWidget)
        self.button_connect.setGeometry(QtCore.QRect(30, 230, 61, 61))
        self.button_connect.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/res/connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_connect.setIcon(icon6)
        self.button_connect.setIconSize(QtCore.QSize(64, 64))
        self.button_connect.setObjectName("button_connect")
        self.button_cursor.raise_()
        self.button_en.raise_()
        self.button_in.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.button_next.raise_()
        self.button_continue.raise_()
        self.button_pause.raise_()
        self.button_test.raise_()
        self.canvas.raise_()
        self.button_connect.raise_()
        self.button_design.raise_()
        MainWindow.setCentralWidget(self.centralWidget)

        Ui_MainWindow.retranslateUi(self,MainWindow)    # 此行也被修改
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "简单时间离散神经元模型可视化"))
        self.button_design.setText(_translate("MainWindow", "设计"))
        self.button_test.setText(_translate("MainWindow", "测试"))
        self.label.setText(_translate("MainWindow", "时刻："))
        self.label_2.setText(_translate("MainWindow", "0"))
        self.button_next.setText(_translate("MainWindow", "下一帧"))

import res_rc