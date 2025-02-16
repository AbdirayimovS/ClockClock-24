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

    Clock shall not have own qthreads. they creates new complexity!
    

    https://www.geeksforgeeks.org/create-analog-clock-using-pyqt5-in-python/
    '''
    def __init__(self, hour=10, minute=30, parent=None):
        super().__init__(parent)
        self.__minute = minute
        self.__hour = hour
        self._previous_minute = minute
        self._previous_hour = hour
        self.percent = 0
        self.delta_second = 0
        self.second_degree = self.delta_second * 6.
        self.minute_degree = 0.
        self.hour_degree = 0. # range [0, 12]
        self.rec = min(self.width(), self.height())
        self.center_x = self.rec // 2
        self.center_y =  self.rec // 2
        self.radius = self.rec - self.center_x
        timer = QTimer(self)
        timer.timeout.connect(self.updateHands)
        timer.start(100)
    
    def updateHands(self):
        # the hour hand is moved only if the minute hand is moved!
        # It means minute hand shall move in order to trigger the hour hand to move 
        self.second_degree += 12 #6  # increase of this number means the speed representation.
        # if current time too far, then the second degree shall be increased, and later it shall be decreased to normal in the end of the reach!
        self.minute_degree += self.second_degree / 60 / 60
        self.hour_degree += self.minute_degree / 30 / 60 / 60

        # shall it be recursive and call itself to continuesly draw
        self.update()

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
        '''
        It is auto called when update() is triggered!
        This is expensive method to run. Because it is run many times.

        TASKS:
            - Draw the circle
            - Draw hour hand (current)
            - Draw minute hand (current)
            - Draw second hand (current)
        
            Drawing the circle depends on the size of widget.

            Hour hand degree depens on minute hand degree and it depens on second degree value.
            Each time when second rotated it forces the minutes to add some value like in a chain rule.
            Therefore, each minute rotation adds some influence to hour to be updated similar to chain rule.

        '''

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        #<<<<<<<Drawing a circle!>>>>>>>>

        painter.setPen(
            QPen(
                QColor(128, 128, 128),  # Color (gray)
                5,
                Qt.SolidLine,
                Qt.RoundCap | Qt.MiterJoin,
                )
            )
        
        painter.drawEllipse(0, 0, self.rec, self.rec)

        ##################################


        #######<DRAWING>######
        painter.setPen(
            QPen(Qt.black,
                 5,
                 Qt.SolidLine,
                 Qt.RoundCap,
                 Qt.RoundJoin
                )
            )
        
        # clean up due to degree values are not cyclic
        if int(self.second_degree) == 360:
            self.second_degree = 0

        if int(self.minute_degree) == 360:
            self.minute_degree = 0
        
        if int(self.hour_degree) == 360:
            self.hour_degree = 0
        
        
        # draw a seconds (optional)
        # What is the independent value -> second_x and second_y
        # minutes are derived from the second_x and second_y
        # hours are derived form minutes and seconds
        #<<<<<<<<<<<<<<TWO WAYS>>>>>>>>>>>>>>>
        # shall we calculate here the decision?
        # Shall we calculate in other place?
        # In order to remain simplicity, lets calculate here for now.
        print(self.second_degree, self.minute_degree, self.hour_degree)

        hours_line_len = self.radius * 0.6
        minute_line_len = self.radius * 0.9
        second_line_len = self.radius * 0.95

        # why we multiple to 30? 360 / 30  = 12. In order to easily classify into twelve points?
        # Is it necessary to move to cos and sin?
        # delta_minute depens on the seconds values
        # in one rotation second has 60 positions. It is same with the minute positions. So it is not a 1, but a 6
        # 1 radian minute consists of 60 radian seconds sum
        # radian_second / 60? # this way is also fine
        # radian minute = math.radians(delta_minute *6 + radian_second)
        # 1 cycle is 360 degree
        # second_degree must be between [0, 6]. Where 0 is start time when second is 0 and 6 is second is 0 but one increment
        
        
        
        radian_second = math.radians(self.second_degree)  # because the second has 360 values?
        radian_minute = math.radians(self.minute_degree)  # + second value influence. It has also in radians influence i bet
        radian_hour = math.radians(self.hour_degree) # + radian_minute_influence. Radian minute is composition of minute and second
        second_x = int(second_line_len * math.sin(radian_second) + self.center_x)
        second_y = int(-1 * second_line_len * math.cos(radian_second) + self.center_y)

        minutes_x = int(minute_line_len * math.sin(radian_minute) + self.center_x)
        minutes_y = int(-1 * minute_line_len * math.cos(radian_minute) + self.center_y)
        hours_x = int(hours_line_len * math.sin(radian_hour) + self.center_x)
        hours_y = int(-1 * hours_line_len * math.cos(radian_hour) + self.center_y)

        painter.drawLine(
            self.center_x, self.center_y,
            second_x, second_y
            )

        painter.drawLine(
            self.center_x, self.center_y,
            minutes_x, minutes_y
            )

        painter.drawLine(
            self.center_x, self.center_y,
            hours_x, hours_y
        )

        super().paintEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    clock = Clock()
    clock.show()
    sys.exit(app.exec_())
