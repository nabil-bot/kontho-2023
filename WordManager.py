# -*- coding:utf-8 -*-
from importlib.resources import path
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QGridLayout, QPushButton, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QItemSelectionModel
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QHeaderView, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QColor
import pyperclip as pc
import sys
from banglish import jointWordSpliter, convert_to_banglish
from LoadWords import *
import traceback
import io


class wordManagerClass(QMainWindow):
    save_signal = pyqtSignal(str)
    def __init__(self):
        super(wordManagerClass, self).__init__()
        uic.loadUi('.//Uis//WordManagerUi.ui', self)

        self.changes_for_tab_1 = []
        self.redoReserve_for_tab_1 = []

        self.changes_for_tab_2 = []
        self.redoReserve_for_tab_2 = []

        self.changes_for_tab_3 = []
        self.redoReserve_for_tab_3 = []

        self.changes_for_tab_4 = []
        self.redoReserve_for_tab_4 = []
        
        self.loadWords(wordsList, self.tableWidget)   # loading bangla words
        # self.loadWords(englaList, self.EnglaTableWidget)
        # self.loadWords(EnglishwordsList, self.EnglishTableWidget)

        self.clearUndoList()

        self.plainTextEdit.textChanged.connect(self.plainEditTextChanged) 


        self.tableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.tableWidget.itemChanged.connect(self.itemChangedFunc)

        self.EnglaTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.EnglaTableWidget.itemChanged.connect(self.itemChangedFunc)

        self.EnglishTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.EnglishTableWidget.itemChanged.connect(self.itemChangedFunc)

        self.tableWidget_3.currentItemChanged.connect(self.currentItemChangedFunc)
        self.tableWidget_3.itemChanged.connect(self.itemChangedFunc)


        self.contentWasEdited_ofTable_1 = False
        self.contentWasEdited_ofTable_2 = False
        self.contentWasEdited_ofTable_3 = False
        self.contentWasEdited_ofTable_4 = False
        
        self.itemChangedByUndoFunc = False

        self.actionUndo.triggered.connect(self.undo)
        self.UndoPushButton.clicked.connect(self.undo)

        self.actionClear_Undo_List.triggered.connect(lambda:self.clearUndoList())

        self.actionShowTextEditor.triggered.connect(lambda:self.dockWidget_2.setVisible(True))

        self.actionRedo.triggered.connect(self.redo)
        self.RedoPushButton.clicked.connect(self.redo)

        self.CopyPushButton.clicked.connect(self.copyFunc)
        self.CutPushButton.clicked.connect(self.CutFunc)
        self.PastePushButton.clicked.connect(self.PasteFunc)

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

        self.tabWidget.currentChanged.connect(self.TabChanged)
        self.SaveChangesPushButton.clicked.connect(self.saveChangesOfPlainTextEdit)

        


    def saveCurrentTableFunc(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        txt = self.getTextFormTable(currentTable)
        if currentTable == self.tableWidget and self.contentWasEdited_ofTable_1 == True:
            path = banglaDictionaryPath
            self.contentWasEdited_ofTable_1 = False
        elif currentTable == self.EnglaTableWidget and self.contentWasEdited_ofTable_2 == True:
            path = englaDictionaryPath
            self.contentWasEdited_ofTable_2 = False 
        elif currentTable == self.EnglishTableWidget and self.contentWasEdited_ofTable_3 == True:
            path= englishDictionaryPath
            self.contentWasEdited_ofTable_3 = False    
        elif currentTable == self.tableWidget_3 and self.contentWasEdited_ofTable_4 == True:
            path = AbbreviationsPath
            self.contentWasEdited_ofTable_4 = False  
        else:
            return          
        self.writeDownContentsToFile(path, txt) 
        self.indicateTabContentChanged(self.tabWidget.currentIndex(), False)

    def writeDownContentsToFile(self, path, txt):
        with io.open(path, "w", encoding="utf-8") as file:
            file.write(txt)
    def saveChangesOfPlainTextEdit(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        c_item = QTableWidgetItem(self.plainTextEdit.toPlainText().format(0, 0))
        currentTable.setItem(currentTable.currentRow() , currentTable.currentColumn(), c_item)
        self.plainTextEdit.setStyleSheet('QPlainTextEdit{\n	background-color: rgb(1, 22, 39);\n	color: rgb(0, 255, 0);\n	font: 57 14pt "Hind Siliguri Medium";\n}')
    def plainEditTextChanged(self):
        if self.plainTextEdit.toPlainText() == self.currentCellText():
            self.plainTextEdit.setStyleSheet('QPlainTextEdit{\n	background-color: rgb(1, 22, 39);\n	color: rgb(0, 255, 0);\n	font: 57 14pt "Hind Siliguri Medium";\n}')
        else:
            self.plainTextEdit.setStyleSheet('QPlainTextEdit{\n	background-color: rgb(1, 22, 39);\n	color: white;\n	font: 57 14pt "Hind Siliguri Medium";\n}')

    def TabChanged(self, index):
        self.currentItem = ""
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        
        currentTable.setCurrentCell(0, 0, QItemSelectionModel.Current)
    def clearUndoList(self):
        self.changes_for_tab_1.clear()
        self.redoReserve_for_tab_1.clear()

        self.changes_for_tab_2.clear()
        self.redoReserve_for_tab_2.clear()

        self.changes_for_tab_3.clear()
        self.redoReserve_for_tab_3.clear()

        self.changes_for_tab_4.clear()
        self.redoReserve_for_tab_4.clear()
    def currentCellText(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        try:    
            text = (currentTable.item(currentTable.currentRow() , currentTable.currentColumn()).text())
        except Exception as e:
            text = ""   
        return text
    def copyFunc(self):
        pc.copy(self.currentCellText()) 
    def CutFunc(self):
        self.copyFunc()
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        c_item = QTableWidgetItem("".format(0, 0))
        currentTable.setItem(currentTable.currentRow() , currentTable.currentColumn(), c_item)
        pass
    def PasteFunc(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        copied_text = pc.paste()
        self.setCurrentCellText(currentTable, copied_text)
    def setCurrentCellText(self,currentTable, txt):
        c_item = QTableWidgetItem(txt.format(0, 0))
        currentTable.setItem(currentTable.currentRow() , currentTable.currentColumn(), c_item)    
    def currentTable(self):
        if self.tabWidget.currentIndex() == 0:
            return self.tableWidget,self.changes_for_tab_1,self.redoReserve_for_tab_1
        if self.tabWidget.currentIndex() == 1:
            return self.EnglaTableWidget,self.changes_for_tab_2,self.redoReserve_for_tab_2 
        if self.tabWidget.currentIndex() == 2:
            return self.EnglishTableWidget,self.changes_for_tab_3,self.redoReserve_for_tab_3 
        if self.tabWidget.currentIndex() == 3:
            return self.tableWidget_3,self.changes_for_tab_4,self.redoReserve_for_tab_4      
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
                currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
                
                textFromTable = self.getTextFormTable(currentTable)
                with io.open(path, "w", encoding="utf-8") as file:
                    file.write(textFromTable)
            except Exception as e:
                self.showError(e)
    def loadAbbribiations(self):
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
        try:
            path, _ = QFileDialog.getOpenFileName(
                parent= self,
                caption='Open Words file',
                directory= 'C:\\Users\\ui\\Desktop',
                filter ='Text Document (*.txt)'
            )
            if path:
                with io.open(path, "r", encoding="utf-8") as file:
                    words_str = file.read()

                wrd_list = words_str.split("|") 
                currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
                   
                self.loadWords(wrd_list, currentTable)
        except Exception as e:
            self.showError(e)
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
            # self.loadBanglaWords(path)
    def addFunc(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        rowPosition = currentTable.rowCount()
        currentTable.insertRow(rowPosition)
        currentTable.scrollToBottom()
        
        self.addRowUnDoReserveFunc(rowPosition, Current_changes_list, currentTable)  # , Current_changes_list, currentTable
    def addRowUnDoReserveFunc(self, rowPosition, changes, currentTable): # , changes, currentTable
        try:
            changedData = []
            changedData.append("|*|added_New_row|*|")
            if len(changes) != 0:
                last_change = changes[0]
                first_Value_of_last_change = last_change[0] 
                if first_Value_of_last_change == "|*|added_New_row|*|":
                    pre_rows_added = last_change[1]  # list of previous rows added 
                    pre_rows_added.append(rowPosition)
                    changedData.append(pre_rows_added)
                    changes[0] = changedData
                else:    
                    changedData.append([rowPosition])
                    changes.insert(0, changedData)
                    changes = changes[:50]    
            else:    
                changedData.append([rowPosition])
                changes.insert(0, changedData)
                changes = changes[:50] 
            self.saveChangesForUndo_Redo(currentTable, changes)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
    def removeFunc(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()  
        current_row = currentTable.currentRow()
        
        changedData = []
        changedData.append("|*|removed_a_row|*|") # <--

        row_contents = []
        for c in range(currentTable.columnCount()):
            try:    
                txt_from_colunm = currentTable.item(current_row, c).text()
            except Exception:
                txt_from_colunm = " " 
            if txt_from_colunm not in ["", " "]:
                row_contents.append(txt_from_colunm)
        changedData.append(row_contents) # <-- row contentents as list
        changedData.append(current_row) # <-- row position

        Current_changes_list.insert(0, changedData)
        Current_changes_list = Current_changes_list[:50] 

        self.saveChangesForUndo_Redo(currentTable, Current_changes_list)
        currentTable.removeRow(current_row)

    def selectAnItem(self, item):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        
        currentTable.setCurrentItem(item)  
        currentTable.setCurrentCell(currentTable.currentRow(), currentTable.currentColumn()) 
        self.MatchedNumberLineEdit.setText(str(self.currentMatchedIndex+1) + "/"+str(len(self.matching_items)))
    def search(self, s):
        if not s:
            return

        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()

        currentTable.setCurrentItem(None)
        if self.MatchCaseCheckBox.isChecked() == False:
            self.matching_items = currentTable.findItems(s, Qt.MatchContains)
        else:
             self.matching_items = currentTable.findItems(s, Qt.MatchExactly)   
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

    def itemChangedFunc(self, citem):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        # print(type(citem))
        # if currentTable == self.tableWidget and currentTable.currentColumn() == 0: 
        #     if self.currentCellText() not in banglaAlphabates:
        #         self.setCurrentCellText(currentTable, citem.text())
        #         return

        changedData = []
        changedData.append(self.currentItem)
        changedData.append(currentTable.currentRow())
        changedData.append(currentTable.currentColumn())
        if self.itemChangedByUndoFunc == False:
            Current_changes_list.insert(0, changedData)
            Current_changes_list = Current_changes_list[:50]
            self.currentItem = citem.text() 
        self.saveChangesForUndo_Redo(currentTable, Current_changes_list)

        if currentTable == self.tableWidget and currentTable.currentColumn() == 0:    
            self.setEnglaWord(currentTable)
        
        
        if currentTable == self.tableWidget and self.contentWasEdited_ofTable_1 == False:
            self.contentWasEdited_ofTable_1 = True
            self.indicateTabContentChanged(0,True)
        if currentTable == self.EnglaTableWidget and self.contentWasEdited_ofTable_2 == False:
            self.contentWasEdited_ofTable_2 = True
            self.indicateTabContentChanged(1,True)
        if currentTable == self.EnglishTableWidget and self.contentWasEdited_ofTable_3 == False:
            self.contentWasEdited_ofTable_3 = True
            self.indicateTabContentChanged(2,True)
        if currentTable == self.tableWidget_3 and self.contentWasEdited_ofTable_4 == False:
            self.contentWasEdited_ofTable_4 = True        
            self.indicateTabContentChanged(3,True)
    def indicateTabContentChanged(self, index, state):
        if state:
            self.tabWidget.setTabText(index, self.tabWidget.tabText(index)+"*")
        else:  
            self.tabWidget.setTabText(index, self.tabWidget.tabText(index).replace("*", ""))

    def setEnglaWord(self, currentTable):
        if currentTable == self.tableWidget and currentTable.currentColumn() == 0:
            try:
                banglish = convert_to_banglish(self.currentCellText())
                currentTable.setCurrentCell(currentTable.currentRow(), 1, QItemSelectionModel.Current)
                c_item = QTableWidgetItem(banglish.format(0, 0))
                currentTable.setItem(currentTable.currentRow() , 1, c_item)
            except Exception as e:
                self.showError(traceback.format_exc())    
    def saveChangesForUndo_Redo(self, currentTable, Current_changes_list=None, curren_redoReserve=None):
        if Current_changes_list!=None:    
            if currentTable == self.tableWidget:
                self.changes_for_tab_1 = Current_changes_list
            if currentTable == self.EnglaTableWidget:
                self.changes_for_tab_2 = Current_changes_list
            if currentTable == self.EnglishTableWidget:
                self.changes_for_tab_3 = Current_changes_list
            if currentTable == self.tableWidget_3:
                self.changes_for_tab_4 = Current_changes_list  
        if curren_redoReserve != None:    
            if currentTable == self.tableWidget:
                self.redoReserve_for_tab_1 = curren_redoReserve
            if currentTable == self.EnglaTableWidget:
                self.redoReserve_for_tab_2 = curren_redoReserve
            if currentTable == self.EnglishTableWidget:
                self.redoReserve_for_tab_3 = curren_redoReserve
            if currentTable == self.tableWidget_3:
                self.redoReserve_for_tab_4 = curren_redoReserve                              
    def currentItemChangedFunc(self, current, previous):
        if current != None:    
            self.currentItem = current.text()
        else:
            self.currentItem = ""
        self.plainTextEdit.setPlainText(self.currentItem)    
        pass    
    def loadWords(self, wordsList, tableWidget):
        self.itemChangedByUndoFunc = True
        
        changedData = []
        changedData.append("|*|added_New_File_content|*|") # ["|*|added_New_File_content|*|", [[row_pos,[row_contents]],....]]
        row_contents = []  
        for wrd in wordsList:
            wordArray = wrd.split(",")
            if wrd in [" ", ""]:
                continue
            rowPosition = tableWidget.rowCount()
            tableWidget.insertRow(rowPosition)
            row_infos = [] # 1st row position 
            row_infos.append(rowPosition) # <-- Undo Reserve Function Call
            row_items = []
            c = 0
            for w in wordArray[:2]:
                item = QTableWidgetItem(w.format(0, 0))
                row_items.append(w)
                tableWidget.setItem(rowPosition,c, item)
                c+=1
            row_infos.append(row_items) # <-- row_contents 
            row_contents.append(row_infos)
            tableWidget.item(rowPosition, 0).setBackground(QColor(1, 87, 155, 255)) 
        changedData.append(row_contents) 
        
        tableWidget.scrollToBottom() 
        
        if tableWidget == self.tableWidget:    
            self.changes_for_tab_1.insert(0, changedData)
            self.changes_for_tab_1 = self.changes_for_tab_1[:50]

        if tableWidget == self.EnglaTableWidget:    
            self.changes_for_tab_2.insert(0, changedData)
            self.changes_for_tab_2 = self.changes_for_tab_2[:50]

        if tableWidget == self.EnglishTableWidget:    
            self.changes_for_tab_3.insert(0, changedData)
            self.changes_for_tab_3 = self.changes_for_tab_3[:50]    

        if tableWidget == self.tableWidget_3:    
            self.changes_for_tab_4.insert(0, changedData)
            self.changes_for_tab_4 = self.changes_for_tab_4[:50]         
        self.itemChangedByUndoFunc = False

    def undo(self):
        try:    
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
            changes_list, redoReserve_list = self.undo_func(currentTable, Current_changes_list, curren_redoReserve)
            self.saveChangesForUndo_Redo(currentTable, changes_list, redoReserve_list)
            self.plainEditTextChanged()
        except Exception as e:
            print(e)

    def redo(self):
        try:    
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
            changes_list, redoReserve_list = self.redo_func(currentTable, Current_changes_list, curren_redoReserve)
            self.saveChangesForUndo_Redo(currentTable, changes_list, redoReserve_list)
            self.plainEditTextChanged()
        except Exception:
            pass
    def undo_func(self,current_table , changes_list, redoReserve_list):
        # print(changes_list)
        if len(changes_list) != 0:    
            self.itemChangedByUndoFunc = True
            try:
                lastChange = changes_list[0]

                first_Value_of_last_change = lastChange[0]


                if first_Value_of_last_change == "|*|added_New_row|*|":
                    redoReserve_list.insert(0, lastChange)
                    rows_added = lastChange[1] # list of rows added
                    rows_added.reverse()
                    for r in rows_added:                            #             0                             1
                        current_table.removeRow(r)   # lastChange = ["|*|added_New_File_content|*|", [[row_pos,[row_contents]],....]]
                elif first_Value_of_last_change == "|*|added_New_File_content|*|": # this block of code will just remove add rows from file
                    
                    redoReserve_list.insert(0, lastChange) # <-- saving for redo func

                    rows_info = lastChange[1] # list of rows added
                    rows_info.reverse()
                    for row_info in rows_info:
                        row_pos = row_info[0]
                        current_table.removeRow(row_pos)        
                elif first_Value_of_last_change == "|*|removed_a_row|*|":
                    redoReserve_list.insert(0, lastChange)
                    removed_row_position = lastChange[2]
                    current_table.insertRow(removed_row_position)

                    contents_according_column = lastChange[1]
                    c = 0
                    for content in contents_according_column:
                        item = QTableWidgetItem((content).format(0, 0))
                        current_table.setItem(removed_row_position,c, item)
                        c+=1
                    current_table.scrollToItem(item) 
                else:  # item change undo call 
                    
                    # print(f"last change: {lastChange}")
                    
                    change = []
                    change.append((current_table.item(lastChange[1], lastChange[2])).text())
                    change.append(lastChange[1])
                    change.append(lastChange[2])

                    redoReserve_list.insert(0, change)
                    
                    item = QTableWidgetItem((lastChange[0]).format(0, 0))
                    current_table.setItem(lastChange[1],lastChange[2], item)
                    # print(f"lastChange[0]:{lastChange[0]}")


                    current_table.setCurrentCell(lastChange[1], lastChange[2], QItemSelectionModel.Current)
                
                redoReserve_list = redoReserve_list[:50]
                changes_list.remove(lastChange)
                return changes_list, redoReserve_list 

            except Exception as e:
                print(e)
                print(traceback.format_exc())
                pass
            self.itemChangedByUndoFunc = False
    def redo_func(self,current_table, changes_list, redoReserve_list):
        # print(redoReserve_list)
        if len(redoReserve_list) != 0:
            self.itemChangedByUndoFunc = True
            try:
                lastChange = redoReserve_list[0]
                first_Value_of_last_change = lastChange[0]
                if first_Value_of_last_change == "|*|added_New_row|*|":
                    changes_list.insert(0, lastChange)
                    rows_added = lastChange[1]
                    rows_added.reverse()
                    for r in rows_added:
                        current_table.insertRow(r)
                    current_table.scrollToBottom() # lastChange = ["|*|added_New_File_content|*|", [[row_pos,[row_contents]],....]]
                elif first_Value_of_last_change == "|*|added_New_File_content|*|":
                    changes_list.insert(0, lastChange) # <-- saving it for undo

                    rows_info = lastChange[1] # [[row_pos,[row_contents]],....]
                    rows_info.reverse()
                    for row_infos in rows_info[:]:
                        # print(row_infos)
                        row_pos = row_infos[0]
                        current_table.insertRow(row_pos)
                        row_conts = row_infos[1]
                        c = 0
                        for w in row_conts[:]:
                            item = QTableWidgetItem(w.format(0, 0))
                            current_table.setItem(row_pos,c, item)
                            c += 1
                    current_table.scrollToBottom()        

                elif first_Value_of_last_change == "|*|removed_a_row|*|":
                    changes_list.insert(0, lastChange)
                    current_table.removeRow(lastChange[2])
                else:
                    change = []
                    try:    
                        change.append((current_table.item(lastChange[1], lastChange[2])).text())
                    except Exception:
                        change.append("")   
                    change.append(lastChange[1])
                    change.append(lastChange[2])
                    
                    changes_list.insert(0, change)
                    item = QTableWidgetItem((lastChange[0]).format(0, 0))
                    current_table.setItem(lastChange[1],lastChange[2], item)
                    current_table.setCurrentCell(lastChange[1], lastChange[2], QItemSelectionModel.Current)

                changes_list = changes_list[:50]
                try:    
                    redoReserve_list = redoReserve_list[1:50]
                except Exception:
                    redoReserve_list = []        
            except Exception as e:
                print(traceback.format_exc())
                pass
            self.itemChangedByUndoFunc = False
            return changes_list,redoReserve_list 
   
    def showError(self, error_msg):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{\n"
                        "color: white;\n"
                        "background-color: rgb(108, 177, 223);\n"
                        "font: 12pt \"MS Shell Dlg 2\";\n"
                        "gridline-color: #EAEDED;\n"
                        "}")
        msg.setWindowTitle("Error")
        msg.setText(f"{error_msg}")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_() 
    def closeEvent(self, event):
        self.close()     
             
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = wordManagerClass()
    ex.show()
    sys.exit(app.exec_())         