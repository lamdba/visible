from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from UI_mainwindow import Ui_MainWindow
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
        self.choose_button_state = None # 统一初始化，是个麻烦的问题
        self.choose_button(0)



        self.d_or_t = 0 # design
        self.canvas.setScene(self.scene)

        self.t = 0


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


    def choose_button(self,n):
        assert n in [0,1,2,3]
        self.choose_button_state = n
        self.scene.mod = n
        for i,button in enumerate([self.button_cursor,self.button_en,self.button_in,self.button_connect]):
            button.setDown(bool(i == n))

    on_button_design_clicked   = E.on_button_design_clicked
    on_button_test_clicked     = E.on_button_test_clicked
    on_button_cursor_clicked   = E.on_button_cursor_clicked
    on_button_en_clicked       = E.on_button_en_clicked
    on_button_in_clicked       = E.on_button_in_clicked
    on_button_connect_clicked  = E.on_button_connect_clicked
    on_button_continue_clicked = E.on_button_continue_clicked
    on_button_pause_clicked    = E.on_button_pause_clicked
    on_button_next_clicked     = E.on_button_next_clicked


