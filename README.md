几个文件的依赖关系：


## neuron.py
```python
```

## draw.py
```python
from cmath import tau, exp
from math import sqrt
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
```

## mywidgets.py
```python
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor

from draw import drawconnects, drawEN, drawIN, PEN, BOUNDINGRECT
from neuron import Neuron, Group, NEURONTYPEEN, NEURONTYPEIN
```

## myevents.py
```python
from PyQt5.QtCore import pyqtSlot
```

## UI_mainwindow.py
```python
from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import MyView
```

## mainwindow.py
```python
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from UI_mainwindow import Ui_MainWindow
from myevents import E

from neuron import Neuron, Group, NEURONTYPEEN, NEURONTYPEIN   # 仅供测试
from mywidgets import ShellEN, ShellIN, ShellAllConnect, MyScene, MyView
```

## main.py
```python
from mainwindow import MyMainWindow
from PyQt5.QtWidgets import QApplication
from sys import argv
```




