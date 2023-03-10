# -*- coding:utf-8 -*-
from importlib.resources import path
from os import stat
from shutil import ExecError
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QGridLayout, QPushButton, QTableWidgetItem, QFileDialog, QTableWidget, QStyledItemDelegate, QLineEdit, QPlainTextEdit, QAbstractItemView
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QItemSelectionModel, QEvent, QRegExp
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QHeaderView, QMessageBox, QGraphicsDropShadowEffect
from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator
import pyperclip as pc
import sys
from banglish import jointWordSpliter, convert_to_banglish, main_banglish_converter
from LoadWords import *
import traceback
import io
import re

import string
class LoadWordsThreadClass(QtCore.QThread):	
    # insert_row_signal = QtCore.pyqtSignal(i)
    setRowItems_signal = QtCore.pyqtSignal(str)

    prog_signal = QtCore.pyqtSignal(int, str)
    finished_signal = QtCore.pyqtSignal(list)
    def __init__(self, wordsList, tableWidget, adding_from_newFile):
        super(LoadWordsThreadClass, self).__init__()
        self.is_running = True
        self.wordsList = wordsList
        self.tableWidget = tableWidget
        self.adding_from_newFile = adding_from_newFile
    def run(self):
        changedData = []
        changedData.append("|*|added_New_File_content|*|") # ["|*|added_New_File_content|*|", [[row_pos,[row_contents]],....]]
        row_contents = []  
    
        rowPosition = self.tableWidget.rowCount()

        length = len(self.wordsList)
        count = 0
        # multiDimen_array_to_send = []
        for wrd in self.wordsList:
            wordArray = wrd.split(",")
            if wrd in [" ", ""]:   # < we have to put the if condition in here 
                continue

            # this code prevents adding dublicate words ==========
            if self.adding_from_newFile == True:
                main_wrd = wordArray[0]
                found_items = self.tableWidget.findItems(main_wrd, Qt.MatchContains)
                if len(found_items) > 0:
                    # print(main_wrd)
                    continue
            rowPosition += 1

            self.tableWidget.insertRow(rowPosition)
            # self.insert_row_signal.emit(rowPosition)


            row_infos = [] # 1st row position 
            row_infos.append(rowPosition) # <-- Undo Reserve Function Call
            row_items = []
            c = 0
            for w in wordArray[:5]:
                item = QTableWidgetItem(w.format(0, 0))
                row_items.append(w)
                self.tableWidget.setItem(rowPosition,c, item)
                self.setRowItems_signal.emit(w)

                c+=1
            row_infos.append(row_items) # <-- row_contents 
            row_contents.append(row_infos)
            
            # if self.adding_from_newFile == False:    
            #     tableWidget.item(rowPosition, 0).setBackground(self.savedBGColor) 
            # multiDimen_array_to_send.append(word_infos)
            count += 1
            progress = (count/length*100)
            self.prog_signal.emit(int(progress), wordArray[0])
        
        changedData.append(row_contents) 
        self.finished_signal.emit(changedData)

    def stop(self):
        self.is_running = False
        self.terminate() 
         
class PlainTextEditEnglishDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PlainTextEditEnglishDelegate, self).__init__(parent)
    def createEditor(self, parent, option, index):
        editor = QPlainTextEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^[a-zA-Z]+$')) 
        editor.setValidator(validator)
        return editor
    

class PlainTextEditBanglaDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PlainTextEditBanglaDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QPlainTextEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('[\u0980-\u09E3]+')) 
        editor.setValidator(validator)
        return editor
    

class AbbribiationDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9!@#$%^&*+=-.<>]+")) 
        editor.setValidator(validator)
        return editor 

class AbbribiationContentDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(".*")) 
        editor.setValidator(validator)
        return editor 
    def setEditorData(self, editor, index):
        editor.setText(index.data())
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

class EnglishDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^[a-zA-Z]+$')) 
        editor.setValidator(validator)
        return editor
    def setEditorData(self, editor, index):
        editor.setText(index.data())
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

class BanglaDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('[\u0980-\u09E3]+')) 
        editor.setValidator(validator)
        return editor
    def setEditorData(self, editor, index):
        editor.setText(index.data())
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


class Ui_Splash(QWidget):
    def __init__(self):
        super(Ui_Splash, self).__init__() 
        uic.loadUi('.//Uis//Splash Screen.ui', self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | QtCore.Qt.Tool )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(1)
        shadow.setColor(QColor(3, 115, 255))
        self.progressBar.setGraphicsEffect(shadow)
    def progress(self, prog):
        self.progressBar.setValue(prog)    

class wordManagerClass(QMainWindow): 
    save_signal = pyqtSignal(str)
    def __init__(self):
        super(wordManagerClass, self).__init__()
        uic.loadUi('.//Uis//WordManagerUi.ui', self)

        
        self.initChanges()
        self.StretchHeaders()
        self.clearUndoList()

        self.plainTextEdit.textChanged.connect(self.plainEditTextChanged) 

        
        # self.Bangla_Delegate = BanglaDelegate(self.tableWidget)
        self.English_Delegate = EnglishDelegate(self.tableWidget)

        self.plainTextEdit_English_Delegate = PlainTextEditEnglishDelegate(self.plainTextEdit) 
        self.plainTextEdit_Bangla_Delegate = PlainTextEditBanglaDelegate(self.plainTextEdit)
        # self.tableWidget.setItemDelegateForRow(0, delegate)


        # self.EnglaTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        # self.EnglaTableWidget.itemChanged.connect(self.itemChangedFunc)

        
        # self.EnglishTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        # self.EnglishTableWidget.itemChanged.connect(self.itemChangedFunc)
        self.EnglishTableWidget.setItemDelegate(self.English_Delegate)  


        self.tableWidget_3.currentItemChanged.connect(self.currentItemChangedFunc)
        self.tableWidget_3.itemChanged.connect(self.itemChangedFunc)

        

        # delegate = AbbribiationDelegate(self.tableWidget_3)
        # self.tableWidget_3.setItemDelegateForColumn(0, delegate)  # < ----------------------- 

        # self.tableWidget.verticalScrollBar().valueChanged.connect(self.scrollEvent_bangla)
        # self.EnglishTableWidget.verticalScrollBar().valueChanged.connect(self.scrollEvent_english)
        
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.scrollEvent)
        # self.EnglishTableWidget.verticalScrollBar().valueChanged.connect(self.scrollEvent)
        # self.EnglaTableWidget.verticalScrollBar().valueChanged.connect(self.scrollEvent)
        
        self.itemChangedByUndoFunc = False

        self.actionUndo.triggered.connect(self.undo)
        self.UndoPushButton.clicked.connect(self.undo)

        self.actionClear_Undo_List.triggered.connect(lambda:self.clearUndoList())

        self.actionShowTextEditor.triggered.connect(lambda:self.dockWidget_2.setVisible(True))

        self.actionRedo.triggered.connect(self.redo)
        self.RedoPushButton.clicked.connect(self.redo)

        self.CopyPushButton.clicked.connect(self.copyFunc)

        self.PastePushButton.clicked.connect(self.PasteFunc)

        self.lineEdit.textChanged.connect(self.search)
        self.matching_items = []

        self.AddPushButton.clicked.connect(self.addFunc)
        self.RemovePushButton.clicked.connect(self.removeFunc)

        self.actionOpen.triggered.connect(self.openFile)
        self.currentItem = ""
        self.actionAdd_Words_from_file.triggered.connect(self.AddWordsFromFile)
    
        self.SavePushButton.clicked.connect(self.saveCurrentTableFunc)

        

        self.matching_items = []
        self.currentMatchedIndex = 0
        self.UpPushButton.clicked.connect(self.upPushButtonClicked)
        self.DownPushButton.clicked.connect(self.DownPushButtonClicked)

        self.actionSave_as.triggered.connect(self.saveAsFunction)
        self.actionSave.triggered.connect(self.saveFunc)

        self.tabWidget.currentChanged.connect(self.TabChanged)
        self.SaveChangesPushButton.clicked.connect(self.saveChangesOfPlainTextEdit)

        
        self.contentWasEdited_ofTable_1 = False

        
        self.ProgressGroupBox.setVisible(False)

        self.CancelPushButton.clicked.connect(self.stopSaveThread)

        # self.PastePushButton.toolTip("Paste in currect cell")
        # self.plainTextEdit.keyPressEvent = self.keyPressEvent_PlainTextEdit
        self.plainTextEdit.installEventFilter(self)
        self.stufLoaded = False
    # =-===================----..>>>>

        self.actionTestBanglishAlgo.triggered.connect(self.TestBanglish)

        special_characters = '''!@#$%^&*()-_=+[{]};:'\",<.>/?\\|'''
        self.abbri_characters = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('0'), ord('9')+1)] + [c for c in special_characters]

        self.MatchCaseCheckBox.clicked.connect(self.search)
        # self.loadStuff()

        self.savedBGColor = QColor(0, 5, 168, 255)
        
        self.loadThres = 130
        self.my_bangla_list = wordsList
        self.total_bangla_num = len(self.my_bangla_list)
        
        self.banglaWordsLoaded = False
        self.englaWordsLoaded = False
        self.englishWordsLoaded = False

        # self.my_engla_list = englaList
        # print(len(self.my_engla_list))
        # self.total_engla_num = len(self.my_engla_list)

        # self.my_english_list = EnglishwordsList
        # self.total_english_num = len(self.my_english_list)
        # self.Load_parcial_bangla()
        # self.Load_parcial_English()

        # self.Load_parcial(self.tableWidget)
        # self.Load_parcial(self.EnglaTableWidget)
        # print(len(self.my_engla_list))
        # self.Load_parcial(self.EnglishTableWidget)
        self.itemChangedByUndoFunc = True
        self.loadAbbribiations()
        self.itemChangedByUndoFunc = False


        self.tableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.tableWidget.itemChanged.connect(self.itemChangedFunc)

        # print(f"before len of self.my_bangla_list:{len(self.my_bangla_list)}")
        
        # print(f"After len of self.my_bangla_list:{len(self.my_bangla_list)}")

        # self.my_engla_list = self.Load_parcial(self.my_engla_list, self.EnglaTableWidget, loadThres=100)
        # self.my_english_list = self.Load_parcial(self.my_english_list, self.EnglishTableWidget, loadThres=100) 

        self.LoadBanglaListPushBtn.clicked.connect(self.loadCompleteBanglaWordList)
        
        self.LoadEnglishPushButton.clicked.connect(self.loadCompleteEnglishWordList)
        
        self.LoadEnglaPushButton.clicked.connect(self.loadCompleteEnglaWordList)
        
        # self.loadWords(EnglishwordsList, self.EnglishTableWidget)
        # self.groupBox_7.setVisible(False) 
        self.loadCustom()
        self.CustomTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.CustomTableWidget.itemChanged.connect(self.itemChangedFunc)

        self.loadClip()
        self.ClipBoardtableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.ClipBoardtableWidget.itemChanged.connect(self.itemChangedFunc)

        

    def loadClip(self):
        self.itemChangedByUndoFunc = True
        self.ClipBoardtableWidget.clear()
        self.ClipBoardtableWidget.setRowCount(0)
        with io.open(clipBoardPath, "r", encoding="utf-8") as RKS:
            clips = RKS.read()
        clipboard = clips.split("|@|\n")
        # print(clipboard)
        for clip in clipboard:
            parts = clip.split("|*|\n")
            if len(parts) == 0:
                return
            rowPosition = self.ClipBoardtableWidget.rowCount()
            self.ClipBoardtableWidget.insertRow(rowPosition)
            try:
                item1 = QTableWidgetItem(parts[0].format(0, 0))
                self.ClipBoardtableWidget.setItem(rowPosition,0, item1)

                item2 = QTableWidgetItem(parts[1].format(0, 0))
                self.ClipBoardtableWidget.setItem(rowPosition, 1, item2)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        self.itemChangedByUndoFunc = False
    def initChanges(self):
        self.changes_for_tab_1 = []
        self.redoReserve_for_tab_1 = []

        self.changes_for_tab_2 = []
        self.redoReserve_for_tab_2 = []

        self.changes_for_tab_3 = []
        self.redoReserve_for_tab_3 = []

        self.changes_for_tab_4 = []
        self.redoReserve_for_tab_4 = []

        self.changes_for_tab_5 = []
        self.redoReserve_for_tab_5 = []

        self.changes_for_tab_6 = []
        self.redoReserve_for_tab_6 = []
        
        self.contentWasEdited_ofTable_1 = False
        self.contentWasEdited_ofTable_2 = False
        self.contentWasEdited_ofTable_3 = False
        self.contentWasEdited_ofTable_4 = False
        self.contentWasEdited_ofTable_5 = False
        self.contentWasEdited_ofTable_6 = False
    def StretchHeaders(self):
        header = self.tableWidget_3.horizontalHeader()       
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        header2 = self.CustomTableWidget.horizontalHeader()
        header2.setSectionResizeMode(0, QHeaderView.Stretch)
        
        header3 = self.ClipBoardtableWidget.horizontalHeader()       
        header3.setSectionResizeMode(1, QHeaderView.Stretch)    
    def loadCompleteBanglaWordList(self):
        self.loadWords(self.my_bangla_list, self.tableWidget)
        self.my_bangla_list = []
        self.groupBox_6.setVisible(False) 
        self.banglaWordsLoaded = True
    def loadCompleteEnglaWordList(self):
        self.loadWords(englaList, self.EnglaTableWidget)
        self.groupBox_8.setVisible(False)
        self.EnglaTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.EnglaTableWidget.itemChanged.connect(self.itemChangedFunc)

        self.englaWordsLoaded = True

    def loadCompleteEnglishWordList(self):
        self.loadWords(EnglishwordsList, self.EnglishTableWidget)
        self.groupBox_7.setVisible(False)  
        self.EnglishTableWidget.currentItemChanged.connect(self.currentItemChangedFunc)
        self.EnglishTableWidget.itemChanged.connect(self.itemChangedFunc)

        self.englishWordsLoaded = True
    
    def scrollEvent(self, value=0):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        
        lastVisibleRow = currentTable.rowAt(currentTable.viewport().height()) 

        if lastVisibleRow >= currentTable.rowCount() - 30 and len(self.my_bangla_list) !=0:
            self.Load_parcial(currentTable)
    
    def Load_parcial(self, c_table, loadThres=250):
        
        self.itemChangedByUndoFunc = True
        if c_table == self.tableWidget:
            c_list = self.my_bangla_list
        # if c_table == self.EnglaTableWidget:
        #     c_list = self.my_engla_list     
        # if c_table == self.EnglishTableWidget:
        #     c_list = self.my_english_list    

        w_c=0
        for wrd in c_list[:]:
            wordArray = wrd.split(",")
            if wrd in [" ", ""]:  # < we have to put the if condition in here ??????????????????????????????
                continue
            
            rowPosition = c_table.rowCount()
            c_table.insertRow(rowPosition)

            c = 0
            for w in wordArray[:5]:
                item = QTableWidgetItem(w.format(0, 0))
                c_table.setItem(rowPosition,c, item)
                c+=1
            w_c+= 1
            c_table.item(rowPosition, 0).setBackground(self.savedBGColor) 
            
            if c_table == self.tableWidget:
                self.my_bangla_list.remove(wrd)
            if c_table == self.EnglaTableWidget:
                self.my_engla_list.remove(wrd)
            if c_table == self.EnglishTableWidget:
                self.my_english_list.remove(wrd)

            if w_c >= loadThres:
                break

        if c_table == self.tableWidget:
            if len(self.my_bangla_list) == 0:
                self.groupBox_6.setVisible(False) 
                self.banglaWordsLoaded = True
            self.banglaLabel.setText(f"Showing {self.tableWidget.rowCount()} of {self.total_bangla_num} words")
            if self.contentWasEdited_ofTable_1 == False:
                self.contentWasEdited_ofTable_1 = False
                self.indicateTabContentChanged(0, False)
                self.setUnsevedSaveButton(False)
        if c_table == self.EnglaTableWidget:
            if len(self.my_engla_list) == 0:
                self.groupBox_8.setVisible(False) 
            # self.EnglaLabel.setText(f"Showing {c_table.rowCount()} of {self.total_engla_num} words")
            if self.contentWasEdited_ofTable_2 == False:
                self.contentWasEdited_ofTable_2 = False
                self.indicateTabContentChanged(1, False)
                self.setUnsevedSaveButton(False)
        if c_table == self.EnglishTableWidget:
            if len(self.my_english_list) == 0:
                self.groupBox_7.setVisible(False) 
            # self.EnglishLabel.setText(f"Showing {c_table.rowCount()} of {self.total_english_num} words")
            if self.contentWasEdited_ofTable_3 == False:
                self.contentWasEdited_ofTable_3 = False
                self.indicateTabContentChanged(2, False)
                self.setUnsevedSaveButton(False)        
        self.itemChangedByUndoFunc = False 

    def loadStuff(self):
        self.loadWords(wordsList, self.tableWidget)   # loading bangla words
        # self.loadWords(englaList, self.EnglaTableWidget)
        # self.loadWords(EnglishwordsList, self.EnglishTableWidget)
        self.loadAbbribiations()
        self.stufLoaded = True

        self.contentWasEdited_ofTable_1 = False
        self.contentWasEdited_ofTable_2 = False
        self.contentWasEdited_ofTable_3 = False
        self.contentWasEdited_ofTable_4 = False

        self.indicateTabContentChanged(0, False)
        self.setUnsevedSaveButton(False)
    def TestBanglish(self):
        row_count = self.tableWidget.rowCount()
        colum_count = self.tableWidget.columnCount()

        for r in range(row_count):
            try:    
                ban_word = self.tableWidget.item(r, 0).text()
                stableEngla = self.tableWidget.item(r, 1).text()
            except Exception:
                continue 

            try:
                banglish_list = main_banglish_converter(ban_word)

                item1 = QTableWidgetItem(banglish_list[0].format(0, 0))
                self.tableWidget.setItem(r,2, item1)

                if len(banglish_list) > 1:
                    item1 = QTableWidgetItem(banglish_list[1].format(0, 0))
                    self.tableWidget.setItem(r,3, item1)

                    if len(banglish_list) == 3:
                        item1 = QTableWidgetItem(banglish_list[2].format(0, 0))
                        self.tableWidget.setItem(r, 4, item1)

                if stableEngla !=  banglish_list[0]:
                    self.tableWidget.item(r, 2).setBackground(QColor(183, 28, 28, 255)) 
            except Exception:
                pass     
        pass    

    def eventFilter(self, obj, event):
        
        return super().eventFilter(obj, event)
        if obj is self.plainTextEdit:
            if event.type() == QtCore.QEvent.KeyPress:
                currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
                if event.text() not in banglaAlphabates and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete) and currentTable.currentColumn() == 0 and currentTable in [self.tableWidget, self.EnglaTableWidget]:
                    event.ignore()
                    return True 
                elif event.text() not in englishAlphabets and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete) and currentTable.currentColumn() != 0 and currentTable in [self.tableWidget, self.EnglaTableWidget]:
                    event.ignore()
                    return True 
                elif event.text() not in self.abbri_characters and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete) and currentTable.currentColumn() == 0 and currentTable in [self.tableWidget_3]:   
                    event.ignore()
                    return True
        return super().eventFilter(obj, event)

    def saveCurrentTableFunc(self):
        
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()

        txt = self.getTextFormTable(currentTable)

        # check if the list is fully loaded, if not the do this =====
        textFromList = ''
        if currentTable == self.tableWidget and len(self.my_bangla_list) != 0: # that's mean the list is not fully loaded
            for wrd in self.my_bangla_list[:]:
                textFromList += f"|{wrd}"
            txt = txt+textFromList

        if txt == "":
            self.showError("No content to save!")
            return
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
        elif currentTable == self.CustomTableWidget and self.contentWasEdited_ofTable_5 == True:
            path = CustomWordsPath
            self.contentWasEdited_ofTable_5 = False
        elif currentTable == self.ClipBoardtableWidget and self.contentWasEdited_ofTable_6 == True:
            path = clipBoardPath
            self.contentWasEdited_ofTable_6 = False    
        else:
            return
        self.writeDownContentsToFile(path, txt) 
        self.indicateTabContentChanged(self.tabWidget.currentIndex(), False)
        self.setUnsevedSaveButton(False)  

        for r in range(currentTable.rowCount()):
            currentTable.item(r, 0).setBackground(self.savedBGColor) 
        self.recognize_Changes(currentTable, False)  

        self.save_signal.emit(path)  

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
        try:
            self.currentItem = ""
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
            currentTable.setCurrentCell(0, 0, QItemSelectionModel.Current)
            if index == 0 and self.contentWasEdited_ofTable_1 == True or index == 1 and self.contentWasEdited_ofTable_2 == True or index == 2 and self.contentWasEdited_ofTable_3 == True or index == 3 and self.contentWasEdited_ofTable_4 == True or index == 4 and self.contentWasEdited_ofTable_5 == True or index == 5 and self.contentWasEdited_ofTable_6 == True:
                self.setUnsevedSaveButton(True)
            else:
                self.setUnsevedSaveButton(False)
        except Exception:
            pass        

    def setUnsevedSaveButton(self, state):
        if state == True:
            self.SavePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\nfont: 10pt "MS Shell Dlg 2l";\nbackground-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(8, 237, 255, 255), stop:1 rgba(255, 91, 253, 255));\nborder:1px solid rgb(253, 254, 254);\ncolor: rgb(255, 255, 255);\nborder-radius:2px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n}\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));"\n}')    
        else:
            self.SavePushButton.setStyleSheet('')    

    def clearUndoList(self):
        self.changes_for_tab_1 = []
        self.redoReserve_for_tab_1 = []

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
    def PasteFunc(self):
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        copied_text = (pc.paste())
        if len(copied_text) > 50 and currentTable in [self.tableWidget, self.EnglaTableWidget, self.EnglishTableWidget]:
            self.showError(f"Text of clipboard doesn't seem like a word!\nClipBoard Text:{pc.paste()}")
            return
        c_c = currentTable.currentColumn()
        text_in = self.identifi_str(copied_text) 
        if text_in == "bangla":  
            if currentTable in [self.tableWidget, self.EnglaTableWidget]:
                if c_c != 0:
                    return
            elif currentTable == self.tableWidget_3:
                c_c != 1
                return
            else:
                return
        elif text_in == "english":
            if currentTable == self.tableWidget or currentTable == self.EnglaTableWidget:
                if c_c == 0:
                    return     
        self.setCurrentCellText(currentTable, copied_text)
    def identifi_str(self, string):
        string_lang = "mixed"
        if string[0] in banglaAlphabates:
            string_lang = "bangla"
            for i in range(len(string)):
                if string[i] not in banglaAlphabates:
                    string_lang = "mixed"
                    break
        if string[0] in englishAlphabets:
            string_lang = "english"
            for i in range(len(string)):
                if string[i] not in englishAlphabets:
                    string_lang = "mixed"
                    break
        return string_lang

    def setCurrentCellText(self,currentTable, txt):
        c_item = QTableWidgetItem(txt.format(0, 0))
        currentTable.setItem(currentTable.currentRow() , currentTable.currentColumn(), c_item)    
    def currentTable(self):
        if self.tabWidget.currentIndex() == 0:
            return self.tableWidget, self.changes_for_tab_1,self.redoReserve_for_tab_1
        if self.tabWidget.currentIndex() == 1:
            return self.EnglaTableWidget,self.changes_for_tab_2,self.redoReserve_for_tab_2 
        if self.tabWidget.currentIndex() == 2:
            return self.EnglishTableWidget,self.changes_for_tab_3,self.redoReserve_for_tab_3 
        if self.tabWidget.currentIndex() == 3:
            return self.tableWidget_3,self.changes_for_tab_4,self.redoReserve_for_tab_4 
        if self.tabWidget.currentIndex() == 4:
            return self.CustomTableWidget, self.changes_for_tab_5, self.redoReserve_for_tab_5  
        if self.tabWidget.currentIndex() == 5:
            return self.ClipBoardtableWidget, self.changes_for_tab_6, self.redoReserve_for_tab_6                 

    def getTextFormTable(self, table):
        row_count = table.rowCount()
        colum_count = table.columnCount()
        
        text_ = ''
        for no in range(row_count):
            wordStr = ""
            for c in range(colum_count):
                try:    
                    txtFromColumn = (table.item(no, c).text())
                except Exception:
                    break    
                if txtFromColumn != "": 
                    if table == self.tableWidget_3:
                        wordStr += f"{txtFromColumn}::"
                    elif table == self.CustomTableWidget:
                        wordStr += f"{txtFromColumn}"  
                    elif table == self.ClipBoardtableWidget:
                        wordStr += f"{txtFromColumn}|*|\n" 
                    else:
                        wordStr += f"{txtFromColumn},"
            if wordStr != "":    
                if table == self.tableWidget_3:
                    text_ += f"{wordStr[:-2]}\n"
                elif table == self.CustomTableWidget:
                    text_ += f"{wordStr}\n" 
                elif table == self.ClipBoardtableWidget:
                    text_ += f"{wordStr[-4]}|@|\n"
                else:
                    text_ += f"{wordStr[:-1]}|"
        if table == self.ClipBoardtableWidget:
            return text_[:-4]
        else:                    
            return text_[:-1]
    def saveAsFunction(self):
        save_as_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file as',
            directory= 'C:\\Users\\ui\\Desktop',
            filter ='Text Document (*.txt)'
        )                               
        if not save_as_path:
            return
        else:
            try:
                currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
                
                textFromTable = self.getTextFormTable(currentTable)

                # self.ProgressGroupBox.setVisible(True)

                # self.getTextFromTableThread = GetTextThreadClass(currentTable)
                # self.getTextFromTableThread.return_text_signal.connect(self.saveTextToPath)
                # self.getTextFromTableThread.progration_signal.connect(self.setProgressFunc)
                # self.getTextFromTableThread.start()

                with io.open(save_as_path, "w", encoding="utf-8") as file:
                    file.write(textFromTable)

            except Exception as e:
                print(traceback.format_exc()) 

                self.showError(e)
    def stopSaveThread(self):
        try:
            self.getTextFromTableThread.stop()
        except Exception as e:
            print(e)    
    def setProgressFunc(self, prog):
        self.progressBar.setValue(prog)
    def saveTextToPath(self, textFromTable):
        try:
            with io.open(self.save_as_path, "w", encoding="utf-8") as file:
                file.write(textFromTable)
        except Exception:
            print(traceback.format_exc())   
            self.showError(traceback.format_exc()) 
    def setProgress(self, progress):
        pass            

    def loadCustom(self):
        for wrd in CustomWords:
            if wrd in ["", " "]:
                continue
            
            r = self.CustomTableWidget.rowCount()
            self.CustomTableWidget.insertRow(r)

            item = QTableWidgetItem(wrd.format(0, 0))
            self.CustomTableWidget.setItem(r,0, item)

    def loadAbbribiations(self):
        
        for ab in abris[:]:
            if ab == "":
                return
            parts = ab.split("::")
            if len(parts) == 0:
                return

            rowPosition = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(rowPosition)
            try:
                item1 = QTableWidgetItem(parts[0].format(0, 0))
                self.tableWidget_3.setItem(rowPosition,0, item1)

                item2 = QTableWidgetItem(parts[1].format(0, 0))
                self.tableWidget_3.setItem(rowPosition, 1, item2)
            except Exception as e:
                print(e)    
    def saveFunc(self):
        if self.contentWasEdited_ofTable_1 == True:
            path = banglaDictionaryPath
            self.contentWasEdited_ofTable_1 = False
            txt = self.getTextFormTable(self.tableWidget)
            self.writeDownContentsToFile(path, txt)
            self.indicateTabContentChanged(0, False)
            self.recognize_Changes(self.tableWidget, False)
        elif self.contentWasEdited_ofTable_2 == True:
            path = englaDictionaryPath
            self.contentWasEdited_ofTable_2 = False 
            txt = self.getTextFormTable(self.EnglaTableWidget)
            self.writeDownContentsToFile(path, txt)
            self.indicateTabContentChanged(1, False)
            self.recognize_Changes(self.EnglaTableWidget, False)
        elif self.contentWasEdited_ofTable_3 == True:
            path= englishDictionaryPath
            self.contentWasEdited_ofTable_3 = False 
            txt = self.getTextFormTable(self.EnglishTableWidget)
            self.writeDownContentsToFile(path, txt)  
            self.indicateTabContentChanged(2, False)
            self.recognize_Changes(self.EnglishTableWidget, False)
        elif self.contentWasEdited_ofTable_4 == True:
            path = AbbreviationsPath
            self.contentWasEdited_ofTable_4 = False  
            txt = self.getTextFormTable(self.tableWidget_3)
            self.writeDownContentsToFile(path, txt)  
            self.indicateTabContentChanged(3, False)
            self.recognize_Changes(self.tableWidget_3, False)
        elif self.contentWasEdited_ofTable_5 == True:
            path = CustomWordsPath
            self.contentWasEdited_ofTable_5 = False  
            txt = self.getTextFormTable(self.CustomTableWidget)
            self.writeDownContentsToFile(path, txt)  
            self.indicateTabContentChanged(4, False)
            self.recognize_Changes(self.CustomTableWidget, False)
        self.setUnsevedSaveButton(False)
        self.save_signal.emit("dkjf")
    def AddWordsFromFile(self):
        
        if any([self.contentWasEdited_ofTable_1, self.contentWasEdited_ofTable_2,self.contentWasEdited_ofTable_3,self.contentWasEdited_ofTable_4]):
            close = QMessageBox.question(self,
                                         "Quit?",
                                         "Save changes before adding words from file?",
                                         QMessageBox.Yes | QMessageBox.Cancel)
            if close == QMessageBox.Yes:
                self.saveFunc()
            if close == QMessageBox.Cancel:
                return

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
                   
                self.loadWords(wrd_list, currentTable, adding_from_newFile= True)
                if len(wrd_list) > 0:
                    self.recognize_Changes(currentTable)
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
            self.itemChangedByUndoFunc = True
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
            while (currentTable.rowCount() > 0):
                currentTable.removeRow(0)
            
            with io.open(path, "r", encoding="utf-8") as wordTxt:
                wordsSTR = wordTxt.read()
            wrdList = wordsSTR.split("|")

            self.loadWords(wrdList,currentTable)   
            self.itemChangedByUndoFunc = False
    def addFunc(self):
        self.itemChangedByUndoFunc = True
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()

        rowPosition = currentTable.currentRow() + 1
        if currentTable == self.tableWidget:
            if rowPosition < 12:
                rowPosition = 12
        if rowPosition > self.tableWidget.rowCount() - 50:
            self.Load_parcial_bangla()

        currentTable.insertRow(rowPosition)
        currentTable.setItem(rowPosition,0, QTableWidgetItem(""))
        currentTable.scrollToItem(currentTable.item(rowPosition, 0))
        currentTable.setCurrentItem(currentTable.item(rowPosition, 0))

        self.addRowUnDoReserveFunc(rowPosition, Current_changes_list, currentTable)  # , Current_changes_list, currentTable
        self.itemChangedByUndoFunc = False
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

        # recognizing Changes 
        try:    
            if row_contents[0] not in [" ", ""] and row_contents[1] not in [" ", ""]:
                self.recognize_Changes(currentTable)
        except Exception:
            pass        

    def selectAnItem(self, item):
        try:    
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
            currentTable.setCurrentItem(item)  
            currentTable.setCurrentCell(currentTable.currentRow(), currentTable.currentColumn()) 
            self.MatchedNumberLineEdit.setText(str(self.currentMatchedIndex+1) + "/"+str(len(self.matching_items)))
        except Exception:
            pass    
    def search(self, s):
        try:
            if not s:
                return

            currentTable, Current_changes_list, curren_redoReserve = self.currentTable()

            currentTable.setCurrentItem(None)
            if self.MatchCaseCheckBox.isChecked() == False:
                self.matching_items = currentTable.findItems(s, Qt.MatchContains)
            else:
                self.matching_items = currentTable.findItems(s, Qt.MatchExactly)   
            self.MatchedNumberLineEdit.setText(str(self.currentMatchedIndex+1) + "/"+str(len(self.matching_items)))
            if len(self.matching_items) == 0:
                self.MatchedNumberLineEdit.setText(str(0) + "/"+str(len(self.matching_items)))

            if self.matching_items:
                item = self.matching_items[0] 
                self.selectAnItem(item) 
        except Exception as e:
            print(e)  

    def search2(self, s):
        try:
            if not s:
                return
            currentTable, Current_changes_list, curren_redoReserve = self.currentTable() 
            currentTable.setCurrentItem(None)
            self.matching_items = currentTable.findItems(s, Qt.MatchExactly) 
            if self.matching_items:
                item = self.matching_items[0] 
                self.selectAnItem(item)
        except Exception:
            pass        

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
        
        if self.tableWidget.isVisible() == True or self.EnglaTableWidget.isVisible() == True :
            if self.tableWidget.currentColumn() == 0 or self.EnglaTableWidget.currentColumn() == 0 or self.tableWidget_3.currentColumn() == 0:
                if self.tableWidget.isVisible() == True:
                    table = self.tableWidget
                elif self.tableWidget_3.isVisible() == True:
                    table = self.tableWidget_3
                else:
                    table = self.EnglaTableWidget
                found_items = table.findItems(citem.text(), Qt.MatchExactly)
                if len(found_items) > 1:
                    table.itemChanged.disconnect(self.itemChangedFunc)
                    table.setItem(citem.row(), citem.column(), QTableWidgetItem(""))
                    item = found_items[0]
                    self.selectAnItem(item)
                    table.itemChanged.connect(self.itemChangedFunc)
                    return
        if self.EnglishTableWidget.isVisible() == True or self.tableWidget_3.isVisible() == True:  
            if self.EnglishTableWidget.isVisible() == True:
                table = self.EnglishTableWidget
            else:
                table = self.tableWidget_3
            found_items = table.findItems(citem.text(), Qt.MatchExactly)
            if len(found_items) > 1:
                table.itemChanged.disconnect(self.itemChangedFunc)
                table.setItem(citem.row(), citem.column(), QTableWidgetItem(""))
                item = found_items[0]
                self.selectAnItem(item)
                table.itemChanged.connect(self.itemChangedFunc)
                return         
        # print("inItemChangedFunc")
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()

        if self.itemChangedByUndoFunc == False:
            changedData = []
            if currentTable == self.tableWidget and currentTable.currentColumn() == 0:    
                self.setEnglaWord(currentTable)

                c_row = currentTable.currentRow()
                
                changedData.append("|*|added_New_File_content|*|")
                row_contents = []
                row_infos = [] # 1st row position 
                row_infos.append(c_row) # <-- Undo Reserve Function Call
                row_items = []
                for c in range(currentTable.columnCount()):
                    try:    
                        txtFromColumn = (currentTable.item(c_row, c).text()).replace(" ", "")
                    except Exception:
                        txtFromColumn = ""    
                    row_items.append(txtFromColumn)
                row_infos.append(row_items) # <-- row_contents 
                row_contents.append(row_infos)
                changedData.append(row_contents) 

            else:    
                changedData.append(self.currentItem)
                changedData.append(currentTable.currentRow())
                changedData.append(currentTable.currentColumn())

            Current_changes_list.insert(0, changedData)
            Current_changes_list = Current_changes_list[:50]
            self.currentItem = citem.text() 
            self.saveChangesForUndo_Redo(currentTable, Current_changes_list)

            
            self.recognize_Changes(currentTable)

            self.itemChangedByUndoFunc = True       
            
            self.itemChangedByUndoFunc = False  

            # print(Current_changes_list)

    def recognize_Changes(self, currentTable, state=True):  # if changes undone state == False 
        if state == True:    
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
            if currentTable == self.CustomTableWidget and self.contentWasEdited_ofTable_5 == False:
                self.contentWasEdited_ofTable_5 = True        
                self.indicateTabContentChanged(4,True)  
            if currentTable == self.ClipBoardtableWidget and self.contentWasEdited_ofTable_6 == False:
                self.contentWasEdited_ofTable_6 = True        
                self.indicateTabContentChanged(5,True)     

            self.setUnsevedSaveButton(True)
        else:
            if currentTable == self.tableWidget and self.contentWasEdited_ofTable_1 == True:
                self.contentWasEdited_ofTable_1 = False
                self.indicateTabContentChanged(0,False)
            if currentTable == self.EnglaTableWidget and self.contentWasEdited_ofTable_2 == True:
                self.contentWasEdited_ofTable_2 = False
                self.indicateTabContentChanged(1,False)
            if currentTable == self.EnglishTableWidget and self.contentWasEdited_ofTable_3 == True:
                self.contentWasEdited_ofTable_3 = False
                self.indicateTabContentChanged(2,False)
            if currentTable == self.tableWidget_3 and self.contentWasEdited_ofTable_4 == True:
                self.contentWasEdited_ofTable_4 = False        
                self.indicateTabContentChanged(3,False)
            if currentTable == self.CustomTableWidget and self.contentWasEdited_ofTable_5 == True:
                self.contentWasEdited_ofTable_5 = False       
                self.indicateTabContentChanged(4,False) 
            if currentTable == self.ClipBoardtableWidget and self.contentWasEdited_ofTable_6 == True:
                self.contentWasEdited_ofTable_6 = False      
                self.indicateTabContentChanged(5,False)       

            self.setUnsevedSaveButton(False)    
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
        currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        position = f"{currentTable.currentRow()+1}, {currentTable.currentColumn()+1}"
        self.RowColumnLineEdit.setText(position)
        return
        if currentTable in [self.tableWidget, self.EnglaTableWidget]: 
            if currentTable.currentColumn() != 0:
                currentTable.setItemDelegate(EnglishDelegate(currentTable)) 
            if currentTable.currentColumn() == 0:
                currentTable.setItemDelegate(BanglaDelegate(currentTable)) 
        if currentTable == self.tableWidget_3:
            if currentTable.currentColumn() == 0:
                self.tableWidget_3.setItemDelegate(AbbribiationDelegate(currentTable))
            if currentTable.currentColumn() != 0:
                self.tableWidget_3.setItemDelegate(AbbribiationContentDelegate(currentTable))
    def loadWords_from_thread(self, wordsList, tableWidget, adding_from_newFile = False):
        self.loadTable = tableWidget
        self.loadThread = LoadWordsThreadClass(wordsList, tableWidget, adding_from_newFile)
        # self.loadThread.insert_row_signal.connect(self.insertRowFunc)
        # self.loadThread.setRowItems_signal.connect(self.insertRowFunc) new 
        self.loadThread.prog_signal.connect(lambda prog: self.progressBar.setValue(prog))
        self.loadThread.finished_signal.connect(self.setNewWrds)
        self.ProgressGroupBox.setVisible(True)
        
        self.loadThread.start()

        self.CancelPushButton.setEnabled(True)
        self.CancelPushButton.clicked.connect(lambda:self.loadThread.stop())
    def setNewWrds(self,changedData):
        # print(changedData)
        multiDimenArray = changedData[1]  # [[row_pos,[c1_content, c2_content,..]],[row_pos,[row_contents]]]
        for word_infos in multiDimenArray:
            self.loadTable.insertRow(self.loadTable.rowCount())
        for word_infos in multiDimenArray:
            row_no = int(word_infos[0])-1
            r_c = word_infos[1]
            # self.loadTable.insertRow(self.loadTable.rowCount())
            c_no = 0
            for content in r_c:

                item = QTableWidgetItem((content).format(0, 0))
                self.loadTable.setItem(row_no,c_no, item)

                c_no += 1


        self.loadTable.scrollToBottom() 
        self.ProgressGroupBox.setVisible(False)
        
        if self.loadTable == self.tableWidget:    
            self.changes_for_tab_1.insert(0, changedData)
            self.changes_for_tab_1 = self.changes_for_tab_1[:50]

        if self.loadTable == self.EnglaTableWidget:    
            self.changes_for_tab_2.insert(0, changedData)
            self.changes_for_tab_2 = self.changes_for_tab_2[:50]

        if self.loadTable == self.EnglishTableWidget:    
            self.changes_for_tab_3.insert(0, changedData)
            self.changes_for_tab_3 = self.changes_for_tab_3[:50]    

        if self.loadTable == self.tableWidget_3:    
            self.changes_for_tab_4.insert(0, changedData)
            self.changes_for_tab_4 = self.changes_for_tab_4[:50]         
        self.itemChangedByUndoFunc = False
        self.CancelPushButton.setEnabled(False)    
    def insertRowFunc(self, wrd):
        # currentTable, Current_changes_list, curren_redoReserve = self.currentTable()
        # self.loadTable.insertRow(self.loadTable.rowCount())
        self.Progresslabel.setText(wrd)
    def loadWords(self, wordsList, tableWidget, adding_from_newFile = False):
        self.itemChangedByUndoFunc = True
        
        if adding_from_newFile:
            self.loadWords_from_thread(wordsList, tableWidget, adding_from_newFile = True)
            return
        
        changedData = []
        changedData.append("|*|added_New_File_content|*|") # ["|*|added_New_File_content|*|", [[row_pos,[row_contents]],....]]
        row_contents = []  

        for wrd in wordsList:
            wordArray = wrd.split(",")
            if wrd in [" ", ""]:   # < we have to put the if condition in here 
                continue

            # this code prevents adding dublicate words ==========
            # if adding_from_newFile == True:

            #     main_wrd = wordArray[0]
            #     found_items = tableWidget.findItems(main_wrd, Qt.MatchContains)
            #     if len(found_items) > 1:
            #         # print(main_wrd)
            #         continue

            rowPosition = tableWidget.rowCount()
            tableWidget.insertRow(rowPosition)
            row_infos = [] # 1st row position 
            row_infos.append(rowPosition) # <-- Undo Reserve Function Call
            row_items = []
            c = 0
            for w in wordArray[:5]:
                item = QTableWidgetItem(w.format(0, 0))
                row_items.append(w)
                tableWidget.setItem(rowPosition,c, item)
                c+=1
            row_infos.append(row_items) # <-- row_contents 
            row_contents.append(row_infos)
            
            if adding_from_newFile == False:    
                tableWidget.item(rowPosition, 0).setBackground(self.savedBGColor) 
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

    def convertTableToMultidimentionalArray(self, table):
        unique_words = []
        unique_multy_dymentional_array = []
        row_count = table.rowCount()
        colum_count = table.columnCount()
        for r in range(row_count):
            word_infos = []
            try:    
                main_wrd_or_row = table.item(r, 0).text()
            except Exception:
                continue    
            if main_wrd_or_row not in unique_words:
                unique_words.append(main_wrd_or_row)
                word_infos.append(main_wrd_or_row)   
            column_values = []    
            for c in range(colum_count)[1:]:
                try:
                    cc = table.item(r, c).text()
                except Exception:
                    cc = ""
                    break
                if cc not in [" ", ''] and cc not in column_values:
                    column_values.append(cc)  
            if len(column_values) != 0:
                word_infos.append(column_values)   
                unique_multy_dymentional_array.append(word_infos)           
      
        return unique_multy_dymentional_array
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
    def undo_func(self, current_table , changes_list, redoReserve_list):
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
                    try:    
                        itemText = (current_table.item(lastChange[1], lastChange[2])).text()
                    except Exception:
                        itemText = ""    
                    change.append(itemText)
                    change.append(lastChange[1])
                    change.append(lastChange[2])

                    redoReserve_list.insert(0, change)
                    
                    item = QTableWidgetItem((lastChange[0]).format(0, 0))
                    current_table.setItem(lastChange[1],lastChange[2], item)
                    # print(f"lastChange[0]:{lastChange[0]}")


                    current_table.setCurrentCell(lastChange[1], lastChange[2], QItemSelectionModel.Current)
                
                redoReserve_list = redoReserve_list[:50]
                changes_list.remove(lastChange)
                # print(changes_list)
                if len(changes_list) == 0:
                    self.recognize_Changes(current_table,False)
                return changes_list, redoReserve_list 

            except Exception as e:
                print(e)
                print(traceback.format_exc())
                pass
            self.itemChangedByUndoFunc = False
        else:
            self.recognize_Changes(current_table,False)
            pass 
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
            
            if len(redoReserve_list) == 0:
                self.recognize_Changes(current_table,True)
            return changes_list,redoReserve_list 
        else:
            self.recognize_Changes(current_table,True)
            pass      

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
    # def closeEvent(self, event):
    #     self.close()  
    def closeEvent(self, event):
        try:
            if any([self.contentWasEdited_ofTable_1, self.contentWasEdited_ofTable_2,self.contentWasEdited_ofTable_3,self.contentWasEdited_ofTable_4]):
                close = QMessageBox.question(self,
                                            "Quit?",
                                            "Do you want to save changes to this file?",
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if close == QMessageBox.Yes:
                    self.saveFunc()
                if close == QMessageBox.No:
                    pass
                if close == QMessageBox.Cancel:
                    event.ignore() 
                    return
            event.accept() 
        except Exception as e:
            print(traceback.format_exc())        
             
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        ex = wordManagerClass()
        ex.show()

        sys.exit(app.exec_())  
    except Exception as e:
        print(traceback.format_exc())           