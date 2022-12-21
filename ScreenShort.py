# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPen, QPixmap, QPainter, QColor
import os
from pathlib import Path
from PyQt5.QtGui import QPainter, QColor, QCursor 
import subprocess
from datetime import datetime
from datetime import date
# import Main
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


class OCR_app(QWidget):
    def __init__(self):
        super().__init__()
        self.screen = QApplication.primaryScreen()
        size = self.screen.size()
        self.window_width, self.window_height = size.width(), size.height()
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.2)
        self.setGeometry(0, 0, self.window_width, self.window_height)
	
        self.setGeometry(0, 0, 4000, 4000)
        self.forOcr = False
        pixmap = QPixmap(".//Uis//Imgs//Cursor2.png")
        cursor = QCursor(pixmap, 15, 15)
        QApplication.setOverrideCursor(cursor)

        self.setStyleSheet('background-color: rgb(3, 134, 255);')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.begin = QPoint()	
        self.destination = QPoint()

        self.start_X_Point = 0
        self.start_Y_Point = 0

        self.end_X_Point = 0
        self.end_Y_Point = 0

        self.endPoint = 0

        # self.screen_resolutions()

    def Show_self(self):
        self.show()
    def screen_resolutions(self):
        for displayNr in range(QDesktopWidget().screenCount()):
            sizeObject = QDesktopWidget().screenGeometry(displayNr)
            print("Display: " + str(displayNr) + " Screen size : " + str(sizeObject.height()) + "x" + str(sizeObject.width()))
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # painter.setOpacity(0.5) # Added
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        rect = QRect(self.start_X_Point, self.start_Y_Point, (self.end_X_Point-self.start_X_Point), (self.end_Y_Point-self.start_Y_Point))

        painter.fillRect(rect, QColor(0,0,0,0))
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))     
        painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()
            self.start_X_Point = self.begin.x()
            self.start_Y_Point = self.begin.y()
            # print(f'self.start_X_Point:{self.start_X_Point}, self.start_Y_Point:{self.start_Y_Point}')
            # print(f'{self.destination.x()} {self.destination.y()}')

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            self.update()
            
            self.end_X_Point = self.destination.x()
            self.end_Y_Point = self.destination.y()


    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            
            # self.main_window_class = Main.Ui()
            # self.main_window_class.hide()

            rect = QRect(self.begin, self.destination)
            painter = QPainter(self)

            painter.drawRect(rect.normalized())
            
            self.setWindowOpacity(0)
            pixmap = QPixmap(".//Imgs//Cursor.png")
            cursor = QCursor(pixmap, 0, 0)
            QApplication.setOverrideCursor(cursor)

            if self.start_X_Point < self.end_X_Point and self.start_Y_Point < self.end_Y_Point:
                image = self.screen.grabWindow(QApplication.desktop().winId(), self.start_X_Point, self.start_Y_Point, self.end_X_Point-self.start_X_Point, self.end_Y_Point-self.start_Y_Point)

            if self.start_X_Point < self.end_X_Point and self.start_Y_Point > self.end_Y_Point:
                image = self.screen.grabWindow(QApplication.desktop().winId(), self.start_X_Point, self.end_Y_Point, self.end_X_Point-self.start_X_Point, self.start_Y_Point-self.end_Y_Point)

            if self.start_X_Point > self.end_X_Point and self.start_Y_Point < self.end_Y_Point:
                image = self.screen.grabWindow(QApplication.desktop().winId(), self.end_X_Point, self.start_Y_Point, self.start_X_Point-self.end_X_Point, self.end_Y_Point-self.start_Y_Point)    
            if self.start_X_Point > self.end_X_Point and self.start_Y_Point > self.end_Y_Point:
                image = self.screen.grabWindow(QApplication.desktop().winId(), self.end_X_Point, self.end_Y_Point, self.start_X_Point-self.end_X_Point, self.start_Y_Point-self.end_Y_Point)

            # self.main_window_class.show()
            now = datetime.now().time()
            today = date.today()
            d2 = today.strftime("%B_%d_%Y")
            current_time = now.strftime("%H_%M_%S")

            try:    
                from pathlib import Path
                if self.forOcr == False:    
                    path_folder = str((Path.home() / f"Pictures/Screenshots/ScreenShot_{d2}_{current_time}.png"))
                if self.forOcr == True:  
                    path_folder = str((Path.home() / f"AppData/Local/Temp/ScreenShot_{d2}_{current_time}.png"))  
                image.save(path_folder)
                if self.forOcr == True:
                    # import OCR
                    # self.Ocr_app = OCR.Ui_OCR()
                    # self.Ocr_app.OpenWithPath(path_folder)
                    pass
            except Exception as e:
                try:    
                    print(e)
                    from pathlib import Path
                    path_ = ((Path.home() / f"Pictures/Screenshots"))
                    os.mkdir(path_) 

                    path_folder = str((Path.home() / f"Pictures/Screenshots/ScreenShot_{d2}_{current_time}.png"))
                    image.save(path_folder)
                except Exception as e:
                    pass   
            if self.forOcr == False: 
                try:    
                    self.explore(path_folder)
                except Exception:
                    pass                                                                               
            self.close()
    def explore(self, path):
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
if __name__ == '__main__':

	app = QApplication(sys.argv)
	
	myApp = OCR_app()
	myApp.show()
	sys.exit(app.exec_())





# import sys
# from PyQt5 import QtWidgets

# app = QtWidgets.QApplication(sys.argv)

# screen = app.primaryScreen()
# print('Screen: %s' % screen.name())
# size = screen.size()
# print('Size: %d x %d' % (size.width(), size.height()))
# rect = screen.availableGeometry()
# print('Available: %d x %d' % (rect.width(), rect.height()))

