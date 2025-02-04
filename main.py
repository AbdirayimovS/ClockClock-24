'''Clock'''

# https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
# how to automate it?

import os # to overcome relative path issues
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QTime

from source.digit import Digit

basedir = os.path.dirname(__file__)


class MainWindow(QWidget):
    '''
    Main Window
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CLOCK')

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        layout = QHBoxLayout()
        time = QTime.currentTime()
        self.H1 = Digit(value=time.hour() // 10, parent=self)
        self.H2 = Digit(value=time.hour() % 10, parent=self)
        self.M1 = Digit(value=time.second() // 10, parent=self)
        self.M2 = Digit(value=time.second() % 10, parent=self)
        layout.addWidget(self.H1)
        layout.addWidget(self.H2)
        layout.addWidget(self.M1)
        layout.addWidget(self.M2)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def update(self):
        time = QTime.currentTime()
        self.H1.value=time.hour() // 10
        self.H2.value=time.hour() % 10
        self.M1.value=time.minute() // 10
        self.M2.value=time.minute() % 10
        print("Time: ", time)
        super().update()

    def mousePressEvent(self, event):
        ''' When press, maybe animation or etc'''
        if event.button() == Qt.LeftButton:
            self.mpos = event.globalPos() - self.pos()    # 记录坐标
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mpos)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''when release the time goes back to the true time.'''
        if event.button() == Qt.LeftButton:
            print("going back")
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        '''Any event, then add dynamic or etc'''
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
            print("Closed. Add necessary things")
            QApplication.instance().quit()
        super().mouseDoubleClickEvent(event)

if __name__ == '__main__':
    print("Bismillah")
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    widget.resize(550, 300)
    sys.exit(app.exec_())
