'''
Digit
=====

'''
from typing import List

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QTimer

from source.clock import Clock

class Digit(QWidget):
    '''
    Digit has 6 clocks.

    '''
    MAPPING_DICT = {
            0: [
                [(6, 15), (6, 45)],  # [(hh, mm), (hh, mm)]
                [(6, 00), (6, 00)],
                [(3, 00), (9, 00)]
            ],
            1: [
                [(00, 00), (6, 30)],
                [(1, 5), (6, 00)],
                [(00, 00), (12, 00)]
            ],
            2: [
                [(3, 15), (9, 30)],
                [(6, 15), (0, 45)],
                [(00, 15), (9, 45)]
            ],
            3: [
                [(3, 15), (9, 30)],
                [(3, 15), (9, 00)],
                [(3, 15), (9, 00)]
            ],
            4: [
                [(6, 30), (6, 30)],
                [(00, 15), (6, 00)],
                [(7, 35), (12, 00)]
            ],
            5: [
                [(6, 15), (9, 45)],
                [(12, 15), (6, 45)],
                [(3, 15), (12, 45)]
            ],
            6: [
                [(6, 15), (9, 45)],
                [(6, 00), (6, 45)],
                [(12, 15), (9, 00)]
            ],
            7: [
                [(3, 15), (6, 45)],
                [(7, 35), (6, 00)],
                [(7, 35), (12, 00)]
            ],
            8: [
                [(6, 15), (6, 45)],
                [(12, 15), (12, 45)],
                [(3, 00), (9, 00)]
            ],
            9: [
                [(6, 15), (6, 45)],
                [(12, 15), (6, 00)],
                [(3, 15), (9, 00)]
            ],
        }
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.__value = value
        self._clocks:List[Clock] = []
        layout = QGridLayout()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)
        # self.timer.start(500)

        val = self.MAPPING_DICT[self.__value]
        for idx, (clock1, clock2) in enumerate(val):
            clock1 = Clock(hour=clock1[0], minute=clock1[1], parent=self)
            clock2 = Clock(hour=clock2[0], minute=clock2[1], parent=self)
            self._clocks.append([clock1, clock2])
            row = idx
            layout.addWidget(clock1, row, 0)
            layout.addWidget(clock2, row, 1)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        # if value != self.__value:
        val = self.MAPPING_DICT[value]
        for clocks, tuple_times in zip(self._clocks, val):
            for clock, tuple_time in zip(clocks, tuple_times):
                clock.hour = tuple_time[0]
                clock.minute = tuple_time[1]

        self.__value = value

    def update(self):
        print("Updating! Digit")
        super().update()
