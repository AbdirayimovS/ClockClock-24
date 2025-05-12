'''
Clock
=====
'''
import math
import datetime

from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF, QSizeF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QGradient, QLinearGradient, QRadialGradient, QConicalGradient

####### PARAMS ########
PEN_WIDTH = 3

SECOND_HAND_PEN = QPen(
    Qt.red,
    PEN_WIDTH,
    Qt.SolidLine,
    Qt.RoundCap,
    Qt.RoundJoin
    )

MINUTE_HAND_PEN = QPen(
    Qt.white,
    PEN_WIDTH,
    Qt.SolidLine,
    Qt.RoundCap,
    Qt.RoundJoin
    )

HOUR_HAND_PEN = QPen(
    Qt.white,
    PEN_WIDTH,
    Qt.SolidLine,
    Qt.RoundCap,
    Qt.RoundJoin
    )


class GraphicsClock(QGraphicsItem):
    def __init__(self, hour:int, minute:int, second=0, mode:int=1, ax=0, ay=0, size=100):
        '''
        Perform as clock!

        Args:
        -----
            - mode (int): 1 --> classical analog clock
                          2 --> display the time of hour and minute
        '''
        super().__init__()
        assert mode in [1, 2]
        self.mode = mode
        self.HOUR_HAND_PEN = HOUR_HAND_PEN
        self.MINUTE_HAND_PEN = MINUTE_HAND_PEN
        
        self.second_degree = second * 6  # 360 / 60
        self.minute_degree = minute * 6 + second * 0.1  # 6° per minute + smooth
        self.hour_degree = (hour % 12) * 30 + minute * 0.5  # 30° per hour + smooth
        
        self.second_degree = 0
        self.minute_degree = 0
        self.hour_degree = 0

        self.rec = size
        self.center_x = self.rec // 2
        self.center_y =  self.rec // 2
        self.radius = self.rec - self.center_x

        self.hours_line_len = self.radius * 0.6
        self.minute_line_len = self.radius * 0.9
        self.second_line_len = self.radius * 0.95
        self.ax = ax
        self.ay = ay
        self.setPos(QPointF(ax, ay))

    # def boundingRect(self):
    # ISSUE HERE: Does not work well!
    # #     # print(self.ax - PEN_WIDTH, self.ay - PEN_WIDTH, self.rec + PEN_WIDTH, self.rec + PEN_WIDTH)
    # #     # return QRectF(self.ax - PEN_WIDTH, self.ay - PEN_WIDTH, self.rec + PEN_WIDTH, self.rec + PEN_WIDTH)
    #     return QRectF(self.ax, self.ay, 1000, self.rec+self.ay)

    def paint(self, painter, option, widget = ...):
        painter.setRenderHint(QPainter.Antialiasing)
        #<<<<<<<Drawing a circle!>>>>>>>>
        # Gradient: https://www.bogotobogo.com/Qt/Qt5_QLinear_QRadial_QConical_QGradient.php
        brush = QBrush(QColor(0, 0, 255))  # create a gradient brush
        # linear gradient
        # gradient = QLinearGradient(0, 0, 400, 0)
        # gradient.setColorAt(0.0, QColor(0, 0, 255))  # blue at the top 
        # gradient.setColorAt(1.0, QColor(60, 60, 180))  # dark blue at the 

        # <<<<<QRadialGradient>>>>>>
        gradient = QRadialGradient(self.center_x, self.center_y, self.center_x) 
        gradient.setColorAt(0.0, QColor(0, 30, 255))  # blue at the top 
        gradient.setColorAt(1.0, QColor(60, 60, 180))  # dark blue at the 
        ##################################

        #<<<<<<<<<QConuqualGradient>>>>>>>
        # gradient = QConicalGradient(200, 50, 250)
        # gradient.setColorAt(0.0, QColor(0, 0, 255))  # blue at the top 
        # gradient.setColorAt(1.0, QColor(60, 60, 180))  # dark blue at the 

        #############################
        brush = QBrush(gradient)
        painter.setBrush(brush)
        
        painter.drawEllipse(0, 0, self.rec, self.rec)

        ##################################
        #######<DRAWING>#####
        # clean up due to degree values are not cyclic
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
        second_x = int(self.second_line_len * math.sin(radian_second) + self.center_x)
        second_y = int(-1 * self.second_line_len * math.cos(radian_second) + self.center_y)

        minutes_x = int(self.minute_line_len * math.sin(radian_minute) + self.center_x)
        minutes_y = int(-1 * self.minute_line_len * math.cos(radian_minute) + self.center_y)
        hours_x = int(self.hours_line_len * math.sin(radian_hour) + self.center_x)
        hours_y = int(-1 * self.hours_line_len * math.cos(radian_hour) + self.center_y)

        # painter.setPen(self.SECOND_HAND_PEN)
        # painter.drawLine(
        #     self.center_x, self.center_y,
        #     second_x, second_y
        #     )
        painter.setPen(self.MINUTE_HAND_PEN)
        painter.drawLine(
            self.center_x, self.center_y,
            minutes_x, minutes_y
            )
        painter.setPen(self.HOUR_HAND_PEN)
        painter.drawLine(
            self.center_x, self.center_y,
            hours_x, hours_y
        )
    
    def advance(self, hour=None, minute=None):
        # if we tell hour and minute --> Immideately set to that hour and minure
        # we can tell just to increment the existsing clock

        # update the drawings
        # update the hands of the clock
        #------------------------------
        if self.mode == 1: # classic clock
            #----------------------------
            now = datetime.datetime.now()
            self.second_degree = now.second * 6  # 360 / 60
            self.minute_degree = now.minute * 6 + now.second * 0.1  # 6° per minute + smooth
            self.hour_degree = (now.hour % 12) * 30 + now.minute * 0.5  # 30° per hour + smooth
            #------------------------------
        elif self.mode == 2:
            #------------------------------
            assert minute != None
            assert hour != None

            self.second_degree = 0  # 360 / 60
            self.minute_degree = minute * 6  #+ second * 0.1  # 6° per minute + smooth
            self.hour_degree = (hour % 12) * 30  #+ minute * 0.5  # 30° per hour + smooth
            #------------------------------
            # speed how to interpretate the speed? the move big movement is bigger speed, small movement is small speed
            # self.minute_degree --> current
            # future_minute_degree --> ?
            # so speed then can be measured
        self.update()



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView

    app = QApplication(sys.argv)
    #########################################
    clock_item = GraphicsClock(1, 1, 0, 1)
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 100, 100)
    scene.addItem(clock_item)
    view = QGraphicsView(scene)
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setFrameShape(QGraphicsView.NoFrame)
    view.setContentsMargins(0, 0, 0, 0)
    view.setAttribute(Qt.WA_TranslucentBackground)
    # view.setFixedSize(100, 100)
    timer = QTimer()
    timer.timeout.connect(clock_item.advance)
    timer.start(32)
    view.show()
    #########################################
   

    sys.exit(app.exec_())
