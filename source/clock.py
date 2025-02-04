'''
Clock
=====
'''
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen


class Clock(QWidget):
    '''
    Round. Has background and foreground colors. Has two strikes.

    https://www.geeksforgeeks.org/create-analog-clock-using-pyqt5-in-python/
    '''
    def __init__(self, hour=10, minute=30, parent=None):
        super().__init__(parent)
        self.__minute = minute
        self.__hour = hour
        self._previous_minute = minute
        self._previous_hour = hour
        self.percent = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(5)
        self.update()
        # it is lagging. I think it is because of the QTimer has many. No it is not lagging

    def update(self):
        self.rec = min(self.width(), self.height())
        self.center_x = self.rec // 2
        self.center_y =  self.rec // 2
        self.radius = self.rec - self.center_x
        delta_val = (abs(self.__minute - self._previous_minute)) / 100 * self.percent
        delta_val2 = (abs(self.__hour - self._previous_hour)) / 100 * self.percent
        print("prevous minute + delta value = self.__minute ", self._previous_minute, delta_val, self.__minute)
        print("prevous hour + delta value = self.__hour ", self._previous_hour, delta_val2, self.__hour)
        delta_minute = self._previous_minute + delta_val# new_time - old-time in several steps with k 
        delta_hour = self._previous_hour + delta_val2

        self.percent += 0.3
        # if self.percent >= 1:
        #     delta_minute = self.__minute
        #     delta_hour = self.__hour

        hours_line_len = self.radius * 0.6
        self.hours_x = int(hours_line_len * math.sin(math.radians(delta_hour * 30)) + self.center_x)
        self.hours_y = int(-1 * hours_line_len * math.cos(math.radians(delta_hour * 30)) + self.center_y)

        minute_line_len = self.radius * 0.9
        self.minutes_x = int(minute_line_len * math.sin(math.radians(delta_minute * 6)) + self.center_x)
        self.minutes_y = int(-1 * minute_line_len * math.cos(math.radians(delta_minute * 6)) + self.center_y)

        super().update()

    @property
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, value):
        self._previous_hour = self.__hour
        self.__hour = value

    @property
    def minute(self):
        return self.__minute

    @minute.setter
    def minute(self, value):
        self._previous_minute = self.__minute
        self.__minute = value
        self.percent = 0

    def paintEvent(self, event):
        # this the hand for hour
        # I want it to move faster
        # this is called continuesly! therer it is not a godd idea to draw continuesly here
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(
            QPen(
                QColor(128, 128, 128),  # Color (gray)
                5,
                Qt.SolidLine,
                Qt.RoundCap | Qt.MiterJoin,
                )
            )
        painter.drawEllipse(0, 0, self.rec, self.rec)


        #######<DRAWING>######
        painter.setPen(
            QPen(Qt.black,
                 5,
                 Qt.SolidLine,
                 Qt.RoundCap,
                 Qt.RoundJoin
                )
            )
        painter.drawLine(
            self.center_x, self.center_y,
            self.minutes_x, self.minutes_y
        )
        painter.drawLine(
            self.center_x, self.center_y,
            self.hours_x, self.hours_y
        )
        
        super().paintEvent(event)
