
#宁可共用代码也不使用继承

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import res_rc
import neuron
import cmath,math



R = 15
DELTA = QPoint(R,R)
O = QPointF(0,0)
ARROWR = 3  # 实际长度将会乘上根号5
def drawarrow(painter, begin, end):
    painter.drawLine(begin,end)
    p3 = (begin+end*2)/3
    dp = end - begin
    a, b = dp.x(), dp.y()
    c = math.sqrt(a**2+b**2)
    dy1, dx1 = (2*b-a)/c, (2*a+b)/c
    dy2, dx2 = (2*b+a)/c, (2*a-b)/c
    painter.drawLine(p3-QPointF(dx1,dy1)*ARROWR,p3)
    painter.drawLine(p3-QPointF(dx2,dy2)*ARROWR,p3)

class ShellAllConnect(QGraphicsItem):####################################尝试解决方案：把所有连接用作一个对象，该对象在底层负责绘制一切连接，并且总是不被选中
    pen = QPen(QColor.fromRgb(255,255,255))
    def __init__(self,group):
        super().__init__()
        self.group = group
        self.setPos(QPoint(0,0))

    def boundingRect(self):
        return QRectF(10,0,0,0)

    def paint(self, painter, styleOptionGraphicsItem, widget_widget=None):  # 有意思的是，painter是以其依附对象为原点开始绘制的
        painter.setPen(self.pen)
        for neuron in self.group.neurons:
            begin = neuron.scenePos()
            for connect in neuron.connects:
                end = connect.to.scenePos()
                drawarrow(painter,begin, end)

class ShellNeuron(QGraphicsItem):  #,neuron.Neuron
    brush_false = QBrush(QColor.fromRgb(48,48,48))
    brush_true = QBrush(QColor.fromRgb(255,255,255))
    #~ brush_true = QBrush(QColor.fromRgb(208,208,208))
    pen = QPen(QColor.fromRgb(255,255,255))
    pen.setWidth(1)

    def __init__(self,pos):
        assert type(self) is not ShellNeuron, "abstract class/less code"

        QGraphicsItem.__init__(self)    # 又要继承类方法，又要继承实例成员
        self.setPos(pos)
        #self.setFlags(QGraphicsItem.ItemIsMovable)  # 奇迹

    def boundingRect(self): # overload
        return QRectF(-DELTA,DELTA)

    def paint(self, painter, styleOptionGraphicsItem, widget_widget=None):  # 有意思的是，painter是以其依附对象为原点开始绘制的
        painter.setPen(self.pen)
        #drawself
        painter.setBrush(self.brush_true if self.value else self.brush_false)
        self.different_paint(painter)






class ShellEN(ShellNeuron):
    sendact=neuron.Neuron.sendact           # 真是没法多继承了！
    receiveact=neuron.Neuron.receiveact
    sendback=neuron.Neuron.sendback
    receiveback=neuron.Neuron.receiveback
    def __init__(self,pos):
        ShellNeuron.__init__(self,pos)
        neuron.Neuron.__init__(self,neuron.NEURONTYPEEN)


    def different_paint(self, painter):
        painter.drawEllipse(QRectF(-DELTA,DELTA))


def t(z):
    return QPointF(z.real,z.imag)
class ShellIN(ShellNeuron):
    sendact=neuron.Neuron.sendact
    receiveact=neuron.Neuron.receiveact
    sendback=neuron.Neuron.sendback
    receiveback=neuron.Neuron.receiveback

    points = [t(R*cmath.exp(1j*(i*cmath.tau/5-cmath.tau/4))) for i in range(5)]

    def __init__(self,pos):
        ShellNeuron.__init__(self,pos)
        neuron.Neuron.__init__(self,neuron.NEURONTYPEIN)


    def different_paint(self,QPainter):
         QPainter.drawPolygon(*self.points)
        #QPainter.drawLine(QLine(QPoint(100,200),QPoint(300,400)))   # 碰撞框内的才会刷新（橡皮擦效应）

    def mousePressEvent(self,event):
        pass


class MyScene(QGraphicsScene):
    def __init__(self,group):
        super().__init__()
        self.choosed = None
        self._dp = None    # 点击位置和实际点的偏差
        self.connect = None # 创建连接时临时要绘制的连接
        self.setSceneRect(QRectF(0,0,760,700))
        self.group = group
        self.addItem(ShellAllConnect(group))
        for neuron in group.neurons:
            self.addItem(neuron)

        self.master = None

    def mousePressEvent(self,event):
        if self.master.d_or_t == 0: # design
            flag = self.master.choose_button_state
            if flag == 0:
                self.master.choose_button(0)    # 应对一个bug（不当有用）
                items = self.items(event.scenePos())
                if items:
                    item = items[0]
                    self.choosed = item
                    self._dp = item.scenePos() - event.scenePos()
            elif flag == 1:
                neuron = ShellEN(event.scenePos())
                self.group.neurons.append(neuron)
                self.addItem(neuron)
            elif flag == 2:
                neuron = ShellIN(event.scenePos())
                self.group.neurons.append(neuron)
                self.addItem(neuron)
            elif flag == 3:
                items = self.items(event.scenePos())
                if items:
                    item = items[0]
                    self.choosed = item  # 暂时使用同一个寄存器
        else:
            items = self.items(event.scenePos())
            if items:
                item = items[0]
                item.value = not item.value
                self.update()



    def mouseMoveEvent(self,event):     # 下一次可以通过父组件来分配，以避开master
        if self.master.d_or_t == 0: # design
            flag = self.master.choose_button_state
            if flag == 0:
                if self.choosed:
                    self.choosed.setPos(event.scenePos()+self._dp)
                    self.update()
            elif flag == 3:
                if self.choosed:
                    items = self.items(event.scenePos())
                    l = self.choosed.connects
                    if items:
                        item = items[0]
                        if l and hasattr(l[-1],"temp"): # 已经有一个临时连接
                            pass
                        elif item is self.choosed:
                            pass
                        else:
                            connect = neuron.Neuron.Connect(10,1,item)
                            connect.temp = True # 添加一个属性作为标记
                            l.append(connect)
                            self.update()
                    else:
                        if (l and hasattr(l[-1],"temp")):
                            l.pop()
                            self.update()
        else:   # design
            pass



    def mouseReleaseEvent(self, event):
        if self.master.d_or_t == 0: # design
            flag = self.master.choose_button_state
            if flag == 0:
                self.choosed = None
                self._dp = None
            elif flag == 3:
                if self.choosed is not None:
                    l = self.choosed.connects
                    if l and hasattr(l[-1],"temp"):
                        delattr(l[-1],"temp")
                    self.choosed = None
        else:
            pass


class MyView(QGraphicsView):
    def __init__(self,parent):
        super().__init__(parent)
        self.setFixedSize(760, 700)
        self.setSceneRect(0, 0, 750, 690)
        self.setBackgroundBrush(QColor.fromRgb(48,48,48))


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.button_design.hide()
        self.button_pause.hide()


        n1 = ShellEN(QPoint(200,200))
        n2 = ShellIN(QPoint(300,400))
        n1.connects.append(neuron.Neuron.Connect(10,1,n2))
        self.group = neuron.Group([n1,n2])
        self.scene = MyScene(self.group)
        self.scene.master = self
        self.choose_button(0)

        self.d_or_t = 0 # design
        self.canvas.setScene(self.scene)

        self.t = 0



    @pyqtSlot()
    def on_button_design_clicked(self):
        self.button_design.hide()
        self.button_test.show()
        self.choose_button(0)

        self.t = 0
        self.label_2.setText(str(0))

        for neuron in self.group.neurons:
            neuron.value = False
        self.scene.update()

        self.d_or_t = 0


    @pyqtSlot()
    def on_button_test_clicked(self):
        self.button_test.hide()
        self.button_design.show()
        self.d_or_t = 1

    def choose_button(self,n):
        assert n in [0,1,2,3]
        self.choose_button_state = n
        for i,button in enumerate([self.button_cursor,self.button_en,self.button_in,self.button_connect]):
            if i == n:
                button.setDown(True)
            else:
                button.setDown(False)

    @pyqtSlot()
    def on_button_cursor_clicked(self):
        self.choose_button(0)

    @pyqtSlot()
    def on_button_en_clicked(self):
        self.choose_button(1)

    @pyqtSlot()
    def on_button_in_clicked(self):
        self.choose_button(2)

    @pyqtSlot()
    def on_button_connect_clicked(self):
        self.choose_button(3)

    @pyqtSlot()
    def on_button_continue_clicked(self):
        self.button_continue.hide()
        self.button_next.hide()
        self.button_pause.show()

    @pyqtSlot()
    def on_button_pause_clicked(self):
        self.button_pause.hide()
        self.button_continue.show()
        self.button_next.show()

    @pyqtSlot()
    def on_button_next_clicked(self):
        self.group.evo()
        self.scene.update()
        self.t += 1
        self.label_2.setText(str(self.t))

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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "简单时间离散神经元模型可视化"))
        self.button_design.setText(_translate("MainWindow", "设计"))
        self.button_test.setText(_translate("MainWindow", "测试"))
        self.label.setText(_translate("MainWindow", "时刻："))
        self.label_2.setText(_translate("MainWindow", "0"))
        self.button_next.setText(_translate("MainWindow", "下一帧"))



app = QApplication(sys.argv)
window = MyMainWindow()
window.show()
sys.exit(app.exec_())
