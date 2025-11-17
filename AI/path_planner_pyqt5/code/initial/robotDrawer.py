from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QDialog
from robot import Robot

import PyQt5.QtCore

class RobotDrawer:
    def __init__(self, robot, win):
        self.robot = robot
        self.win = win
    
    def draw(self):
        self._draw_body(self.robot.get_body(), Qt.gray)
        self._draw_wheel(self.robot.get_front_wheel(), Qt.black)
        self._draw_wheel(self.robot.get_rear_wheel(), Qt.red)
        # your code
        
    def _draw_body(self, body, color):
        qp = QPainter()
        qp.begin(self.win)

        pen = QPen(color, 2)
        qp.setPen(pen)

        x,y = body.get_pos()
        w,h = body.get_size()
        r = self.robot.get_wheel_size()

        qp.drawRect(x+r, y-h+r, w, h)

        qp.end()

    def _draw_wheel(self, wheel, color):
        qp = QPainter()
        qp.begin(self.win)

        pen = QPen(color, 2)
        qp.setPen(pen)

        xc, yc = wheel.get_center()
        r = wheel.get_radius()

        rect = PyQt5.QtCore.QRect(xc, yc, 2*r, 2*r)
        startAngle = 0
        arcLength = 360*16*r #  https://doc.qt.io/qt-5/qpainter.html#drawArc-1
        # your code
        qp.drawArc(rect, startAngle, arcLength)

        qp.end()