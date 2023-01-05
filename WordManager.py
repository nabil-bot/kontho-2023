# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QGridLayout, QPushButton, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QItemSelectionModel
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QHeaderView, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QColor
import sys
from banglish import jointWordSpliter, convert_to_banglish
from LoadWords import wordsList, englaList, EnglishwordsList
import traceback
import io
# from banglish import jointWordSpliter, convert_to_banglish

class wordManagerClass(QMainWindow):
    save_signal = pyqtSignal(str)
    def __init__(self):
        super(wordManagerClass, self).__init__()
        uic.loadUi('.//Uis//WordManagerUi.ui', self)

        # self.loadBanglaWords()

        self.loadWords(wordsList, self.tableWidget)   # loading bangla words
        # self.loadWords(englaList, self.EnglaTableWidget)
        # self.loadWords(EnglishwordsList, self.EnglishTableWidget)


        self.changes = []
        self.redoReserve = []

        self.tableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.tableWidget.itemChanged.connect(self.itemChangedFunc)

        self.itemChangedByUndoFunc = False

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

        self.lineEdit.textChanged.connect(self.search)
        self.matching_items = []

        self.AddPushButton.clicked.connect(self.addFunc)
        self.RemovePushButton.clicked.connect(self.removeFunc)

        self.actionOpen.triggered.connect(self.openFile)
        self.currentItem = ""
        self.actionAdd_Words_from_file.triggered.connect(self.AddWordsFromFile)
    
        self.SavePushButton.clicked.connect(self.saveFunc)

        self.loadAbbribiations()

        self.matching_items = []
        self.currentMatchedIndex = 0
        self.UpPushButton.clicked.connect(self.upPushButtonClicked)
        self.DownPushButton.clicked.connect(self.DownPushButtonClicked)

        self.actionSave_as.triggered.connect(self.saveAsFunction)

        # self.tableWidget.itemChanged.connect(self.itemChangedFunc)
    

    def getTextFormTable(self, table):
        row_count = table.rowCount()
        colum_count = table.columnCount()
        
        text_ = ''
        for no in range(row_count):
            wordStr = ""
            for c in range(colum_count):
                try:    
                    txtFromColumn = (table.item(no, c).text()).replace(" ", "")
                except Exception:
                    break    
                if txtFromColumn != "":   
                    wordStr += f"{txtFromColumn},"
            if wordStr != "":    
                text_ += f"{wordStr[:-1]}|"
        return text_[:-1]
    def saveAsFunction(self):
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file as',
            directory= 'C:\\Users\\ui\\Desktop',
            filter ='Text Document (*.txt)'
        )                               
        if not path:
            return
        else:
            try:
                if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Bangla":
                    textFromTable = self.getTextFormTable(self.tableWidget)
                    with io.open(path, "w", encoding="utf-8") as file:
                        file.write(textFromTable)
            except Exception as e:
                self.showError(e)
    def loadAbbribiations(self):
        with io.open('.//Res//Abbreviations.txt', "r", encoding="utf-8") as RKS:
            abriStr = RKS.read()
        abris = abriStr.split("\n")
        
        header = self.tableWidget_3.horizontalHeader()       
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        for ab in abris[:]:
            if ab == "":
                return
            parts = ab.split("::")
            if len(parts) == 0:
                return

            rowPosition = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(rowPosition)

            item1 = QTableWidgetItem(parts[0].format(0, 0))
            self.tableWidget_3.setItem(rowPosition,0, item1)

            item2 = QTableWidgetItem(parts[1].format(0, 0))
            self.tableWidget_3.setItem(rowPosition, 1, item2)
    def saveFunc(self):
        if self.tabWidget.currentIndex() == 0:
            pass
        elif self.tabWidget.currentIndex() == 3:
            strToSave = ""
            row_count = self.tableWidget_3.rowCount()
            for i in range(row_count):
                if self.tableWidget_3.item(i, 0).text() and self.tableWidget_3.item(i, 1).text() not in ["", " ", "  "]:
                    strToSave += f"{self.tableWidget_3.item(i, 0).text()}::{self.tableWidget_3.item(i, 1).text()}\n"
            with io.open('.//Res//Abbreviations.txt', "w", encoding="utf-8") as RKS:
                RKS.write(strToSave)
        self.save_signal.emit("dkjf")
    def AddWordsFromFile(self):
        path, _ = QFileDialog.getOpenFileName(
            parent= self,
            caption='Open Words file',
            directory= 'C:\\Users\\ui\\Desktop',
            filter ='Text Document (*.txt)'
        )
        if path:
            self.loadBanglaWords(path)
        pass
    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(
            parent= self,
            caption='Open Words file',
            directory= 'C:\\Users\\ui\\Desktop',
            filter ='Text Document (*.txt)'
        )
        if path:
            # self.tableWidget.clear()
            while (self.tableWidget.rowCount() > 0):
                self.tableWidget.removeRow(0)
            self.loadBanglaWords(path)
    def addFunc(self):
        if self.tabWidget.currentIndex() == 0:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.scrollToBottom()

            # saving it to undo func 
        
            changedData = []
            changedData.append("|*|added_New_row|*|")
            
            if len(self.changes) != 0:
                last_change = self.changes[0]
                first_Value_of_last_change = last_change[0] 
                if first_Value_of_last_change == "|*|added_New_row|*|":
                    pre_rows_added = last_change[1]  # list of previous rows added 
                    pre_rows_added.append(rowPosition)
                    changedData.append(pre_rows_added)
                    self.changes[0] = changedData
                else:    
                    changedData.append([rowPosition])
                    self.changes.insert(0, changedData)
                    self.changes = self.changes[:50]    
            else:    
                changedData.append([rowPosition])
                self.changes.insert(0, changedData)
                self.changes = self.changes[:50]    
        elif self.tabWidget.currentIndex() == 3:
            rowPosition = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(rowPosition)
            self.tableWidget_3.scrollToBottom()
            pass 
   
        pass
    def removeFunc(self):
        if self.tabWidget.currentIndex() == 0:    
            current_row = self.tableWidget.currentRow()
            
            changedData = []
            changedData.append("|*|removed_a_row|*|") # <--
            
            row_contents = []
            for c in range(self.tableWidget.columnCount()):
                try:    
                    txt_from_colunm = self.tableWidget.item(current_row, c).text()
                except Exception:
                    txt_from_colunm = " " 
                if txt_from_colunm not in ["", " "]:
                    row_contents.append(txt_from_colunm)
            changedData.append(row_contents) # <-- row contentents as list
            changedData.append(current_row) # <-- row position

            self.changes.insert(0, changedData)
            self.changes = self.changes[:50] 

            self.tableWidget.removeRow(current_row)

            # saving it to undo func 


        elif self.tabWidget.currentIndex() == 2:   
            self.tableWidget_3.removeRow(self.tableWidget.currentRow())
    def selectAnItem(self, item):
        self.tableWidget.setCurrentItem(item)  
        self.tableWidget.setCurrentCell(self.tableWidget.currentRow(), self.tableWidget.currentColumn()) 
        self.MatchedNumberLineEdit.setText(str(self.currentMatchedIndex+1) + "/"+str(len(self.matching_items)))
    def search(self, s):
        if not s:
            return
        if self.tabWidget.currentIndex() == 0: 
            self.tableWidget.setCurrentItem(None)
            
            self.matching_items = self.tableWidget.findItems(s, Qt.MatchContains)
            self.MatchedNumberLineEdit.setText(str(self.currentMatchedIndex+1) + "/"+str(len(self.matching_items)))
            if self.matching_items:
                item = self.matching_items[0] 
                self.selectAnItem(item) 
    def DownPushButtonClicked(self):
        if len(self.matching_items) != 0:
            try:    
                item = self.matching_items[self.currentMatchedIndex+1] 
                self.currentMatchedIndex+=1
            except Exception:
                item = self.matching_items[0]
                self.currentMatchedIndex = 0
            self.selectAnItem(item)
        pass
    def upPushButtonClicked(self):
        if len(self.matching_items) != 0:
            try:    
                item = self.matching_items[self.currentMatchedIndex-1] 
                self.currentMatchedIndex-=1
            except Exception:
                item = self.matching_items[0]
                self.currentMatchedIndex = 0

            self.selectAnItem(item)
            pass
        pass
    # def itemChangedFunc(self, citem):
    #     changedData = []
    #     changedData.append(self.currentItem)
    #     changedData.append(self.tableWidget.currentRow())
    #     changedData.append(self.tableWidget.currentColumn())
    #     if self.itemChangedByUndoFunc == False:
    #         self.changes.insert(0, changedData)
    #         self.changes = self.changes[:50]
    #         self.currentItem = citem

    #     pass
    #     # print("in func")
    #     if self.tableWidget.currentColumn() == 0:
    #         # print("in if")
    #         word = self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text()
    #         # print(word)
    #         try:
    #             convertion = jointWordSpliter(word) 
    #             if convertion != None:
    #                 banglish = convertion
    #             else:
    #                 banglish = convert_to_banglish(word) 
    #             pass
    #             # print(banglish)
    #             current_item = banglish
    #             c_item = QTableWidgetItem(current_item.format(0, 0))
                
    #             self.tableWidget.itemChanged.disconnect(self.itemChangedFunc)
                
    #             self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn()+1, c_item)
    #             self.tableWidget.itemChanged.connect(self.itemChangedFunc)

    #         except Exception as e:
    #             print(e)
    # def currentItemChangedFunc(self, current, previous):
    #     if current != None:    
    #         self.currentItem = current.text()
    #     else:
    #         self.currentItem = ""

    #     pass

    def itemChangedFunc(self, citem):
        changedData = []
        changedData.append(self.currentItem)
        changedData.append(self.tableWidget.currentRow())
        changedData.append(self.tableWidget.currentColumn())
        if self.itemChangedByUndoFunc == False:
            self.changes.insert(0, changedData)
            self.changes = self.changes[:50]
            self.currentItem = citem
        pass
    def currentItemChangedFunc(self, current, previous):
        if current != None:    
            self.currentItem = current.text()
        else:
            self.currentItem = ""
        pass    
    def loadWords(self, wordsList, tableWidget):
        for wrd in wordsList:
            wordArray = wrd.split(",")
            if wrd in [" ", ""]:
                continue
            rowPosition = tableWidget.rowCount()
            tableWidget.insertRow(rowPosition)
            c = 0
            for w in wordArray[:2]:
                item = QTableWidgetItem(w.format(0, 0))
                tableWidget.setItem(rowPosition,c, item)
                c+=1
            tableWidget.item(rowPosition, 0).setBackground(QColor(170, 255, 0, 155)) 
    def undo(self):
        if len(self.changes) != 0:    
            self.itemChangedByUndoFunc = True
            try:
                lastChange = self.changes[0]

                first_Value_of_last_change = lastChange[0]


                if first_Value_of_last_change == "|*|added_New_row|*|":
                    self.redoReserve.insert(0, lastChange)
                    rows_added = lastChange[1] # list of rows added
                    rows_added.reverse()
                    for r in rows_added:
                        self.tableWidget.removeRow(r)
                elif first_Value_of_last_change == "|*|removed_a_row|*|":
                    self.redoReserve.insert(0, lastChange)
                    removed_row_position = lastChange[2]
                    self.tableWidget.insertRow(removed_row_position)

                    contents_according_column = lastChange[1]
                    c = 0
                    for content in contents_according_column:
                        item = QTableWidgetItem((content).format(0, 0))
                        self.tableWidget.setItem(removed_row_position,c, item)
                        c+=1
                    self.tableWidget.scrollToItem(item) 
                else:
                    change = []
                    change.append((self.tableWidget.item(lastChange[1], lastChange[2])).text())
                    change.append(lastChange[1])
                    change.append(lastChange[2])

                    self.redoReserve.insert(0, change)
                    
                    item = QTableWidgetItem((lastChange[0]).format(0, 0))
                    self.tableWidget.setItem(lastChange[1],lastChange[2], item)
                    self.tableWidget.setCurrentCell(lastChange[1], lastChange[2], QItemSelectionModel.Current)
                
                self.redoReserve = self.redoReserve[:50]
                try:    
                    self.changes = self.changes[1:50] 
                except Exception:
                    self.changes = []   
                # print(self.changes)
            except Exception as e:
                print(e)
                print("in undo function") 
                pass
            self.itemChangedByUndoFunc = False
    def redo(self):
        if len(self.redoReserve) != 0:
            self.itemChangedByUndoFunc = True
            try:
                lastChange = self.redoReserve[0]
                
                first_Value_of_last_change = lastChange[0]

                if first_Value_of_last_change == "|*|added_New_row|*|":
                    self.changes.insert(0, lastChange)
                    rows_added = lastChange[1]
                    rows_added.reverse()
                    for r in rows_added:
                        self.tableWidget.insertRow(r)
                    self.tableWidget.scrollToBottom()
                elif first_Value_of_last_change == "|*|removed_a_row|*|":
                    self.changes.insert(0, lastChange)
                    self.tableWidget.removeRow(lastChange[2])
                else:
                    self.changes.insert(0, lastChange)
                    item = QTableWidgetItem((lastChange[0]).format(0, 0))
                    self.tableWidget.setItem(lastChange[1],lastChange[2], item)
                    self.tableWidget.setCurrentCell(lastChange[1], lastChange[2], QItemSelectionModel.Current)

                self.changes = self.changes[:50]
                try:    
                    self.redoReserve = self.redoReserve[1:50]
                except Exception:
                    self.redoReserve = []        
            except Exception as e:
                print(traceback.format_exc())
                pass
            self.itemChangedByUndoFunc = False
            pass  
    def showError(self, e):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{\n"
                        "color: white;\n"
                        "background-color: rgb(108, 177, 223);\n"
                        "font: 12pt \"MS Shell Dlg 2\";\n"
                        "gridline-color: #EAEDED;\n"
                        "}")
        msg.setWindowTitle("Error")
        msg.setText(f"{e}")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = wordManagerClass()
    ex.show()
    sys.exit(app.exec_())         