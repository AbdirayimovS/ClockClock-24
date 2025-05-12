'''Clock'''

# https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
# how to automate it?

import os # to overcome relative path issues
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QGraphicsView
from PyQt5.QtCore import Qt, QTimer, QTime, QRectF
from source.four_digit_scene import FourDigitScene

basedir = os.path.dirname(__file__)


 
class MainWindow(QWidget):
    '''
    Main Window
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CLOCK')
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.layout = QHBoxLayout()
        CLOCK_SIZE_PX = 50
        CLOCK_BOUNDARY_OFFSET = 2
        width = (CLOCK_BOUNDARY_OFFSET + CLOCK_SIZE_PX)*8
        height = (CLOCK_BOUNDARY_OFFSET + CLOCK_SIZE_PX) * 3
        rect = QRectF(0, 0, width, height)
        scene = FourDigitScene(rect, mode=2, clock_size_px=CLOCK_SIZE_PX, clock_boundary_offset=CLOCK_BOUNDARY_OFFSET)
        self.timer = QTimer(self)
        self.timer.timeout.connect(scene.advance)
        self.timer.start(16)
        self.view = QGraphicsView(scene)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.NoFrame)
        self.view.setStyleSheet("background: transparent; border: none;")
        self.view.setAttribute(Qt.WA_TranslucentBackground)
        self.view.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.view.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.view.setFrameRect(rect.toRect())

    def mousePressEvent(self, event):
        ''' When press, maybe animation or etc'''
        if event.button() == Qt.LeftButton:
            self.mpos = event.globalPos() - self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mpos)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''when release the time goes back to the true time.'''
        print("Mouse release event")
        if event.button() == Qt.LeftButton:
            print("going back")
        super().mouseReleaseEvent(event)

    # def mouseDoubleClickEvent(self, event):
    #     if event.button() == Qt.RightButton:
    #         self.close()
    #         print("Closed. Add necessary things")
    #         QApplication.instance().quit()
    #     super().mouseDoubleClickEvent(event)

if __name__ == '__main__':
    print("Bismillah")
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
