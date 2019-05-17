
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
    def __init__(self,pos, value = False):  # 下一版就把默认False改成强制传入
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

    def __init__(self,pos,value = False):
        super().__init__()
        self.setPos(pos)
        Neuron.__init__(self,NEURONTYPEIN)
        self.value = value

    def boundingRect(self): # overload
        return BOUNDINGRECT

    def paint(self,painter, styleOptionGraphicsItem, widget_widget=None):
        drawIN(painter,self.value)

    def mousePressEvent(self,event):
        pass

    def repr(self,group):
        return ("IN" if self.type == NEURONTYPEEN else "IN", (self.x(), self.y()), self.value, [connect.repr(group) for connect in self.connects])


def group_serialize(group):
    return str([neuron.repr(group) for neuron in group.neurons])


def withpack(connect,actpacks, backpacks):
    connect.actpacks = actpacks
    connect.backpacks = backpacks
    return connect

def group_unserialize(s):   # 返回的不是group，是List[ShellEN/ShellIN]
    l = eval(s)
    neurons = []
    lconnects = []  # 表中存表
    for flag, p, value, connects in l:
        neurons.append((ShellEN if flag == 'EN' else ShellIN)(QPointF(*p),value))
        lconnects.append(connects)
    for neuron, connects in zip(neurons, lconnects):
        neuron.connects = [withpack(Neuron.Connect(k,t,neurons[id]), actpacks, backpacks) for id, k ,t, actpacks, backpacks in connects]
    return neurons


class MyScene(QGraphicsScene):
    def __init__(self,group,d_t):
        super().__init__()
        self.choosed = None
        self._dp = None    # 点击位置和实际点的偏差（move模式寄存用）
        self.connect = None # 创建连接时临时要绘制的连接
        self.setSceneRect(QRectF(0,0,760,700))
        self.group = group  # 初始group
        self.allconnect = ShellAllConnect(group)
        self.addItem(self.allconnect)       # 对象管理同步
        for neuron in group.neurons:
            self.addItem(neuron)

        self.d_t = d_t  # design / test
        self.mod = None # design下的模式

    def evo(self):
        self.group.evo()
        self.update()

    def clear(self):
        for neuron in self.group.neurons:
            neuron.value = False
        self.update()

    def serialize(self,temp = False):
        path = "F:/visible-group.txt" if not temp else "F:/visible-group-temp"
        with open(path, 'w') as f:
            f.write(group_serialize(self.group))

    def unserialize(self,temp = False):
        path = "F:/visible-group.txt" if not temp else "F:/visible-group-temp"
        with open(path, 'r') as f:
            s = f.read()
            neurons = group_unserialize(s)
            self.group.neurons = neurons

            for obj in self.items():    # 用clear根本没用嘛！
                self.removeItem(obj)
            self.addItem(self.allconnect)       # 对象管理同步
            for neuron in neurons:
                self.addItem(neuron)
            self.update()

    def mousePressEvent_move(self,event):   # 为了表驱动
        items = self.items(event.scenePos())
        if items:
            item = items[0]
            self.choosed = item
            self._dp = item.scenePos() - event.scenePos()

    def mousePressEvent_setvalue(self,event):
        items = self.items(event.scenePos())
        if items:
            item = items[0]
            item.value = not item.value
            self.update()

    def mousePressEvent_newen(self,event):
        neuron = ShellEN(event.scenePos())
        self.group.neurons.append(neuron)
        self.addItem(neuron)

    def mousePressEvent_newin(self,event):
        neuron = ShellIN(event.scenePos())
        self.group.neurons.append(neuron)
        self.addItem(neuron)

    def mousePressEvent_connect(self,event):
        items = self.items(event.scenePos())
        if items:
            item = items[0]
            self.choosed = item  # 暂时使用同一个寄存器


    TABLE_mousePressEvent = [mousePressEvent_move, mousePressEvent_setvalue,
        mousePressEvent_newen, mousePressEvent_newin, mousePressEvent_connect]

    def mousePressEvent(self,event):
        self.TABLE_mousePressEvent[self.mod](self,event)    # 注意是向类方法传参


    def mouseMoveEvent_move(self,event):   # 未使用表驱动
        if self.choosed:
            self.choosed.setPos(event.scenePos()+self._dp)
            self.update()

    def mouseMoveEvent_connect(self,event):
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


    def mouseMoveEvent(self,event):
        mod = self.mod
        if mod == 0:
            self.mouseMoveEvent_move(event)
        elif mod == 4:
            self.mouseMoveEvent_connect(event)


    def mouseReleaseEvent(self, event):  # 也未使用表驱动
        mod = self.mod
        if mod == 0:    # move
            self.choosed = None
            self._dp = None
        elif mod == 4:  # connect
            if self.choosed is not None:
                l = self.choosed.connects
                if l and hasattr(l[-1],"temp"):
                    delattr(l[-1],"temp")
                self.choosed = None


class MyView(QGraphicsView):
    def __init__(self,parent):
        super().__init__(parent)
        self.setFixedSize(760, 700)
        self.setSceneRect(0, 0, 750, 690)
        self.setBackgroundBrush(QColor.fromRgb(48,48,48))

