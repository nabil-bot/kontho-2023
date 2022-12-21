# -*- coding:utf-8 -*-

from ast import Str
# from json.tool import main
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QGridLayout, QPushButton, QGroupBox
from PyQt5.QtCore import Qt, QSettings, pyqtSignal
from PyQt5 import QtCore
# import pyautogui
import ctypes
from PyQt5.QtGui import QPainter, QColor 
from pynput.keyboard import Controller, Key
from pynput import mouse
from PyQt5.QtWidgets import QWidget
keyboard = Controller()
import difflib
import io
import os
import threading
import winsound
from win32gui import GetWindowText, GetCursorPos, WindowFromPoint
from Main import similarityThread, wordThread
from LoadWords import wordsList,englaList,EnglishwordsList


from ahk import AHK
ahk = AHK()
import traceback

# with io.open('BanglishList.txt', "r", encoding="utf-8") as BAW:
#     BanglishList = (BAW.read()).split("|") 
# with io.open('EnglishWords.txt', "r", encoding="utf-8") as BAW:
#     EnglishWords = (BAW.read()).split("|") 
# with io.open('BanglishList.txt', "r", encoding="utf-8") as wordTxt:
#     wordsSTR = wordTxt.read()
# wordsList = wordsSTR.split("|")    
def similarity_ration_btween(first_string, second_string):
    temp = difflib.SequenceMatcher(None,first_string , second_string)
    return temp.ratio()    
User32 = ctypes.WinDLL('User32.dll')

greenStyleSheet = 'QPushButton{\n	font:  12pt "MS Shell Dlg 2";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(62, 255, 41, 255), stop:1 rgba(5, 240, 255, 255));\nborder:2px solid rgb(0, 187, 255);\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(9, 198, 250, 200));\nborder:1px solid rgb(0, 187, 255);}\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n}'





class similarityThread(QtCore.QThread):
    mostMatchedWords = QtCore.pyqtSignal(list)
    ruledOutSimiSignal = QtCore.pyqtSignal(bool)            # call preventer signal 1
    similarTheredIsRunningSignal = QtCore.pyqtSignal(bool, bool, str)  # call preventer signal 2
    def __init__(self, BanglaWordsofar = ""):
        super(similarityThread, self).__init__()
        self.is_running = True
        
        self.BanglaWordsofar = BanglaWordsofar
        self.ruledOutSimi = False
        self.brokenByNewCharacter = False
               
    def run(self):
        self.newCharacterIsPressed = False 
        self.similarTheredIsRunningSignal.emit(True, self.brokenByNewCharacter, self.BanglaWordsofar)
        self.similarWords = []
        self.heighestMatchedRatio = 0  
        for wrd in wordsList[:]: 
            try:
                wordArray = wrd.split(",")
                banglaWord = wordArray[0]
                englishWord = wordArray[1]
            except Exception:
                continue    
            if englishWord in ["", " "]:
                continue

            try:    
                if len(wordArray) == 1: #  or englishWord[0] != self.englishWordSofar[0]
                    continue
            except Exception:
                continue    
  
            similarity = self.similarity_ration_btween(banglaWord, self.BanglaWordsofar)   

            if len(self.BanglaWordsofar) < 5:
                minimumSimi = 0.7
            else:
                minimumSimi = 0.7   
            if similarity > minimumSimi:
                if similarity > self.heighestMatchedRatio:
                    self.similarWords.insert(0, banglaWord)
                    self.heighestMatchedRatio = similarity
                else:
                    self.similarWords.append(banglaWord)
                        
            if len(self.similarWords) > 9 or self.newCharacterIsPressed == True:
                if self.newCharacterIsPressed == True:
                    # print(f"new character break was called: for {englishWordSofar}")   
                    self.brokenByNewCharacter = True
                break
        if len(self.similarWords) == 0:
            self.ruledOutSimi = True
            self.ruledOutSimiSignal.emit(True)
            return
        self.mostMatchedWords.emit(self.similarWords)
        self.similarTheredIsRunningSignal.emit(False, self.brokenByNewCharacter, self.BanglaWordsofar)
        pass
    def similarity_ration_btween(self, x, y):
        seq = difflib.SequenceMatcher(None,x,y)
        d = seq.ratio()
        return d                
    def newCharecterIsPressedStateChange(self, state):
        self.newCharacterIsPressed = True
    def stop(self):
        self.is_running = False
        self.terminate()

class BanglawordThread(QtCore.QThread):
    matched_Word_signal = QtCore.pyqtSignal(list)
    newCherecterIspressed = QtCore.pyqtSignal(bool)
    def __init__(self):
        super(BanglawordThread, self).__init__()
        self.is_running = True
        self.ruledOut = False
        self.ruledOutSimi = False
        self.similarTheredIsRunning = False
        self.preWord = ""

    def run(self, BanglaWord=""):
        if BanglaWord in ["", " "]:
            return
        if self.similarTheredIsRunning == True:    
            self.newCherecterIspressed.emit(True)
        self.wordSofar = BanglaWord

        try:
            self.matchedWords = []
            self.newCharecterState = False
            if self.ruledOut == False:
                for wrd in wordsList[:]:
                    wordArray = wrd.split(",")
                    if len(wordArray) == 1:
                        continue
                    banglaWord = wordArray[0]
                    if banglaWord[:len(self.wordSofar)] == self.wordSofar:
                        self.matchedWords.append(banglaWord)

                    if len(self.matchedWords) > 9 or self.newCharecterState == True:
                        break  
                if len(self.matchedWords) == 0:   
                    self.ruledOut = True 

            if self.ruledOut == True and self.ruledOutSimi == False and self.similarTheredIsRunning == False:  # and self.similarTheredIsRunning == False
                self.similarityThread = similarityThread(BanglaWord)
                self.similarityThread.ruledOutSimiSignal.connect(self.ruledOutSimiStateChange)
                self.similarityThread.mostMatchedWords.connect(self.addSimiWordsFunc)
                self.similarityThread.similarTheredIsRunningSignal.connect(self.similarTheredIsRunningStateChange)
                self.similarTheredIsRunning = True
                self.newCherecterIspressed.connect(self.similarityThread.newCharecterIsPressedStateChange)
                self.similarityThread.start()
            self.matched_Word_signal.emit(self.matchedWords)


        except Exception as e:
            print(traceback.format_exc()) 
        
    def addSimiWordsFunc(self, simiWords):
        self.matchedWords = []
        for w in simiWords:
            self.matchedWords.append(w)
        self.matched_Word_signal.emit(self.matchedWords)     
    def similarTheredIsRunningStateChange(self, state, state2, englishWordSofar):
        self.similarTheredIsRunning = state
        if state == False and state2 == True:
            self.similarityThread = similarityThread(englishWordSofar)
            self.similarityThread.ruledOutSimiSignal.connect(self.ruledOutSimiStateChange)
            self.similarityThread.mostMatchedWords.connect(self.addSimiWordsFunc)
            self.similarityThread.similarTheredIsRunningSignal.connect(self.similarTheredIsRunningStateChange)
            self.similarTheredIsRunning = True
            self.newCherecterIspressed.connect(self.similarityThread.newCharecterIsPressedStateChange)
            self.similarityThread.start()

    def ruledOutSimiStateChange(self, state):
        self.ruledOutSimi = state
        self.similarTheredIsRunning = False
        
        # try:    
        #     self.similarityThread.stop()
        # except Exception:
        #     pass 

    def initFunc(self, sig):
        self.ruledOut = False
        self.ruledOutSimi = False
        self.similarTheredIsRunning = False
        try:    
            self.similarityThread.stop()
        except Exception:
            pass    

    def similarity_ration_btween(self, x, y):
        seq = difflib.SequenceMatcher(None,x,y)
        d = seq.ratio()
        return d
    def stop(self):
        self.is_running = False
        self.terminate()
  

class OSK_UI(QtWidgets.QMainWindow):
    bangla_word_signal = pyqtSignal(str)
    initBanglaThread_signal = pyqtSignal(str)
    
    word_signal = pyqtSignal(str, str, str)
    initThread_signal = pyqtSignal(str)
    def __init__(self):
        super(OSK_UI, self).__init__()
        uic.loadUi('.//Uis//oskUi.ui', self)

        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # | QtCore.Qt.WA_DeleteOnClose
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        User32.SetWindowLongW(int(self.winId()), -20, 134217728)
        self.CloseButton.clicked.connect(lambda: self.close())
        self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        self.clicked = False
        self.WinOsk.clicked.connect(self.oenWinOsk)
        self.tabWidget.currentChanged.connect(self.tabChangedFunc)
        self.SFXcheckBox.clicked.connect(self.sfxStatechanged)
        self.CurrentWord = ""
        self.RecomendationList = []
        self.banglaRecomendationBtns = [self.RB1,self.RB2,self.RB3,self.RB4,self.RB5,self.RB6,self.RB7,self.RB8,self.RB9, self.RB10]
        self.numDic = {'1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯','0':'০',}

        self.emojiLoaded = False
        self.characterLoaded = False

        self.RB1.clicked.connect(self.rb1Clicked)
        self.RB2.clicked.connect(self.rb2Clicked)
        self.RB3.clicked.connect(self.rb3Clicked)
        self.RB4.clicked.connect(self.rb4Clicked)
        self.RB5.clicked.connect(self.rb5Clicked)
        self.RB6.clicked.connect(self.rb6Clicked)
        self.RB7.clicked.connect(self.rb7Clicked)
        self.RB8.clicked.connect(self.rb8Clicked)
        self.RB9.clicked.connect(self.rb9Clicked)
        self.RB10.clicked.connect(self.rb10Clicked)
        
        self.OskHistory = QSettings("OSK_History")

        self.CharHistory = self.OskHistory.value("spChaHis")

        self.SFXcheckBox.setChecked(bool(self.OskHistory.value("sfxState")))

        self.capsLocked = False
        self.shiftState = False
        self.ctrlState = False
        self.altState = False
        self.winState = False

        self.pushButton_35.setStyleSheet("")
# banglakeyboard connectors ===========================
        self.Ao_pushButton.clicked.connect(lambda:self.logIn("অ"))
        self.Aa_pushButton.clicked.connect(lambda:self.logIn("আ"))
        self.pushButton_85.clicked.connect(lambda:self.logIn("ই"))
        self.pushButton_80.clicked.connect(lambda:self.logIn("ঈ"))
        self.pushButton_82.clicked.connect(lambda:self.logIn("উ"))
        self.pushButton_88.clicked.connect(lambda:self.logIn("ঊ"))
        self.pushButton_87.clicked.connect(lambda:self.logIn("ঋ"))
        self.pushButton_79.clicked.connect(lambda:self.logIn("এ"))
        self.pushButton_83.clicked.connect(lambda:self.logIn("ঐ"))
        self.pushButton_86.clicked.connect(lambda:self.logIn("ও"))
        self.pushButton_89.clicked.connect(lambda:self.logIn("ঔ"))
        self.pushButton_155.clicked.connect(lambda:self.logIn("া"))
        self.pushButton_156.clicked.connect(lambda:self.logIn("ি"))
        self.Deghi_pushButton.clicked.connect(lambda:self.logIn("ী"))
        self.pushButton_158.clicked.connect(lambda:self.logIn("ু"))
        self.pushButton_159.clicked.connect(lambda:self.logIn("ূ"))
        self.pushButton_160.clicked.connect(lambda:self.logIn("ৃ"))
        self.pushButton_161.clicked.connect(lambda:self.logIn("ে"))
        self.pushButton_162.clicked.connect(lambda:self.logIn("ৈ"))
        self.pushButton_163.clicked.connect(lambda:self.logIn("ো"))
        self.pushButton_164.clicked.connect(lambda:self.logIn("ৌ"))
        self.pushButton_101.clicked.connect(lambda:self.logIn("ক"))
        self.pushButton_91.clicked.connect(lambda:self.logIn("খ"))
        self.pushButton_96.clicked.connect(lambda:self.logIn("গ"))
        self.pushButton_133.clicked.connect(lambda:self.logIn("ঘ"))
        self.pushButton_138.clicked.connect(lambda:self.logIn("ঙ"))
        self.pushButton_148.clicked.connect(lambda:self.logIn("চ"))
        self.pushButton_93.clicked.connect(lambda:self.logIn("ছ"))
        self.pushButton_141.clicked.connect(lambda:self.logIn("জ"))
        self.pushButton_92.clicked.connect(lambda:self.logIn("ঝ"))
        self.pushButton_145.clicked.connect(lambda:self.logIn("ঞ"))
        self.pushButton_150.clicked.connect(lambda:self.logIn("ট"))
        self.pushButton_151.clicked.connect(lambda:self.logIn("ঠ"))
        self.pushButton_135.clicked.connect(lambda:self.logIn("ড"))
        self.pushButton_153.clicked.connect(lambda:self.logIn("ঢ"))
        self.pushButton_140.clicked.connect(lambda:self.logIn("ণ"))
        self.pushButton_143.clicked.connect(lambda:self.logIn("ত"))
        self.pushButton_104.clicked.connect(lambda:self.logIn("থ"))
        self.pushButton_132.clicked.connect(lambda:self.logIn("দ"))
        self.pushButton_99.clicked.connect(lambda:self.logIn("ধ"))
        self.pushButton_103.clicked.connect(lambda:self.logIn("ন"))
        self.pushButton_142.clicked.connect(lambda:self.logIn("প"))
        self.pushButton_131.clicked.connect(lambda:self.logIn("ফ"))
        self.pushButton_94.clicked.connect(lambda:self.logIn("ব"))
        self.pushButton_147.clicked.connect(lambda:self.logIn("ভ"))
        self.pushButton_100.clicked.connect(lambda:self.logIn("ম"))
        self.pushButton_95.clicked.connect(lambda:self.logIn("য"))
        self.pushButton_134.clicked.connect(lambda:self.logIn("র"))
        self.Lo_pushButton.clicked.connect(lambda:self.logIn("ল"))
        self.pushButton_90.clicked.connect(lambda:self.logIn("শ"))
        self.pushButton_97.clicked.connect(lambda:self.logIn("ষ"))
        self.pushButton_137.clicked.connect(lambda:self.logIn("স"))
        self.pushButton_146.clicked.connect(lambda:self.logIn("হ"))
        self.pushButton_149.clicked.connect(lambda:self.logIn("ড়"))
        self.pushButton_144.clicked.connect(lambda:self.logIn("ঢ়"))
        self.pushButton_98.clicked.connect(lambda:self.logIn("য়"))
        self.pushButton_105.clicked.connect(lambda:self.logIn("ৎ"))
        self.pushButton_136.clicked.connect(lambda:self.logIn("ং"))
        self.pushButton_139.clicked.connect(lambda:self.logIn("ঃ"))
        self.pushButton_152.clicked.connect(lambda:self.logIn("ঁ"))
        self.pushButton_154.clicked.connect(lambda:self.logIn("্"))
        self.pushButton_165.clicked.connect(lambda:self.logIn("্য"))
        self.pushButton_166.clicked.connect(lambda:self.logIn("্র"))
        self.pushButton_170.clicked.connect(lambda:self.logIn("০"))
        self.pushButton_167.clicked.connect(lambda:self.logIn("১"))
        self.pushButton_173.clicked.connect(lambda:self.logIn("২"))
        self.pushButton_169.clicked.connect(lambda:self.logIn("৩"))
        self.pushButton_171.clicked.connect(lambda:self.logIn("৪"))
        self.pushButton_172.clicked.connect(lambda:self.logIn("৫"))
        self.pushButton_168.clicked.connect(lambda:self.logIn("৬"))
        self.pushButton_175.clicked.connect(lambda:self.logIn("৭"))
        self.pushButton_174.clicked.connect(lambda:self.logIn("৮"))
        self.pushButton_176.clicked.connect(lambda:self.logIn("৯"))
        self.pushButton_186.clicked.connect(lambda:self.logIn("ক্ষ"))
        self.pushButton_193.clicked.connect(lambda:self.logIn("ঙ্ক"))
        self.pushButton_185.clicked.connect(lambda:self.logIn("ঙ্গ"))
        self.pushButton_187.clicked.connect(lambda:self.logIn("ঞ্চ"))
        self.pushButton_188.clicked.connect(lambda:self.logIn("ঞ্ছ"))
        self.pushButton_194.clicked.connect(lambda:self.logIn("ঞ্জ"))
        self.pushButton_191.clicked.connect(lambda:self.logIn("জ্ঞ"))
        self.pushButton_183.clicked.connect(lambda:self.logIn("হ্ম"))
        self.pushButton_190.clicked.connect(lambda:self.logIn("ষ্ণ"))
        self.pushButton_195.clicked.connect(lambda:self.logIn("ষ্ম"))
        self.pushButton_189.clicked.connect(lambda:self.logIn("ত্ত"))
        self.pushButton_177.clicked.connect(lambda:self.logIn("।"))
        self.pushButton_178.clicked.connect(lambda:self.logIn(","))
        self.pushButton_179.clicked.connect(lambda:self.logIn("?"))
        self.pushButton_180.clicked.connect(lambda:self.logIn(";"))
        self.pushButton_181.clicked.connect(lambda:self.logIn(":"))
        self.pushButton_182.clicked.connect(lambda:self.logIn("৳"))
        self.pushButton_192.clicked.connect(lambda:self.logIn("!"))
        self.pushButton_184.clicked.connect(lambda:self.logIn("@"))
        self.pushButton_196.clicked.connect(lambda:self.logIn("("))
        self.pushButton.clicked.connect(lambda:self.logIn(")"))
# /banglakeyboard connectors =========================== 
        self.pushButton_201.clicked.connect(self.spaceClicked)
        self.pushButton_198.clicked.connect(self.tabClicked)            
        self.pushButton_64.clicked.connect(self.tabClicked)
        self.pushButton_199.clicked.connect(self.BackSpaceClicked)
        self.pushButton_33.clicked.connect(self.BackSpaceClicked)
        self.pushButton_200.clicked.connect(self.deleteClicked)
        self.pushButton_78.clicked.connect(self.deleteClicked)
        self.pushButton_197.clicked.connect(self.EnterClicked)
        self.pushButton_47.clicked.connect(self.EnterClicked)
        self.pushButton_20.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_20.text())))
        self.pushButton_21.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_21.text())))
        self.pushButton_22.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_22.text())))
        self.pushButton_23.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_23.text())))
        self.pushButton_24.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_24.text())))
        self.pushButton_25.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_25.text())))
        self.pushButton_26.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_26.text())))
        self.pushButton_27.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_27.text())))
        self.pushButton_28.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_28.text())))
        self.pushButton_29.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_29.text())))
        self.pushButton_30.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_30.text())))
        self.pushButton_31.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_31.text())))
        self.pushButton_32.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_32.text())))
        self.pushButton_65.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_65.text())))
        self.pushButton_66.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_66.text())))
        self.pushButton_67.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_67.text())))
        self.pushButton_68.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_68.text())))
        self.pushButton_69.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_69.text())))
        self.pushButton_70.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_70.text())))
        self.pushButton_71.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_71.text())))
        self.pushButton_72.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_72.text())))
        self.pushButton_73.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_73.text())))
        self.pushButton_74.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_74.text())))
        self.pushButton_75.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_75.text())))
        self.pushButton_76.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_76.text())))
        self.pushButton_77.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_77.text())))
        self.pushButton_36.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_36.text())))
        self.pushButton_37.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_37.text())))
        self.pushButton_38.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_87.text())))
        self.pushButton_39.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_39.text())))
        self.pushButton_40.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_40.text())))
        self.pushButton_41.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_41.text())))
        self.pushButton_42.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_42.text())))
        self.pushButton_43.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_43.text())))
        self.pushButton_44.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_44.text())))
        self.pushButton_45.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_45.text())))
        self.pushButton_46.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_46.text())))
        self.pushButton_84.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_84.text())))
        self.pushButton_102.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_102.text())))
        self.pushButton_106.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_106.text())))
        self.pushButton_107.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_107.text())))
        self.pushButton_108.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_108.text())))
        self.pushButton_109.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_109.text())))
        self.pushButton_110.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_110.text())))
        self.pushButton_111.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_111.text())))
        self.pushButton_112.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_112.text())))
        self.pushButton_113.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_113.text())))       
        self.pushButton_38.clicked.connect(lambda: self.engishLogIn(str(self.pushButton_38.text())))     
        self.pushButton_114.clicked.connect(lambda: keyboard.tap(Key.up))
        self.pushButton_54.clicked.connect(lambda: keyboard.tap(Key.left))
        self.pushButton_55.clicked.connect(lambda: keyboard.tap(Key.down))
        self.pushButton_56.clicked.connect(lambda: keyboard.tap(Key.right))
        self.pushButton_48.clicked.connect(lambda: keyboard.tap(Key.home))
        self.pushButton_116.clicked.connect(lambda: keyboard.tap(Key.end))
        self.pushButton_19.clicked.connect(self.escFunc)
        self.pushButton_52.clicked.connect(self.spaceClicked)
        # functions ==========================================================
        self.pushButton_2.clicked.connect(lambda: keyboard.tap(Key.f1))
        self.pushButton_3.clicked.connect(lambda: keyboard.tap(Key.f2))
        self.pushButton_18.clicked.connect(lambda: keyboard.tap(Key.f3))
        self.pushButton_17.clicked.connect(lambda: keyboard.tap(Key.f4))
        self.pushButton_16.clicked.connect(lambda: keyboard.tap(Key.f5))
        self.pushButton_15.clicked.connect(lambda: keyboard.tap(Key.f6))
        self.pushButton_14.clicked.connect(lambda: keyboard.tap(Key.f7))
        self.pushButton_13.clicked.connect(lambda: keyboard.tap(Key.f8))
        self.pushButton_12.clicked.connect(lambda: keyboard.tap(Key.f9))
        self.pushButton_11.clicked.connect(lambda: keyboard.tap(Key.f10))
        self.pushButton_10.clicked.connect(lambda: keyboard.tap(Key.f11))
        self.pushButton_9.clicked.connect(lambda: keyboard.tap(Key.f12))
        
        # /function ==========================================================
        self.changeStatedStylesheet = "background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1.197, fx:0.489, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(72, 173, 255, 255));"
        # media controll =====================================================
        self.pushButton_8.clicked.connect(lambda: keyboard.tap(Key.media_volume_down))
        self.pushButton_7.clicked.connect(lambda: keyboard.tap(Key.media_volume_up))
        self.pushButton_6.clicked.connect(lambda: keyboard.tap(Key.media_previous))
        self.pushButton_5.clicked.connect(lambda: keyboard.tap(Key.media_play_pause))
        self.pushButton_4.clicked.connect(lambda: keyboard.tap(Key.media_next))
        # /media controll   ===================================================
        
        self.pushButton_35.clicked.connect(self.CapsClicked)

        self.latter_btns = [self.pushButton_65, self.pushButton_66,self.pushButton_67,self.pushButton_68,self.pushButton_69,
            self.pushButton_70,self.pushButton_71,self.pushButton_72,self.pushButton_73,self.pushButton_74,self.pushButton_36,self.pushButton_37,self.pushButton_38,self.pushButton_39,self.pushButton_40,self.pushButton_41,self.pushButton_42,self.pushButton_43,self.pushButton_44,
            self.pushButton_84, self.pushButton_102,self.pushButton_106, self.pushButton_107, self.pushButton_108, self.pushButton_109, self.pushButton_110]

        self.norCha = ["`","1","2","3","4","5","6","7","8","9","0","-","=","[","]",' \ ', ";", "'", ",", ".", "/"]
        self.shiftCha = ["~","!","@","#","$","%","^","&&","*","(",")","_","+", "{", "}", "|", ":", '"', "<", ">", "?"]
        self.karList = ["া","ি","ী","ু","ূ","ৃ","ে","ৈ","ো","ৌ"]
        self.btsForNorChar = [self.pushButton_20,self.pushButton_21,self.pushButton_22,self.pushButton_23,self.pushButton_24,
                self.pushButton_25,self.pushButton_26,self.pushButton_27,self.pushButton_28,self.pushButton_29,self.pushButton_30,self.pushButton_31,self.pushButton_32,self.pushButton_75,self.pushButton_76,self.pushButton_77,self.pushButton_45,self.pushButton_46, self.pushButton_111,self.pushButton_112,self.pushButton_113]    
        self.pushButton_81.clicked.connect(self.shiftClicked)
        self.pushButton_115.clicked.connect(self.shiftClicked)

        self.pushButton_49.clicked.connect(self.ctrlClicked)
        self.pushButton_51.clicked.connect(self.altClicked)
        self.pushButton_50.clicked.connect(self.winClicked)
        self.pushButton_53.clicked.connect(self.altClicked)

        self.pushButton_57.clicked.connect(lambda:ahk.run_script(str("send, {AppsKey}"), blocking=False))

        characterList = [self.pushButton_20,
        self.pushButton_21,self.pushButton_22,self.pushButton_23,self.pushButton_24,self.pushButton_25,self.pushButton_26,
        self.pushButton_27,self.pushButton_28,self.pushButton_29,self.pushButton_30,self.pushButton_31,self.pushButton_32,
        self.pushButton_65,self.pushButton_84, self.pushButton_102,self.pushButton_106,self.pushButton_107,
        self.pushButton_68,self.pushButton_69,self.pushButton_70,self.pushButton_71,self.pushButton_72,self.pushButton_73,
        self.pushButton_74,self.pushButton_75,self.pushButton_76,self.pushButton_77,self.pushButton_66,self.pushButton_67,
        self.pushButton_36,self.pushButton_37,self.pushButton_38,self.pushButton_39,self.pushButton_40,
        self.pushButton_41,self.pushButton_42,self.pushButton_43,self.pushButton_44,self.pushButton_45,self.pushButton_46,
        self.pushButton_108,self.pushButton_109,self.pushButton_110,self.pushButton_111,self.pushButton_112,self.pushButton_113, self.pushButton_101, self.pushButton_91, self.pushButton_96, self.pushButton_133, self.pushButton_138, self.pushButton_148, self.pushButton_93, self.pushButton_141, self.pushButton_92, self.pushButton_145, self.pushButton_150, self.pushButton_151, self.pushButton_135, self.pushButton_153, self.pushButton_140, self.pushButton_143, self.pushButton_104, self.pushButton_132, self.pushButton_99, self.pushButton_103, self.pushButton_142, self.pushButton_131, self.pushButton_94, self.pushButton_147, self.pushButton_100, self.pushButton_95, self.pushButton_134, self.Lo_pushButton, self.pushButton_90, self.pushButton_97, self.pushButton_137, self.pushButton_146, self.pushButton_149, self.pushButton_144, self.pushButton_98, self.pushButton_105, self.pushButton_136, self.pushButton_139, self.pushButton_152
        
        ]
        for btn in characterList:
            try:    
                btn.setStyleSheet(greenStyleSheet)
            except Exception:
                pass    

        self.recentChaBtns = [self.RecentCha, self.RecentCha_2,self.RecentCha_3,self.RecentCha_4,self.RecentCha_5,self.RecentCha_6,self.RecentCha_7,self.RecentCha_8,self.RecentCha_9,self.RecentCha_10,self.RecentCha_11,self.RecentCha_12,self.RecentCha_13,self.RecentCha_14,self.RecentCha_15,self.RecentCha_16,self.RecentCha_17,self.RecentCha_18,self.RecentCha_19,self.RecentCha_20
        ]
        for cha, btn in zip(self.CharHistory, self.recentChaBtns):
            btn.setText(cha)
        ser = 0
        for btn in self.recentChaBtns:
            btn.clicked.connect(lambda ch, text=ser: self.recChaClicked(text))  
            ser +=1  
        
        # self.loadCharacters() 
        
        

        self.wordSoFar = ""

        self.englishWordSofar = "" 
        self.wordSofar = ""
        self.previous_word = ""
        self.formar_previous_word = ""
        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = ""

        self.previousLetter = ""
    
        self.MouseListener = mouse.Listener(on_click = self.on_click)
        self.MouseListener.start()
        
        self.BanglawordThread = BanglawordThread()
        self.BanglawordThread.matched_Word_signal.connect(self.populateBanglaWords)
        self.bangla_word_signal.connect(self.BanglawordThread.run)
        self.initBanglaThread_signal.connect(self.BanglawordThread.initFunc)
        self.BanglawordThread.start()


        self.wordThread_ = wordThread()
        self.wordThread_.matched_Word_signal.connect(self.populateBanglaWords)
        self.word_signal.connect(self.wordThread_.run)
        self.initThread_signal.connect(self.wordThread_.initFunc)
        self.wordThread_.start()

    def on_click(self, x, y, button, pressed):
        if GetWindowText(WindowFromPoint(GetCursorPos())) != self.windowTitle():
            self.CurrentWord = ""
            self.recomendFunc()
            self.initState() 
            self.initThread_signal.emit("init")
            pass
    
    def trim(self, l):
        self.CurrentWord = self.CurrentWord[:-l]
        for i in range(l):  
            keyboard.tap(Key.backspace)

    def sendBanglishFor(self, key):
        try: 
            if str(key) == "Key.shift" and self.shiftKeyBlocked == False:
                for i in self.keysToUnlock:
                    try:    
                        kb2.unblock_key(i)
                    except Exception:
                        pass    
                self.shiftKeyBlocked = True    

            if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"] and self.keysBlocked == True: 
                kb2.unhook_all()
                self.keysBlocked = False
                self.initialize()
                return    
            if str(key) == "'.'":
                kb.type("।")
                self.initialize()
                return
            if str(key) == "Key.space":
                self.initialize()
        
            if str(key) == "Key.backspace":
                if wordSofar != "":    
                    if len(wordSofar) > 1:   
                        wordSofar = wordSofar[:-1]
                        englishWordSofar = englishWordSofar[:-1]
                    else:
                        self.initialize() 

            bnglaKey = ""
            stringKey = (str(key)).replace("'", "")

            if stringKey in self.numDic:
                keyboard.type(self.numDic[stringKey])
                self.initialize()
                return
            if stringKey == "a":
                if self.CurrentWord == "":
                    bnglaKey = "আ"
                elif self.previous_word == "a":
                    bnglaKey = "্য"
                else:
                    if self.CurrentWord[-1] == "ং":
                        self.trim(1)
                        bnglaKey = "ঙা"
                    else:
                        bnglaKey = "া"
            if stringKey == "b":
                if self.previous_word in ["b","r"]:
                    bnglaKey= "্ব"
                else:
                    bnglaKey= "ব"
            if stringKey == "c":
                if self.previous_word in ["c","h"]:
                    bnglaKey = "্চ"
                elif self.previous_word in ["n","G"]:
                    bnglaKey = "ঞ্চ"
                    self.trim(1)
                else:
                    bnglaKey= "চ"  
            if stringKey == "d":
                if self.previous_word in ["n","b", "d", "l", "k", "m"]:
                    bnglaKey = "্দ"    
                else:
                    bnglaKey = "দ"    
            if stringKey == "D":
                if self.previous_word in ["n","D", "l"]:
                    bnglaKey = "্ড"    
                else:
                    bnglaKey = "ড"
            if stringKey == "e":
                if self.CurrentWord == "":
                    bnglaKey = "এ"
                elif self.previous_word == 't' and self.formar_previous_word == 'n':
                    bnglaKey = "তে"
                    self.trim(2)
                else:
                    bnglaKey = "ে"
            if stringKey == "E":
                if self.CurrentWord == "":
                    bnglaKey = "ঈ"
                else:
                    bnglaKey = "ী"
            if stringKey == "f" or stringKey == "F":
                bnglaKey = "ফ"
            if stringKey == "g":
                if self.previous_word == "n" or self.previous_word == "N":
                    if self.previous_word == "n": 
                        bnglaKey= "ং"
                    if self.previous_word == "N": 
                        bnglaKey= "ঙ"
                    self.trim(1)
                elif self.previous_word == "r": 
                    bnglaKey= "্গ"
                elif self.previous_word == "g":
                    bnglaKey= "জ্ঞ" 
                    self.trim(1)
                else: 
                    bnglaKey= "গ" 
            if stringKey == "G":
                if self.previous_word == "N":
                    bnglaKey= "ঞ" 
                    self.trim(1) 
                else: 
                    bnglaKey= "গ" 
            if stringKey == "h":
                if self.previous_word == "K":
                    bnglaKey = "্ষ"
                elif self.previous_word == "c":
                    bnglaKey= "ছ" 
                    self.trim(1)
                elif self.previous_word == "j":
                    bnglaKey = "ঝ" 
                    self.trim(1) 
                elif self.previous_word == "k": 
                    if self.formar_previous_word == "k":
                        bnglaKey = "ষ"     
                    else:
                        bnglaKey = "খ"
                        self.trim(1)    
                elif self.previous_word == "p":
                    bnglaKey = "ফ"
                    self.trim(1)  
                elif self.previous_word == "g":
                    bnglaKey = "ঘ"
                    self.trim(1)  
                elif self.previous_word == "d":
                    if self.formar_previous_word == "g":
                        bnglaKey = "্ধ"
                        self.trim(1)
                    else:
                        bnglaKey = "ধ"
                    self.trim(1)  
                elif self.previous_word == "D":
                    bnglaKey = "ঢ"
                    self.trim(1)
                elif self.previous_word == "b":
                    if self.formar_previous_word == "d":
                        bnglaKey = "্ভ"
                    else:
                        bnglaKey = "ভ"
                    self.trim(1)
                elif self.previous_word == "R":
                    bnglaKey = "ঢ়"
                    self.trim(1) 
                elif self.previous_word == "s":
                    bnglaKey = "শ"
                    self.trim(1)
                elif self.previous_word == "S":
                    self.trim(1)
                    bnglaKey = "ষ"
                    
                elif self.previous_word == "t":
                    bnglaKey = "থ"
                    self.trim(1)  
                elif self.previous_word == "T":
                    bnglaKey = "ঠ"
                    self.trim(1)  
                elif self.previous_word == "v":
                    pass
                else:
                    bnglaKey = "হ" 
            if stringKey == "H":
                if self.previous_word == "K":
                    bnglaKey = "্ষ"
                elif self.previous_word == "T":
                    bnglaKey = "ৎ"
                    self.trim(1)
            if stringKey == "i":
                if self.CurrentWord == "" or self.previous_word == "a":
                    bnglaKey= "ই"
                elif self.previous_word == "r" and self.formar_previous_word == "r":
                    bnglaKey= "ৃ"
                    self.trim(3)
                elif self.previous_word == "o" or self.previous_word == "O":
                    if self.formar_previous_word == "":
                        bnglaKey= "ঐ"
                        self.trim(1)
                    else:
                        bnglaKey= "ৈ"
                else:
                    bnglaKey= "ি"
            if stringKey == "I":
                if self.previous_word == "o" or self.previous_word == "O":
                    if self.formar_previous_word == "":
                        bnglaKey= "ঐ"
                        self.trim(1)
                    else:
                        bnglaKey= "ৈ"
                elif wordSofar == "" or wordSofar[-1] in self.karList:
                    bnglaKey = "ঈ"    
                else:
                    bnglaKey = "ী"
            if stringKey == "j":
                if self.previous_word == "n":
                    bnglaKey= "ঞ্জ"
                    self.trim(1)
                elif self.previous_word in ["j", "J"]:
                    bnglaKey= "্জ" 
                else:
                    bnglaKey= "জ"
            if stringKey == "J":
                bnglaKey= "ঝ"    
            if stringKey == "k":
                if self.previous_word in ["k", "K", "l", "s", "r"]:
                    bnglaKey = "্ক"
                elif self.previous_word == "h" and self.formar_previous_word == "s":
                    bnglaKey = "ষ্ক"
                    self.trim(1)  
                elif self.previous_word == "n":
                    bnglaKey = "ঙ্ক"
                    self.trim(1)      
                elif self.previous_word == "g" and self.formar_previous_word == "N":
                    bnglaKey = "্ক"
                else:
                    bnglaKey = "ক"
            if stringKey == "K":
                bnglaKey = "ক"
            if stringKey == "l":
                if self.previous_word == "l":
                    bnglaKey= "্ল"
                else:
                    bnglaKey= "ল"         
            if stringKey == "m":
                if self.previous_word == "h":
                    bnglaKey = "হ্ম"
                    self.trim(1) 
                elif self.previous_word in ["d", "l", "n", "r", "s", "t", "g", "m"]:
                    bnglaKey = "্ম" 
                else:
                    bnglaKey = "ম" 
            if stringKey == "M":
                bnglaKey = "মো" 
            if stringKey == "n":
                # print(self.previous_word)
                if self.previous_word in ["n", "p", "t", "g", "h", "m", "s", "r"]:
                    bnglaKey= "্ন"
                else:
                    bnglaKey= "ন"      
            if stringKey == "N":
                if self.previous_word == "r":
                    bnglaKey = "্ণ" 
                else:
                    bnglaKey = "ণ" 
            if stringKey == "o":
                # print("in o if")
                if self.previous_word == self.formar_previous_word != "": 
                    if self.previous_word == "g":
                        bnglaKey = "্য"
                elif self.CurrentWord == "":
                    bnglaKey = "অ"
                elif self.previous_word == "g" and self.formar_previous_word == "n":
                    bnglaKey = "ঙ্গ"
                    self.trim(1)  
                # elif self.previous_word == "h" and self.formar_previous_word == "r":   
                elif self.previous_word in ["p", "s", "t", "T", "c", "d", "z", "m", "O", "k", "b", "n", "r", "g", "j", "l", "h", "y"]: 
                    self.previous_word = "o"
                    pass 
                else:
                    bnglaKey = "ো"
            if stringKey == "O":
                if self.CurrentWord == "":
                    bnglaKey = "ও"
                else:
                    bnglaKey = "ো"
            if stringKey in ["p", "P"] :
                if self.previous_word == "s":
                    bnglaKey = "্প"
                else:
                    bnglaKey = "প"
            if stringKey in ["q", "Q"]:
                bnglaKey = "ক"
            if stringKey == "r":
                if self.previous_word in ["t","b","k","f","g","h","j","c","d","n","p","s","v","T","D","z","F", "m"]:
                    bnglaKey = "্র" 
                else:
                    bnglaKey = "র"
            if stringKey == "R":
                if self.CurrentWord == "":
                    bnglaKey = "ঋ" 
                else:
                    bnglaKey = "ড়"  
            if stringKey == "s":
                if self.previous_word == "r":
                    bnglaKey = "্স" 
                elif self.previous_word == "H":
                    bnglaKey = "্"
                    self.trim(1)
                else:
                    bnglaKey = "স"  
            if stringKey == "S":
                bnglaKey = "শ" 
            if stringKey == "t":
                if self.previous_word in ["n","t", "p", "r"]:
                    bnglaKey = "্ত"
                elif self.previous_word == "k": 
                    bnglaKey = "ক্ত"
                    self.trim(1)
                elif self.previous_word == "s":
                    bnglaKey = "স্ত"
                    self.trim(1)
                else:
                    bnglaKey = "ত"
            if stringKey == "T":
                # print(self.CurrentWord)
                if self.previous_word in ["h", "k","l","n", "p", "s","T"] and self.formar_previous_word not in ["g"]:
                    bnglaKey = "্ট"
                else:
                    bnglaKey = "ট"
            if stringKey == "u":
                if self.previous_word in ["O", "o"]:
                    bnglaKey = "ঔ"
                    self.trim(1)  
                elif self.CurrentWord == "":
                    bnglaKey = "উ"  
                else:
                    bnglaKey = "ু"      
            if stringKey == "U":
                if self.CurrentWord == "":
                    bnglaKey = "ঊ"
                elif self.previous_word == "O":
                    if self.formar_previous_word == "":
                        bnglaKey = "ঔ"
                    else:
                        bnglaKey = "ৌ"
                    self.trim(1) 
                else:
                    bnglaKey = "ূ"
            if stringKey in ["v", "V"] : 
                if self.previous_word in ["m", "d"]:
                    bnglaKey = "্ভ"
                else:
                    bnglaKey = "ভ"
            if stringKey in  ["w", "W"]:
                if self.CurrentWord == "":
                    bnglaKey = "ও"
                else:
                    bnglaKey = "্ব"
            if stringKey in  ["y", "Y"]:
                    bnglaKey = "য়"
            if stringKey == "z":
                if self.previous_word == "r":
                    bnglaKey== "্য"
                else:
                    bnglaKey== "য"
            if stringKey == "Z":
                bnglaKey== "্য"   
            if bnglaKey != "" or stringKey == "o":
                keyboard.type(str(bnglaKey))
                self.CurrentWord += str(bnglaKey)
                self.formar_previous_formar_previous_word = self.previous_formar_previous_word
                self.previous_formar_previous_word = self.formar_previous_word
                self.formar_previous_word = self.previous_word
                self.previous_word = stringKey
                self.englishWordSofar += stringKey

                self.word_signal.emit(self.CurrentWord, self.englishWordSofar, "bangla")
            self.initState()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        pass

        pass
    def populateBanglaWords(self, words):
        for btn in self.banglaRecomendationBtns:
            btn.setText("")
        for wrd, btn in zip(words, self.banglaRecomendationBtns):
            btn.setText(wrd)
        pass
    def rb1Clicked(self):
        self.completFunc(str(self.RB1.text()))
    def rb2Clicked(self):
        self.completFunc(str(self.RB2.text())) 
    def rb3Clicked(self):
        self.completFunc(str(self.RB3.text()))   
    def rb4Clicked(self):
        self.completFunc(str(self.RB4.text()))  
    def rb5Clicked(self):
        self.completFunc(str(self.RB5.text()))    
    def rb6Clicked(self):
        self.completFunc(str(self.RB6.text()))  
    def rb7Clicked(self):
        self.completFunc(str(self.RB7.text())) 
    def rb8Clicked(self):
        self.completFunc(str(self.RB8.text()))    
    def rb9Clicked(self):
        self.completFunc(str(self.RB9.text()))
    def rb10Clicked(self):
        self.completFunc(str(self.RB10.text()))    
    def recChaClicked(self, ser):
        try:
            cha = self.CharHistory[int(ser)]
        except Exception as e:
            print(cha)
            print(e) 
            cha = ""    

        try:    
            keyboard.type(cha) 
        except Exception:     
            with io.open("dalal.ahk", 'w', encoding="utf-16") as f:
                f.write(f"send,{cha}")
            os.system('AutoHotkeyU64.exe "dalal.ahk"')
    def logEmojie(self, Cha): 
        try:    
            keyboard.type(Cha) 
        except Exception:     
            with io.open("dalal.ahk", 'w', encoding="utf-16") as f:
                f.write(f"send,{Cha}")
            os.system('AutoHotkeyU64.exe "dalal.ahk"')
        self.initState()
    def tabChangedFunc(self, index):
        r = 0
        c = 0
        for btn in self.banglaRecomendationBtns:
            if self.tabWidget.currentIndex() == 0:    
                self.gridLayout_3.addWidget(btn,r, c)
            elif self.tabWidget.currentIndex() == 1:    
                self.gridLayout_5.addWidget(btn,r, c)
            c+=1
            if c == 5:
                c= 0
                r+=1
        self.CurrentWord = ""
        self.recomendFunc()

        if index == 2 and self.characterLoaded == False:
            self.loadCharacters()
            self.characterLoaded = True
        if index == 3 and self.emojiLoaded == False:
            self.loadEmojies()
            self.emojiLoaded = True
                
    def initState(self):
        if self.shiftState == True:
            self.shiftClicked()
        if self.ctrlState == True:
            self.ctrlClicked()  
        if self.altState == True:
            self.altClicked() 
        if self.winState == True:
            self.winClicked()
           
    def escFunc(self):
        keyboard.tap(Key.esc)
        self.initState()     
    def logCha(self, Cha): 
        try:    
            keyboard.type(Cha) 
        except Exception:     
            with io.open("dalal.ahk", 'w', encoding="utf-16") as f:
                f.write(f"send,{Cha}")
            os.system('AutoHotkeyU64.exe "dalal.ahk"')
        
        if self.CharHistory[0] != Cha:    
            self.CharHistory.insert(0, Cha)

            self.CharHistory = self.CharHistory[0:20]

            for cha, btn in zip(self.CharHistory, self.recentChaBtns):
                btn.setText(cha)
                text = btn.text()
             
        self.initState()
    def winClicked(self):
        if self.winState == False:
            keyboard.press(Key.cmd)
            self.winState = True
            self.pushButton_50.setStyleSheet(self.changeStatedStylesheet)  
            return
        if self.winState == True:
            keyboard.release(Key.cmd)
            self.winState = False
            self.pushButton_50.setStyleSheet("")
            return    
    def altClicked(self):
        if self.altState == False:
            keyboard.press(Key.alt)
            self.altState=True
            self.pushButton_51.setStyleSheet(self.changeStatedStylesheet)
            self.pushButton_53.setStyleSheet(self.changeStatedStylesheet)
            return
        if self.altState == True:
            keyboard.release(Key.alt)
            self.altState=False
            self.pushButton_51.setStyleSheet("")
            self.pushButton_53.setStyleSheet("")
    def ctrlClicked(self):
        if self.ctrlState == False:
            keyboard.press(Key.ctrl)
            self.ctrlState = True
            self.pushButton_49.setStyleSheet(self.changeStatedStylesheet)
            return
        if self.ctrlState == True:
            keyboard.release(Key.ctrl)
            self.ctrlState = False
            self.pushButton_49.setStyleSheet("")
            return   
    def shiftClicked(self):
        if self.shiftState == False:
            keyboard.press(Key.shift)
            for btn in self.latter_btns:
                btnText = (btn.text()).upper()
                btn.setText(btnText)
            for btn, cha in zip(self.btsForNorChar, self.shiftCha):
                btn.setText(cha)
            self.shiftState = True
            self.pushButton_81.setStyleSheet(self.changeStatedStylesheet)    
            self.pushButton_115.setStyleSheet(self.changeStatedStylesheet)    


            return
        if self.shiftState == True:
            keyboard.release(Key.shift)
            
            for btn in self.latter_btns:
                btnText = (btn.text()).lower()
                btn.setText(btnText)  
            for btn, cha in zip(self.btsForNorChar, self.norCha):
                btn.setText(cha)
            self.shiftState = False
            self.pushButton_81.setStyleSheet("")    
            self.pushButton_115.setStyleSheet("")    

            return      
    def CapsClicked(self):    
        if self.capsLocked == False:
            for btn in self.latter_btns:
                btnText = (btn.text()).upper()
                btn.setText(btnText)

            for btn, cha in zip(self.btsForNorChar, self.shiftCha):
                btn.setText(cha)

            self.pushButton_35.setStyleSheet(self.changeStatedStylesheet)    
            self.capsLocked = True
            return

        if self.capsLocked == True:
            for btn in self.latter_btns:
                btnText = (btn.text()).lower()
                btn.setText(btnText)  
            for btn, cha in zip(self.btsForNorChar, self.norCha):
                btn.setText(cha)

            self.pushButton_35.setStyleSheet("")    
            self.capsLocked = False  
            return  
    def engishLogIn(self, char): 
        if self.BanglishCheckBox.isChecked() == False or any([self.ctrlState, self.altState, self.winState]):
            if any([self.ctrlState, self.altState, self.winState]):
                keyboard.tap(char)  
            else:
                keyboard.type(char)
                self.CurrentWord += char
                self.recomendFunc()

            self.initState()     
        elif self.BanglishCheckBox.isChecked() == True:
            self.sendBanglishFor(char) 
                
    def EnterClicked(self):
        keyboard.tap(Key.enter)
        self.initState()
    def deleteClicked(self):
        keyboard.tap(Key.delete)
        self.initState()
    def BackSpaceClicked(self):
        keyboard.tap(Key.backspace)
        if self.CurrentWord != "": 
            try:
                self.CurrentWord = self.CurrentWord[:-1]
            except Exception:
                self.CurrentWord = ""    
            # self.recomendFunc()
            self.initState()
    def tabClicked(self):
        keyboard.tap(Key.tab)
        self.initState()
    def subsTrack(self, fullWord, childWord):
        childLength = len(childWord)
        try:    
            if fullWord[:childLength] == childWord:    
                return fullWord[childLength:]
            else:
                ahk.run_script(str("send, ^+{Left}"), blocking=False)
                return fullWord

        except Exception:
            print(fullWord)   
            print(childWord) 
    def completFunc(self, selectedWord):
        if self.CurrentWord == "":
            return
        # selectedWord = self.RecomendationList[serial]
        keyboard.type(self.subsTrack(selectedWord, self.CurrentWord))
        if self.SpaceCheckBox.isChecked() == True:
            keyboard.type(" ")
        self.CurrentWord = ""
        self.recomendFunc()
        pass
    
    def recomendFunc(self):
        if self.CurrentWord == "":
            for btn in self.banglaRecomendationBtns:
                btn.setText("")
            return    
        self.RecomendationList = []

        # if self.tabWidget.currentIndex() == 0:
        #     list_ = BanglaWords

        if self.tabWidget.currentIndex() == 1:
            list_ = EnglishwordsList
            
        for word in list_[:]:
            if word[:len(self.CurrentWord)] == self.CurrentWord and word not in self.RecomendationList:
                self.RecomendationList.append(word)
            if len(self.RecomendationList) > 9:
                break
        if len(self.RecomendationList) == 0:
            for word in list_:
                similarity = similarity_ration_btween(word, self.CurrentWord)
                if similarity > 0.70 and word not in self.RecomendationList:
                    self.RecomendationList.append(word) 
        for wrd, btn in zip(self.RecomendationList, self.banglaRecomendationBtns):
            btn.setText(wrd)

    def logIn(self, char): # bangla cha log in  ==========================================> 
        keyboard.type(char)
        if self.SFXcheckBox.isChecked() == True:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            pass
        self.CurrentWord += char
        # self.recomendFunc()
        self.bangla_word_signal.emit(self.CurrentWord)
        
    def spaceClicked(self):
        keyboard.tap(Key.space)
        if self.CurrentWord != "":
            self.CurrentWord = ""
            self.recomendFunc()
            self.initState() 
            self.englishWordSofar = ""
            self.previous_word = ""
            self.formar_previous_word = ""
            self.previous_formar_previous_word = ""
            self.formar_previous_formar_previous_word = ""
            self.initBanglaThread_signal.emit("dfdf")
            self.initThread_signal.emit("init") 
    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(128, 128, 128, 0))
    def mousePressEvent(self, event):
        self.old_pos = event.screenPos()
    def mouseMoveEvent(self, event):
        if self.clicked:
            dx = self.old_pos.x() - event.screenPos().x()
            dy = self.old_pos.y() - event.screenPos().y()
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = event.screenPos()
        self.clicked = True
        return QWidget.mouseMoveEvent(self, event)
    def showSelf(self):
        self.show()
    def oenWinOsk(self):
        try:    
            os.startfile("osk.exe")
        except Exception as e:
            print(e)    
    def sfxStatechanged(self):
        self.OskHistory.setValue("sfxState", self.SFXcheckBox.isChecked())
    def loadCharacters(self):
        with io.open('.//Uis//SpecialCharectrs//specialCharacter.txt', "r", encoding="utf-8") as STC:
            characterGroups = (STC.read()).split("|*|")    

        self.widget = QWidget()
        self.verticalLayout = QVBoxLayout()

        self.verticalLayout.addWidget(self.RecentsGroupBox)
        
        for grp in characterGroups:
            groupParts = grp.split("|!|")
            
            groupName = groupParts[0] 
            groupCharec = (groupParts[1].split("|"))
            
            groupBox = QGroupBox()
            groupBox.setTitle(groupName)

            self.gridLayout = QGridLayout(groupBox)
            self.gridLayout.setContentsMargins(0,0, 0,0)
            self.gridLayout.setSpacing(1)
            rowcount = 0
            columnCount = 0
            columnNum = 20

            for cha in groupCharec[:]:
                self.btn = QPushButton((cha).replace("\n", ""))
                self.btn.setMinimumSize(25, 25)
                text = self.btn.text()
                try:    
                    # self.btn.clicked.connect(lambda ch, text=text : self.logCha("{}".format(text)))
                    self.btn.clicked.connect(lambda ch, text=text : self.logCha(text))
                except Exception as e:
                    print
                    pass

                if cha in ["ﷴ", "﷼", "﷽"]:
                    # self.gridLayout.addWidget(self.btn,rowcount, columnCount, 0, 2)
                    # columnCount +=2
                    pass

                else:
                    self.gridLayout.addWidget(self.btn,rowcount, columnCount)
                    columnCount +=1
                if columnCount == columnNum:
                    rowcount +=1
                    columnCount = 0 

            self.verticalLayout.addWidget(groupBox)

        self.widget.setLayout(self.verticalLayout)  

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scrollArea.setWidget(self.widget) 
    def loadEmojies(self):
        with io.open('.//Uis//SpecialCharectrs//OSKemojies.txt', "r", encoding="utf-8") as STC:
            emojiGroups = (STC.read()).split("|*|") 

        self.widget2 = QWidget()
        self.verticalLayout2 = QVBoxLayout()

        for grp in emojiGroups:
            groupParts = grp.split("|@|")
            
            groupName = groupParts[0] 
            groupCharec = (groupParts[1].split("|"))
            
            groupBox = QGroupBox()
            groupBox.setTitle(groupName)

            self.gridLayout2 = QGridLayout(groupBox)
            self.gridLayout2.setContentsMargins(0,0, 0,0)
            self.gridLayout2.setSpacing(1)
            rowcount = 0
            columnCount = 0
            columnNum = 20

            for cha in groupCharec[:]:
                if len(cha) == 0:
                    continue

                self.btn2 = QPushButton((cha).replace("\n", ""))

                self.btn2.setMinimumSize(25, 25)

                text = self.btn2.text()
                try:    
                    self.btn2.clicked.connect(lambda ch, text=text : self.logEmojie(text))
                except Exception as e:
                    print(e)
                    pass

                self.gridLayout2.addWidget(self.btn2,rowcount, columnCount)
                columnCount +=1
                if columnCount == columnNum:
                    rowcount +=1
                    columnCount = 0 

            self.verticalLayout2.addWidget(groupBox)

        self.widget2.setLayout(self.verticalLayout2)  
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidget(self.widget2)
    def closeEvent(self, event):
        if self.shiftState == True:
            self.shiftClicked()
        if self.capsLocked == True:
            self.CapsClicked()
        if self.ctrlState == True:
            self.ctrlClicked()
        if self.altState == True:
            self.altClicked()
        if self.winState == True:
            self.winClicked()

        self.OskHistory.setValue("spChaHis", self.CharHistory)  
        # self.listener.stop()  
        self.close()                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OSK_UI() 
    ex.show()
    sys.exit(app.exec_()) 
             