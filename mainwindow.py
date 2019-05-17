from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from Ui_mainwindow import Ui_MainWindow
from myevents import E

from neuron import Neuron, Group, NEURONTYPEEN, NEURONTYPEIN   # 仅供测试
from mywidgets import ShellEN, ShellIN, ShellAllConnect, MyScene, MyView

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Ui_MainWindow.setupUi(self,self)

        # model/state(scene)
        n1 = ShellEN(QPoint(200,200))
        n2 = ShellIN(QPoint(300,400))
        n1.connects.append(Neuron.Connect(10,1,n2))
        group = Group([n1,n2])
        #~ s = group.serialize()
        #~ print(Group.unserialize(s))
        self.scene = MyScene(group,True)

        self.button_design.hide()
        self.button_pause.hide()
        self.mod = None # 统一初始化，是个麻烦的问题




        self.d_or_t = 0 # design
        self.canvas.setScene(self.scene)

        self.t = 0

        self.toolbar = self.addToolBar('mytoolbar')
        self.toolbar.setMovable(False)

        serializeAction = QAction( '&储存', self)  # QAction放哪都诡异
        serializeAction.setShortcut('Ctrl+S')
        serializeAction.setStatusTip('Serialize application')
        self.toolbar.addAction(serializeAction)

        serializeAction.triggered.connect(self.scene.serialize)


        unserializeAction = QAction( '&读取', self)
        unserializeAction.setShortcut('Ctrl+O')
        unserializeAction.setStatusTip('Unserialize application')
        unserializeAction.triggered.connect(self.scene.unserialize)
        self.toolbar.addAction(unserializeAction)


        self.label.hide()       # 这些按钮是首屏不显示的
        self.label_2.hide()
        self.button_next.hide()
        self.button_continue.hide()

        self.choose_button(0)

    def choose_button(self,n):
        assert n in [0,1,2,3,4]
        self.mod = n
        self.scene.mod = n
        for i,button in enumerate([self.button_cursor,self.button_set,self.button_en,self.button_in,self.button_connect]):
            button.setDown(bool(i == n))

    on_button_design_clicked   = E.on_button_design_clicked
    on_button_test_clicked     = E.on_button_test_clicked
    on_button_cursor_clicked   = E.on_button_cursor_clicked
    on_button_set_clicked     = E.on_button_set_clicked
    on_button_en_clicked       = E.on_button_en_clicked
    on_button_in_clicked       = E.on_button_in_clicked
    on_button_connect_clicked  = E.on_button_connect_clicked
    on_button_continue_clicked = E.on_button_continue_clicked
    on_button_pause_clicked    = E.on_button_pause_clicked
    on_button_next_clicked     = E.on_button_next_clicked


