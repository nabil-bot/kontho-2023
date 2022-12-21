import PyQt5
from PyQt5 import uic, QtCore
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog,QColorDialog, QMainWindow, QMessageBox, QPushButton, QSlider, QScrollArea,QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem, QTextEdit, QFontDialog 
from PyQt5.QtGui import QIntValidator, QColor, QFont, QPixmap, QMovie  
from PyQt5.QtCore import QSettings
import sys
import easyocr
import pyperclip

class ThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(str)

    def __init__(self,file_path, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
        self.file_path = file_path
    def run(self):
        reader = easyocr.Reader(['bn','en']) # this needs to run only once to load the model into memory
        result = reader.readtext(self.file_path)
        result_to_send = ""
        for item in result:
            result_to_send += (f"{item[1]} ")
        self.any_signal.emit(result_to_send)

    def stop(self):
        self.is_running = False
        self.terminate()    

class Ui_OCR(QMainWindow):
    def __init__(self):
        super(Ui_OCR, self).__init__() 
        uic.loadUi('.//Uis//OCRUI.ui', self) 
        self.OpenBtn.clicked.connect(self.openImageFunc)
        self.CopyBTN.clicked.connect(self.CopyFunc)
        self.CutBtn.clicked.connect(self.CutFunc)
        self.ClearBtn.clicked.connect(lambda:self.plainTextEdit.clear())
        self.CancelBtn.setVisible(False)
        self.CancelBtn.clicked.connect(self.missionAbortFunc)
        self.groupBox.setVisible(False)

    def openImageFunc(self):   
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory="",
            filter= 'All(*.*);;png file (*.png);; jpg (*.jpg)'
            )

        if file_path:
            self.thread = ThreadClass(file_path, parent=None)
            self.thread.any_signal.connect(self.ShowResult) 
            self.thread.start()
            self.CancelBtn.setVisible(True)
            self.OpenBtn.setVisible(False)
            self.groupBox.setVisible(False)
            pixmap = QPixmap(file_path)
            self.label.setPixmap(pixmap)
    def missionAbortFunc(self):
        try:
            self.thread.stop()
            self.CancelBtn.setVisible(False)
            self.OpenBtn.setVisible(True)
            self.groupBox.setVisible(False)
            self.label.setText("Open an Image")
        except Exception:
            pass
    def CopyFunc(self):
        text = self.plainTextEdit.toPlainText()
        pyperclip.copy(text)
    def ShowResult(self, result):
        self.plainTextEdit.setPlainText(result)
        self.groupBox.setVisible(True)
        self.CancelBtn.setVisible(False)
        self.OpenBtn.setVisible(True)
        self.groupBox.setVisible(True)
    def CutFunc(self):
        self.CopyFunc()
        self.plainTextEdit.clear()   
    def ShowSelf(self):
        self.show() 
    def OpenWithPath(self, filePath):
        self.thread = ThreadClass(filePath, parent=None)
        self.thread.any_signal.connect(self.ShowResult) 
        self.thread.start()
        pixmap = QPixmap(filePath)
        self.label.setPixmap(pixmap) 
        self.CancelBtn.setVisible(True)
        self.OpenBtn.setVisible(False)  
        self.show()
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_OCR() 
    ex.show()
    sys.exit(app.exec_())          