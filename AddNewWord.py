# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QGridLayout, QPushButton, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QSettings, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5 import uic
import sys
from banglish import jointWordSpliter, convert_to_banglish

class AddNewWordsClass(QMainWindow):
    def __init__(self):
        super(AddNewWordsClass, self).__init__()
        uic.loadUi('.//Uis//AddNewWords_Ui.ui', self)

        self.PlusButton.clicked.connect(self.addRowFunc)
        self.MinusButton.clicked.connect(self.RemoveRowFunc)
        
        self.tableWidget.itemChanged.connect(self.itemChangedFunc)

        

    
    def itemChangedFunc(self):
        if self.tableWidget.currentColumn() == 0:
            word = self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text()
            try:
                convertion = jointWordSpliter(word) 
                if convertion != None:
                    banglish = convertion
                else:
                    banglish = convert_to_banglish(word) 
                pass
                current_item = banglish
                c_item = QTableWidgetItem(current_item.format(0, 0))
                self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn()+1, c_item)
            except Exception as e:
                print(e)
    def addRowFunc(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        pass
    def RemoveRowFunc(self):
        # selected_items = self.tableWidget.selectedItems()
        self.tableWidget.removeRow(self.tableWidget.currentRow())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AddNewWordsClass() 
    ex.show()
    sys.exit(app.exec_())         