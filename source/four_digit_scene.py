'''
Total number of clocks --> 24 clocks
Format: 
------
    OO OO OO OO 
    OO OO OO OO 
    OO OO OO OO 

Items: HH:MM

'''

import datetime
from typing import List


from PyQt5.QtWidgets import  QGraphicsScene
from PyQt5.QtCore import QRectF
from source.clock import GraphicsClock
from source.utils import DIGIT_MAPPING_DICT


class FourDigitScene(QGraphicsScene):
    def __init__(self, rect:QRectF, mode=2, clock_size_px=50, clock_boundary_offset=2):
        super().__init__()
        self.setSceneRect(rect)
        self.call_step = 0 
        self.hour_hand = 0
        self.minute_hand = 0
        self.h1_face_digit = 0
        self.h2_face_digit = 0
        self.m1_face_digit = 0
        self.m2_face_digit = 0
 
        clock_x_boundary = clock_size_px + clock_boundary_offset
        clock_y_boundary = clock_size_px + clock_boundary_offset

        ###### H1 DIGIT ########
        def __make_digit(digit_face_num:int, global_ax, global_ay) -> List:
            clocks = []
            val = DIGIT_MAPPING_DICT[digit_face_num]
            for idx, (hour, minute) in enumerate(val):
                # 0,1,2,3,4,5,6
                ax1 = global_ax + idx % 2 * clock_x_boundary
                ay = global_ay + idx // 2 * clock_y_boundary 
                clock_item = GraphicsClock(hour, minute, mode=mode, ax=ax1, ay=ay, size=clock_size_px)
                self.addItem(clock_item)
                clocks.append(clock_item)
            return clocks
        ##########################
        self.H1_clocks = __make_digit(0, 0, 0)
        self.H2_clocks = __make_digit(1, clock_x_boundary*2, 0)
        self.M1_clocks = __make_digit(1, clock_x_boundary*4, 0)
        self.M2_clocks = __make_digit(1, clock_x_boundary*6, 0)

        self.clocks = [
            self.H1_clocks, 
            self.H2_clocks, self.M1_clocks, self.M2_clocks,
            ]
        
        # helpers
        # text_item = self.addText("0, 0")
        # text_item.setPos(0, 0)

        # text_item = self.addText("400, 400")
        # text_item.setPos(400, 400)
        
    def advance(self):
        # call each 16 ms!
        # 1 minute is 60 seconds
        # 1 second is 1000 ms
        # for each change of minute I have 60_000 ms
        # advance() is called 62.5 times in one second
        # advance() is called 3750 times in one minute
        #
        #
        #
        # Event 1: Display current time for x milliseconds
        # Actions from Event 1 -> Event 2
        # Actions from Event 2 --> Event 1
        # Event 2: Display circles in circles for x milliseconds: 
        #                                       Curve1 Curve2 Curve3 Curve4 Mirror_Curve4 Mirror_Curve3 Mirror_Curve2 Mirror_Curve1
        #                                       Curve5 Curve6 Curve7 Curve8 Mirror_Curve8 Mirror_Curve7 Mirror_Curve6 Mirror_Curve5
        #                                       Curve9 Curve10 Curve11 Curve12 Mirror_Curve12 Mirror_Curve11 Mirror_Curve10 Mirror_Curve9
        # Event 3: Display clocks where every hour hand and minute hand are in one line
        # Event 4: Display clocks where every hour hand and minute hand are in one line
        now = datetime.datetime.now()
        second = now.second
        if second == 00 or self.call_step == 3750:
            self.call_step = 0 
            self.hour_hand = 0
            self.minute_hand = 0
            print("self.call_step is set 0")
            return
        
        # Event 1 ##########
        # display for 240 ms --> 15 steps
        if 0 <= self.call_step < 15:
            # here draw once and no drawing!
            self.h1_face_digit = int(str(now.hour)[0]) if len(str(now.hour)) > 1 else 0
            self.h2_face_digit = int(str(now.hour)[-1])
            self.m1_face_digit = int(str(now.minute)[0]) if len(str(now.minute)) > 1 else 0
            self.m2_face_digit = int(str(now.minute)[-1])
            for clocks, face_digit in zip(self.clocks, [self.h1_face_digit, self.h2_face_digit, self.m1_face_digit, self.m2_face_digit]):
                for clock, (hour, minute) in zip(clocks, DIGIT_MAPPING_DICT[face_digit]):
                    clock.advance(hour, minute)
        
        elif 15 <= self.call_step < 1015:
            print("moving from Event 1 to Event 2")
            # moving from Event 1 to Event 2
            # change the clock mode?
            for digit_clock in self.clocks:
                for clock in digit_clock:
                    clock.minute_degree += 1
                    clock.hour_degree += 1
                    clock.advance()


            # for digit_clock in self.clocks:
            #     for clock in digit_clock:
            #         self.hour_hand += 1
            #         self.minute_hand += 0.1
            #         if self.hour_hand == 12: self.hour_hand = 0
            #         if self.minute_hand == 60: self.minute_hand = 0
            #         # [upper left, upper right, middle left, middle right, bottom left, bottom right]
            #         clock.advance(self.hour_hand, self.minute_hand, strick=False) # let each one to move in such way 

        elif 1015 <= self.call_step < 2015:
            # moving from Event 1 to Event 2
            # change the clock mode?
            print("moving from Event 2 to Event 1")

            for digit_clock in self.clocks:
                for clock in digit_clock:
                    clock.minute_degree -= 1
                    clock.hour_degree -= 1
                    clock.advance()
                    # self.hour_hand -= 1
                    # self.minute_hand -= 0.1
                    # if self.hour_hand == 12: self.hour_hand = 0
                    # if self.minute_hand == 60: self.minute_hand = 0
                    # # [upper left, upper right, middle left, middle right, bottom left, bottom right]
                    # clock.advance(self.hour_hand, self.minute_hand, strick=False) # let each one to move in such way 
        
        self.call_step += 1
