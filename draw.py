from cmath import tau, exp
from math import sqrt
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF

R = 15
DELTA = QPointF(R,R)
O = QPointF(0,0)
ORECT = QRectF(0,0,0,0)
BOUNDINGRECT = QRectF(-DELTA, DELTA)


ARROWR = 3  # 实际长度会将此值乘上根号5

def drawarrow(painter, begin, end):
    painter.drawLine(begin,end)
    p3 = (begin+end*2)/3
    dp = end - begin
    a, b = dp.x(), dp.y()
    c = sqrt(a**2+b**2)
    dy1, dx1 = (2*b-a)/c, (2*a+b)/c
    dy2, dx2 = (2*b+a)/c, (2*a-b)/c
    painter.drawLine(p3-QPointF(dx1,dy1)*ARROWR,p3)
    painter.drawLine(p3-QPointF(dx2,dy2)*ARROWR,p3)

def drawconnects(painter, neurons):
    painter.setPen(PEN)
    for neuron in neurons:
        begin = neuron.scenePos()
        for connect in neuron.connects:
            end = connect.to.scenePos()
            drawarrow(painter,begin, end)

def drawoneconnect(painter, n1, n2):
    painter.setPen(PEN)
    drawarrow(painter,n1.scenePos(), n2.scenePos())

FBRUSH = QBrush(QColor.fromRgb(48,48,48))
TBRUSH = QBrush(QColor.fromRgb(255,255,255))
#~ brush_true = QBrush(QColor.fromRgb(208,208,208))
PEN = QPen(QColor.fromRgb(255,255,255))
PEN.setWidth(1)


def drawEN(painter,state):
    painter.setPen(PEN)
    painter.setBrush(TBRUSH if state else FBRUSH)
    painter.drawEllipse(QRectF(-DELTA,DELTA))

def t(z):
    return QPointF(z.real,z.imag)
PENTAGONPOINTS = [t(R*exp(1j*(i*tau/5-tau/4))) for i in range(5)]
def drawIN(painter,state):
    painter.setPen(PEN)
    painter.setBrush(TBRUSH if state else FBRUSH)
    painter.drawPolygon(*PENTAGONPOINTS)
