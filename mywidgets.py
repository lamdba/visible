
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor

from draw import drawconnects, drawEN, drawIN, PEN, BOUNDINGRECT
from neuron import Neuron, Group, NEURONTYPEEN, NEURONTYPEIN

class ShellAllConnect(QGraphicsItem):####################################尝试解决方案：把所有连接用作一个对象，该对象在底层负责绘制一切连接，并且总是不被选中
    def __init__(self,group):
        super().__init__()
        self.group = group
        self.setPos(QPoint(0,0))

    def boundingRect(self):
        return QRectF(0,0,0,0)

    def paint(self, painter, styleOptionGraphicsItem, widget_widget=None):  # 有意思的是，painter是以其依附对象为原点开始绘制的
        drawconnects(painter, self.group.neurons)


class ShellEN(QGraphicsItem):
    sendact=Neuron.sendact           # 真是没法多继承了！
    receiveact=Neuron.receiveact
    sendback=Neuron.sendback
    receiveback=Neuron.receiveback
    def __init__(self,pos):
        super().__init__()
        self.setPos(pos)
        Neuron.__init__(self,NEURONTYPEEN)

    def boundingRect(self): # overload
        return BOUNDINGRECT

    def paint(self, painter, styleOptionGraphicsItem, widget_widget=None):
        drawEN(painter,self.value)

    def repr(self,group):
        return ("EN" if self.type == NEURONTYPEEN else "IN", (self.x(), self.y()), self.value, [connect.repr(group) for connect in self.connects])


class ShellIN(QGraphicsItem):
    sendact=Neuron.sendact
    receiveact=Neuron.receiveact
    sendback=Neuron.sendback
    receiveback=Neuron.receiveback

    def __init__(self,pos):
        super().__init__()
        self.setPos(pos)
        Neuron.__init__(self,NEURONTYPEIN)

    def boundingRect(self): # overload
        return BOUNDINGRECT

    def paint(self,painter, styleOptionGraphicsItem, widget_widget=None):
        drawIN(painter,self.value)

    def mousePressEvent(self,event):
        pass

    def repr(self,group):
        return ("IN" if self.type == NEURONTYPEEN else "IN", (self.x(), self.y()), self.value, [connect.repr(group) for connect in self.connects])


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
                            connect = Neuron.Connect(10,1,item)
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

