# -*- coding:utf-8 -*-

from distutils.log import FATAL
from pickle import NONE
from shutil import ExecError
import time
import keyboard as kb2
import speech_recognition as sr
from pynput.keyboard import Controller, Key
kb = Controller()
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QTimer, QSettings, QEasingCurve, QEvent
from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QListWidgetItem, QMenu, QTableWidgetItem, QAction, QApplication, QMessageBox, QGraphicsDropShadowEffect, QVBoxLayout, QGridLayout, QPushButton, QGroupBox, QSystemTrayIcon, QGraphicsBlurEffect, QGraphicsOpacityEffect
from PyQt5.QtGui import QPainter, QColor , QBrush
import os
import io 
import threading
from bijoy2unicode import converter  
import pyautogui
import webbrowser
import Script_pad
import Mic
import ScreenShort
import traceback
import Converter_for_main
from CreateShortcut import creat_shortcut
from pathlib import Path
from Options import Options_UI
# import OSK
import win32api
import winsound
import sounddevice as sd
import numpy as np
from ahk import AHK
ahk = AHK()
from pynput import mouse
import ctypes
import difflib
import win32process
import win32api
import pyperclip as pc
from num2words import num2words
from PyQt5.QtGui import QFont
from BlurWindow.blurWindow import blur
from textblob import TextBlob
import datetime
from spellchecker import SpellChecker
 
spell = SpellChecker()


from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


User32 = ctypes.WinDLL('User32.dll')

from win32gui import GetWindowText, GetCursorPos, WindowFromPoint, GetForegroundWindow, GetWindowRect, GetCaretPos, GetCursorInfo
from WordManager import wordManagerClass
from LoadWords import *
from pynput import keyboard
import NumberToWord
import ast

# ++++++++++++++++global variables ====================
similarTheredIsRunning = False
previous_word = ""
formar_previous_word = ""
previous_formar_previous_word = ""
formar_previous_formar_previous_word = ""
wordSofar = ""
sentencece_sofar = ""
englishWordSofar = ""
shiftKeyBlocked = False
keysBlocked = True
completorTraegered = False 
CurrentWord = ""
ruledOut = False
minimun_Similarity_Ratio = 0.70
ansi_wordSOFar = ""
using_functionKeys = False

currentWrdOutOfDic = False

selfCopyFuncCalled = False

using_tab = True
using_arrow = True

emojiDictionary = []
emoji_list = []
suggestEmoji = False

word_submitted_for_similarity = ""
word_submitted_lang = ""
newCharacterIsPressed = False

block_up_down = False


def initGlobal():
    global previous_word 
    global formar_previous_word 
    global previous_formar_previous_word 
    global formar_previous_formar_previous_word 
    global wordSofar 
    global englishWordSofar 
    global shiftKeyBlocked 
    global keysBlocked
    
    previous_word = ""
    formar_previous_word = ""
    previous_formar_previous_word = ""
    formar_previous_formar_previous_word = ""
    wordSofar = ""
    englishWordSofar = ""
    shiftKeyBlocked = False
    keysBlocked = True

def sendClip(txt):
    global selfCopyFuncCalled
    selfCopyFuncCalled = True
    reserved_clip = pc.paste()         
    pc.copy(txt)
    pyautogui.hotkey('ctrl', 'v')
    pc.copy(reserved_clip) 
    selfCopyFuncCalled = False



ahkScript = "global pinedState := 0 \nreviousXPos := 0\npreviousYPos := 0\nSetTimer, setPos, 100\nsetPos:\nglobal pinedState\nif pinedState = 0\n{\n	WinGetActiveTitle, wintitle\n	WinGetPos, perant_X, perant_Y,,, %wintitle%\n	position_X := A_CaretX + perant_X\n	position_Y := A_CaretY + perant_Y\n	if position_X != previousXPos and position_Y != previousYPos\n		WinMove, Nms_completer,, position_X, position_Y\n		previousXPos = %position_X%\n		previousYPos = %position_Y%\n}\nIfWinNotExist, Nms Voice pad\n{\n	ExitApp\n}\nreturn\nF23::\nglobal pinedState\nif pinedState = 0\n{\n	pinedState = 1\n	return\n}\nif pinedState = 1\n{\n	pinedState = 0\n}\nreturn"


keysToBlock = [2,3,4,5,6,7,8,9,10,11,  16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,   44,45,46,47,48,49,50,  52]    
upDownKey = [ 79 , 80]

def Custom_convert(text):
    text = text.replace('??????', '???')
    text = text.replace('??????', '???')
    text = text.replace('??????', '???')
    test = converter.Unicode()
    demo_text = '2007 ??? ????????????????????????????????? ??????????????????????????? ???????????? ????????????????????? ???????????????????????? ??????????????????????????? ????????? ?????????'
    toPrint = test.convertUnicodeToBijoy(f'{demo_text} {text}')
    rang = len(toPrint)
    if '??' in toPrint:      # this reset rep  
        pass_loop = -1
        custom_text = ''
        for index in range(rang):  
            if index == pass_loop:
                custom_text += toPrint[index]
                custom_text += '??'
                continue
            if toPrint[index] == '??':
                pass_loop = index + 1
                pass
            else:
                custom_text += toPrint[index]
            
        toPrint = custom_text   
            # print(toPrint[index])

    else:
        custom_text = toPrint
    
    if 'o' in toPrint or 'p' in toPrint or 'q' in toPrint:
        loop_count = 0
        pass_loop = -1
        custom_text = ''
        for index in range(rang):
            loop_count += 1   
            if loop_count == pass_loop:
                
                custom_text += toPrint[index]
                custom_text += index_l
                continue
            try:    
                if toPrint[index] == 'o' or toPrint[index] == 'p' or toPrint[index] == 'q':
                    if toPrint[index + 1] == 'w' or toPrint[index + 1] == '???' or toPrint[index + 1] == '???' or toPrint[index + 1] == '??':
                        pass_loop = loop_count + 1
                        index_l = toPrint[index]
                    else:
                        custom_text += toPrint[index]   
                        
                else:
                    custom_text += toPrint[index] 
            except Exception:
                pass    
        pass

    if '????' in custom_text:
        fixed_text = custom_text.replace('????', '??')
        custom_text = fixed_text
    if 'i?????v' in custom_text:
        fixed_text = custom_text.replace('i?????v', 'i??v')
        custom_text = fixed_text
    B_f_words = custom_text.split(" ")
    new_text = ''
    for w in B_f_words[10:]:
        if B_f_words.index(w) == 10:
            new_text += f'{w}'
        else:
            new_text += f' {w}'          
    custom_text  = new_text
    return custom_text 

def convert(text):
    if text == None:
        return ""
    text = text.replace('??????', '???')
    text = text.replace('??????', '???')
    text = text.replace('??????', '???')
    test = converter.Unicode()
    toPrint = test.convertUnicodeToBijoy(f'{text}')
    return toPrint 


class ClipBoardThreadClass(QtCore.QThread):	
    copy_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ClipBoardThreadClass, self).__init__(parent)
        self.is_running = True
        
    def run(self):
        while True:
            current_clipboard = pc.waitForNewPaste()
            global selfCopyFuncCalled
            if selfCopyFuncCalled == False:    
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                currentClip = f"{formatted_time}|*|\n{current_clipboard[:600]}"

                with io.open(".//Res//clipboard.txt", "r", encoding="utf-8") as file:
                    clipHis = file.read()
                preClips = clipHis.split("|@|\n")[:99]

                for c in preClips:
                    if len(c) == 0:
                        preClips.remove(c)

                preClips.insert(0, currentClip)

                txt_tosave = ""
                for clip in preClips:
                    txt_tosave += f"{clip}|@|\n"
                txt_tosave = txt_tosave[:-4]
                with io.open(".//Res//clipboard.txt", "w", encoding="utf-8") as file:
                    file.write(txt_tosave)
                self.copy_signal.emit("check clipboard")

class ThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
    def print_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)
        self.any_signal.emit(int(volume_norm))
    def run(self):
        while self.is_running == True:
            if self.is_running == True:    
                try:
                    with sd.Stream(callback=self.print_sound):
                        sd.sleep(4000)
                except Exception:
                    pass         
            else: 
                break    
    def stop(self):
        self.is_running = False
        self.terminate() 


class OwnSettings():
    def __init__(self):
        pass
    def setValue(self, setting_name, value):
        try:
            with io.open(f".//Res//{setting_name}.txt", 'w', encoding="utf-16") as f:
                f.write(str(value))
        except Exception as e:
            print(e)
    def value(self, setting_name):
        try:
            with io.open(f".//Res//{setting_name}.txt", 'r', encoding="utf-16") as f:
                value = f.read()
            if value in ["True", "False"]:
                value = ast.literal_eval(value)
                return ((value))
        except Exception as e:
            value = e
            print(e) 
        return value 

class Main_recognation(QtCore.QThread):	
    recognize_signal = QtCore.pyqtSignal(str)
    listener_signal = QtCore.pyqtSignal(str)
    def __init__(self, lang, UANSI_pos, audio, taking_cmd, parent=None):
        super(Main_recognation, self).__init__(parent)
        self.is_running = True
        self.lang = str(lang)
        self.UANSI_pos = str(UANSI_pos)
        self.audio = audio
        self.taking_cmd = taking_cmd
      
    def run(self):
        r = sr.Recognizer()
        try:
            text = r.recognize_google(self.audio, language= self.lang)
            global selfCopyFuncCalled
            
            
            if self.UANSI_pos == 'False':    
                if self.lang == 'bn-BD':
                    # for word, initial in {"1":"???", "2":"???", "3":"???", "4":"???", "5":"???", "6":"???", "7":"???", "8":"???", "9": "???", "0": "???"  }.items():
                    #     text = text.replace(word, initial) 
                    for word, initial in {"???????????????????????? ":"?????????????????????"}.items():
                        text = text.replace(word, initial)
                    if '????????????' in text:
                        text = text.replace('????????????', '???????????????') 
                    if ' ?????????????????????????????? ???????????????' in text or ' ???????????????????????? ???????????? ???????????????' in text or ' ?????????????????? ???????????? ???????????????' in text:
                        if ' ?????????????????????????????? ???????????????' in text:
                            text = text.replace(' ?????????????????????????????? ???????????????', '?')
                        if ' ?????????????????? ???????????? ???????????????' in text:
                            text = text.replace(' ?????????????????? ???????????? ???????????????', '?')    
                        if ' ???????????????????????? ???????????? ???????????????' in text: 
                            text = text.replace(' ???????????????????????? ???????????? ???????????????', '?')       
                    if ' ????????????????????????????????? ???????????????' in text or ' ????????????????????????????????? ???????????????' in text or ' ????????????????????? ???????????? ???????????????' in text  or ' ????????????????????? ???????????? ???????????????' in text or ' ????????????????????? ???????????????' in text:
                        if ' ????????????????????? ???????????? ???????????????' in text:
                            text = text.replace(' ????????????????????? ???????????? ???????????????', '!') 
                        if ' ????????????????????????????????? ???????????????' in text:
                            text = text.replace(' ????????????????????????????????? ???????????????', '!') 
                                
                        if ' ????????????????????????????????? ???????????????' in text:
                            text = text.replace(' ????????????????????????????????? ???????????????', '!') 
                        if ' ????????????????????? ???????????? ???????????????' in text:
                            text = text.replace(' ????????????????????? ???????????? ???????????????', '!') 
                        if ' ????????????????????? ???????????????' in text:
                            text = text.replace(' ????????????????????? ???????????????', '!')     
                    if ' ??????????????? ???????????????' in text or ' ?????????????????????????????? ???????????????' in text:
                        if ' ??????????????? ???????????????' in text:
                            text = text.replace(' ??????????????? ???????????????', '???')
                        if ' ?????????????????????????????? ???????????????' in text:
                            text = text.replace(' ?????????????????????????????? ???????????????', '???') 
                    if ' ????????? ???????????????' in text or ' ???????????????????????? ???????????????' in text:
                        if ' ????????? ???????????????' in text:
                            text = text.replace(' ????????? ???????????????', ',')
                        if ' ???????????????????????? ???????????????' in text:
                            text = text.replace(' ???????????????????????? ???????????????', ',')
                    if ' ???????????? ???????????? ???????????????' in text or ' ???????????????????????? ???????????????' in text:
                        if ' ???????????? ???????????? ???????????????' in text:
                            text = text.replace(' ???????????? ???????????? ???????????????', ';')
                        if ' ???????????????????????? ???????????????' in text:
                            text = text.replace(' ???????????????????????? ???????????????', ';')
                    else:
                        pass                
                    phase = text   
                if self.lang == 'en-US' or self.lang == 'en-GB':
                    if ' question mark' in text:
                        text = text.replace(' question mark', '?')
                    if ' exclamation mark' in text:
                        text = text.replace(' exclamation mark', '!')
                    if ' full stop' in text:
                        text = text.replace(' full stop', '.')   
                    if ' comma mark' in text:
                        text = text.replace(' comma mark', ',')
                    if ' colon' in text:
                        text = text.replace(' comma', ':')
                txt_ = text
                try:    
                    
                    words = txt_.split(' ')
                    if words[-1] in ["??????", "?????????", "??????????????????", "???????????????", "?????????????????????"]: 
                        words[-1] = words[-1]+"?"
                    
                    reserved_clip = pc.paste()
                    selfCopyFuncCalled = True
                    pc.copy(f"{txt_}")
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.write(' ')
                    pc.copy(reserved_clip)
                    selfCopyFuncCalled = False
                    
                except Exception as e:
                    print('type error; UANSI_pos == False')
                    print(e)
            if self.UANSI_pos == 'True':    
                if self.lang == 'bn-BD':    
                    toPrint = Custom_convert(text)
                else:
                    toPrint = text
                try:
                    reserved_clip = pc.paste()
                    selfCopyFuncCalled = True
                    pc.copy(toPrint)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.write(' ')

                    pc.copy(reserved_clip)
                    selfCopyFuncCalled = False
                     
                except Exception as e:
                    print('type error; UANSI_pos == True')
                    print(e)
                    pass
        except Exception as e:
            if str(e) == 'recognition connection failed: [Errno 11001] getaddrinfo failed':
                self.recognize_signal.emit(str(e))
            self.is_running = False

    def stop(self):
        self.is_running = False

        self.terminate()
        
class whileThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(str)
    def __init__(self, lang, UANSI_pos, taking_cmd, micIndex , micName, energy, pause, phrase ,non_speaking_duration , parent=None):
        super(whileThreadClass, self).__init__()
        self.is_running = True
        self.lang = lang
        self.UANSI_pos = UANSI_pos
        self.taking_cmd = taking_cmd

        self.micIndex = micIndex
        self.micName = micName
        self.energy = energy
        self.pause = pause
        self.phrase = phrase
        self.non_speaking_duration = non_speaking_duration
    def run(self):
        try:
            r = sr.Recognizer()
            self.mic_index = int(self.micIndex) # int(settings[5])
            self.mic_name = self.micName # settings[6]
            r.energy_threshold = int(self.energy) # int(settings[0])
            r.pause_threshold = float(self.pause) # float(settings[1])
            r.phrase_threshold = float(self.phrase) # float(settings[2])
            r.non_speaking_duration = float(self.non_speaking_duration) # float(settings[3])
            r.operation_timeout = None


            sr_mic_list = sr.Microphone.list_microphone_names() 
            if sr_mic_list[self.mic_index] == self.mic_name:
                mic = sr.Microphone(device_index= self.mic_index)   
                # print('selected mic is pluged in')
            else:     
                print('selected mic is not pluged in')
                mic = sr.Microphone()
            with mic as source:
                try:
                    r.adjust_for_ambient_noise(source)
                except Exception as e:
                    print(e)
                    print('adjust_for_ambient_noise problem!')
                    pass
                self.start_thread = threading.Thread(target=start_sig)
                
                self.start_thread.start()
                self.any_signal.emit("Listening...")
                if self.taking_cmd == False:
                    while self.is_running:
                        try:
                            audio = r.listen(source)
                        except Exception as e:
                            print(e)
                            self.any_signal.emit('Audio recording problem problem')
                            break
                        self.recognizer_thread = Main_recognation(self.lang, self.UANSI_pos, audio, self.taking_cmd)
                        self.recognizer_thread.recognize_signal.connect(self.send_signal)
                        # self.recognizer_thread.listener_signal.connect(self.send_signal)
                        self.recognizer_thread.finished.connect(self.recognizer_thread.deleteLater)
                        self.recognizer_thread.start()
                else:
                    try:
                        audio = r.listen(source)
                    except Exception as e:
                        print(e)
                        print(f'Audio recording problem problem')
                        self.any_signal.emit('Audio recording problem problem')
                    r = sr.Recognizer()
                    try:
                        text = r.recognize_google(audio, language= self.lang)
                        # self.recognize_signal.emit('recognition complete')#<====================experiment=======================>
                        if self.UANSI_pos == False:    
                            if self.lang == 'bn-BD':
                                for word, initial in {"1":"???", "2":"???", "3":"???", "4":"???", "5":"???", "6":"???", "7":"???", "8":"???", "9": "???", "0": "???"  }.items():
                                    text = text.replace(word, initial)
                                if '????????????' in text:
                                    text = text.replace('????????????', '???????????????') 
                                if ' ?????????????????????????????? ???????????????' in text or ' ???????????????????????? ???????????? ???????????????' in text or ' ?????????????????? ???????????? ???????????????' in text:
                                    if ' ?????????????????????????????? ???????????????' in text:
                                        text = text.replace(' ?????????????????????????????? ???????????????', '?')
                                    if ' ?????????????????? ???????????? ???????????????' in text:
                                        text = text.replace(' ?????????????????? ???????????? ???????????????', '?')    
                                    if ' ???????????????????????? ???????????? ???????????????' in text: 
                                        text = text.replace(' ???????????????????????? ???????????? ???????????????', '?')       
                                if ' ????????????????????????????????? ???????????????' in text or ' ????????????????????????????????? ???????????????' in text or ' ????????????????????? ???????????? ???????????????' in text  or ' ????????????????????? ???????????? ???????????????' in text or ' ????????????????????? ???????????????' in text:
                                    if ' ????????????????????? ???????????? ???????????????' in text:
                                        text = text.replace(' ????????????????????? ???????????? ???????????????', '!') 
                                    if ' ????????????????????????????????? ???????????????' in text:
                                        text = text.replace(' ????????????????????????????????? ???????????????', '!') 
                                            
                                    if ' ????????????????????????????????? ???????????????' in text:
                                        text = text.replace(' ????????????????????????????????? ???????????????', '!') 
                                    if ' ????????????????????? ???????????? ???????????????' in text:
                                        text = text.replace(' ????????????????????? ???????????? ???????????????', '!') 
                                    if ' ????????????????????? ???????????????' in text:
                                        text = text.replace(' ????????????????????? ???????????????', '!')     
                                if ' ??????????????? ???????????????' in text or ' ?????????????????????????????? ???????????????' in text:
                                    if ' ??????????????? ???????????????' in text:
                                        text = text.replace(' ??????????????? ???????????????', '???')
                                    if ' ?????????????????????????????? ???????????????' in text:
                                        text = text.replace(' ?????????????????????????????? ???????????????', '???') 
                                if ' ????????? ???????????????' in text or ' ???????????????????????? ???????????????' in text:
                                    if ' ????????? ???????????????' in text:
                                        text = text.replace(' ????????? ???????????????', ',')
                                    if ' ???????????????????????? ???????????????' in text:
                                        text = text.replace(' ???????????????????????? ???????????????', ',')
                                if ' ???????????? ???????????? ???????????????' in text or ' ???????????????????????? ???????????????' in text:
                                    if ' ???????????? ???????????? ???????????????' in text:
                                        text = text.replace(' ???????????? ???????????? ???????????????', ';')
                                    if ' ???????????????????????? ???????????????' in text:
                                        text = text.replace(' ???????????????????????? ???????????????', ';')
                                else:
                                    pass                
                                phase = text   
                            if self.lang == 'en-US' or self.lang == 'en-GB':
                                if ' question mark' in text:
                                    text = text.replace(' question mark', '?')
                                if ' exclamation mark' in text:
                                    text = text.replace(' exclamation mark', '!')
                                if ' full stop' in text:
                                    text = text.replace(' full stop', '.')   
                                if ' comma mark' in text:
                                    text = text.replace(' comma mark', ',')
                                if ' colon' in text:
                                    text = text.replace(' comma', ':')
                            phase = text 
                            txt_ = phase
                            try:    
                                kb.type(f"{txt_} ")
                                try:
                                    kb.press(Key.enter)
                                    kb.release(Key.enter)
                                except Exception as e:
                                    print(e+"353")    
                            except Exception as e:
                                print('type error; UANSI_pos == False')
                                print(e)
                        if self.UANSI_pos == True:    
                            if self.lang == 'bn-BD':    
                                toPrint = Custom_convert(text)
                            else:
                                toPrint = text
                            try:
                                kb.type(f"{toPrint} ")
                            except Exception as e:
                                print('type error; UANSI_pos == True')
                                print(e)
                                pass
                    except Exception as e:
                        print(e)
                        if str(e) == 'recognition connection failed: [Errno 11001] getaddrinfo failed':
                            self.any_signal.emit(str(e))
                        self.is_running = False    
                    self.any_signal.emit('commend compleated brauh!')          
                return
        except Exception as e:
            print(e)
            print('in main thread exception!')
            self.any_signal.emit('Audio recording problem problem')

    def send_signal(self, info):
        self.any_signal.emit(info)
        self.stop()
    def stop(self):
        try:    
            self.is_running = False
            self.start_thread.join()
            
            self.recognizer_thread.stop()

            self.terminate()
                
        except Exception:
            pass
def start_sig():
    try:
        winsound.PlaySound('.//SFX//Start.wav', winsound.SND_FILENAME)
    except Exception:
        pass
def stop_sig():
    try:
        winsound.PlaySound('.//SFX//Finish.wav', winsound.SND_FILENAME)
    except Exception:
        pass 

class AdvanceSimilarityThread(QtCore.QThread):
    mostMatchedWords = QtCore.pyqtSignal(list)
    def __init__(self, wordSofar, englishWordSoFar):
        super(AdvanceSimilarityThread, self).__init__()
        self.is_running = True
           
    def run(self):
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
                if len(wordArray) == 1:
                    continue
            except Exception:
                continue    
  
            similarity = self.similarity_ration_btween(englishWord, englishWordSofar)   

            if len(englishWordSofar) < 5:
                minimumSimi = 0.7
            else:
                minimumSimi = 0.7  
            if similarity > minimumSimi:
                if similarity > self.heighestMatchedRatio:
                    self.similarWords.insert(0, banglaWord)
                    self.heighestMatchedRatio = similarity
                else:
                    self.similarWords.append(banglaWord)
                        
            if len(self.similarWords) > 9:
                break

        self.mostMatchedWords.emit(self.similarWords)

    def similarity_ration_btween(self, x, y):
        seq = difflib.SequenceMatcher(None,x,y)
        d = seq.ratio()
        return d                
    def stop(self):
        self.is_running = False
        self.terminate()

        

class similarity_While_Thread(QtCore.QThread):
    mostMatchedWords = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(similarity_While_Thread, self).__init__(parent)
        self.is_running = True
        self.ruledOutSimi = False
        self.brokenByNewCharacter = False
        self.preEngWrd = ""
    def run(self):
        while self.is_running:
            global minimun_Similarity_Ratio
            global word_submitted_for_similarity
            global word_submitted_lang
            global wordSofar
            try:
                if self.preEngWrd != word_submitted_for_similarity and word_submitted_for_similarity != "":

                    # print("in similarity thread!")
                    current_word = word_submitted_for_similarity # this for inconsistencie updates 
                    self.similarWords = []
                    self.heighestMatchedRatio = 0   # to get the most matched wrd

                    if self.ruledOutSimi == False or len(word_submitted_for_similarity) < len(self.preEngWrd):
                        if word_submitted_lang == "bangla":
                            currentwordsList = wordsList 
                        else:
                            currentwordsList = EnglishwordsList
                            # self.similarWords = self.suggest_word(word_submitted_for_similarity, currentwordsList, minimun_Similarity_Ratio)
                        
                        # =============
                        # print(word_submitted_lang)
                        
                        # print("about to start")
                        
                        if word_submitted_lang == "english":
                            b = TextBlob(word_submitted_for_similarity)
                            corrected = str(b.correct())
                            self.similarWords.insert(0, corrected) 


                            if len(self.similarWords) < 2 :
                                corrected = (spell.correction(word_submitted_for_similarity))
                                if corrected != None and corrected not in self.similarWords: 
                                    self.similarWords.insert(0, corrected)

                            # if len(self.similarWords) == 1:
                            if len(self.similarWords) < 2 :
                                params = {
                                'q' : word_submitted_for_similarity,   
                                'hl': 'en',
                                'gl': 'us'
                                }

                                html = requests.get('https://www.google.com/search?q=', headers=headers, params=params).text
                                soup = BeautifulSoup(html, 'lxml')

                                # print(soup)
                                i_tag = soup.find('i')
                                if i_tag:
                                    text_in_i_tag = i_tag.get_text()
                                    # print(text_in_i_tag)
                                    if text_in_i_tag not in self.similarWords:   
                                        self.similarWords.insert(0, text_in_i_tag) 

                        if word_submitted_lang == "bangla" or len(self.similarWords) < 2:
                            
                            params = {
                            'q' : wordSofar,   
                            'hl': 'bn',
                            'gl': 'bd'
                            }

                            html = requests.get('https://www.google.com/search?q=', headers=headers, params=params).text
                            soup = BeautifulSoup(html, 'lxml')

                            # print(soup)
                            i_tag = soup.find('i')
                            if i_tag:
                                text_in_i_tag = i_tag.get_text()
                                # print(text_in_i_tag)
                                if text_in_i_tag not in self.similarWords:   
                                    self.similarWords.insert(0, text_in_i_tag)
                            
                            if len(self.similarWords) < 2 : 
                                for wrd in currentwordsList[:]: 
                                    if word_submitted_lang == "bangla":
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
                                    else:
                                        englishWord = wrd  

                                    if len(current_word) > 3 and len(englishWord)<4:
                                        continue

                                    if word_submitted_for_similarity[0] not in englishLatters:
                                        similarity = self.similarity_ration_btween(banglaWord, word_submitted_for_similarity)
                                    else:
                                        similarity = self.similarity_ration_btween(englishWord, word_submitted_for_similarity)   
                                    minimumSimi = minimun_Similarity_Ratio 
                                    if similarity >= minimumSimi:
                                        if similarity > self.heighestMatchedRatio:
                                            if word_submitted_lang == "bangla":    
                                                self.similarWords.insert(0, banglaWord)
                                            else:
                                                self.similarWords.insert(0, englishWord)
                                            self.heighestMatchedRatio = similarity

                                    global newCharacterIsPressed            
                                    if newCharacterIsPressed == True:  #<------   # len(self.similarWords) > 30 or    
                                        if newCharacterIsPressed == True:  
                                            self.brokenByNewCharacter = True
                                        # print("bro by new")    
                                        break 
                            
                                    
                        
                            

                        # print(corrected)




                        if len(self.similarWords) == 0: #  and self.brokenByNewCharacter == False
                            self.ruledOutSimi = True

                        else:
                            self.ruledOutSimi = False
                        if len(self.similarWords) != 0:    
                            # print(f"for:{}")
                            self.mostMatchedWords.emit(self.similarWords)
                        self.preEngWrd = current_word
                    else:
                        self.preEngWrd = current_word
            except Exception as e:
                pass
            time.sleep(0.1)   
    def similarity_ration_btween(self, x, y):
        seq = difflib.SequenceMatcher(None,x,y)
        d = seq.ratio()
        return d    
    def suggest_word(self, word, word_list, mini_simi= 0.6):
        word = word.lower()
        word_list = [w.lower() for w in word_list]
        suggestions = difflib.get_close_matches(word, word_list, n=10, cutoff = mini_simi)
        return suggestions                
    def initFunc(self, sig):
        self.ruledOutSimi = False
        pass
    def stop(self):
        self.is_running = False
        self.terminate()

class WhileloopThroughListThread(QtCore.QThread):
    matchedWordsSignal = QtCore.pyqtSignal(list)
    ruledOutSignal = QtCore.pyqtSignal(bool)
    newCherecterIspressed = QtCore.pyqtSignal(bool)
    themeSignal = QtCore.pyqtSignal(str)
    acSignal = QtCore.pyqtSignal(str) # autoCurrect
    caretPosSignal = QtCore.pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(WhileloopThroughListThread, self).__init__(parent)
        
        self.newCharecterState = False
        self.is_running = True
        self.ruledOut = False
        self.ruledOutEngla = False
        self.preWord = ""
        self.preEngWrd = ""
        self.ruledOutSimi = False
        self.similarTheredIsRunning = False
        self.mainRuledOut = False

        self.preACSig = ''
        pass
    def run(self):
        while self.is_running:
            global wordSofar
            global englishWordSofar
            global newCherecterIspressed 
            global suggestEmoji
            global currentWrdOutOfDic
            # if ((self.preEngWrd != englishWordSofar and englishWordSofar != "") or (self.preWord != wordSofar and wordSofar != "")):
            #     try:
            #         lastcha = wordSofar[len(self.preWord)]
            #         if lastcha not in englishLatters:
            #             self.mainRuledOut = True

            #         if self.mainRuledOut == True:
            #             self.matchedWordsSignal.emit([wordSofar])
            #     except Exception:
            #         pass    
                
            if ((self.preEngWrd != englishWordSofar and englishWordSofar != "") or (self.preWord != wordSofar and wordSofar != "")) and self.mainRuledOut == False:   
                newCherecterIspressed = True
                self.matchedWords = []
                try:
                    if wordSofar[0] not in englishLatters and wordSofar[0] not in banglaNumbs:  # for bangla lang
                        if self.ruledOut == False or len(englishWordSofar) < len(self.preWord):  
                            self.loopThroughList(wordsList, wordSofar,englishWordSofar)    # this gonna check in main dictionary
                            if len(self.matchedWords) == 0:
                                self.ruledOut = True
                            elif len(self.matchedWords) != 0 and self.ruledOut == True: 
                                self.themeSignal.emit("green")
                                currentWrdOutOfDic = False
                                self.ruledOut = False 

                        if self.ruledOut == True and self.ruledOutEngla == False:  # englawords dictionary
                            self.loopThroughList(englaList,wordSofar,englishWordSofar)
                            if len(self.matchedWords) == 0:
                                self.ruledOutEngla = True
                            else:    
                                self.themeSignal.emit("blue")

                        if len(self.matchedWords) == 0 :  # and self.ruledOutSimi == False
                            if englishWordSofar != "":    
                                self.startSimilarityThread(englishWordSofar, 'bangla')   
                            else:
                                self.startSimilarityThread(wordSofar, 'bangla')   

                    if wordSofar[0] in englishLatters:     # for english
                        # ================================
                        englishWordSofar = wordSofar
                        
                        # adding emojies ===================================
                        if suggestEmoji:
                            for e_pro in emojiDictionary:
                                emoji = e_pro[0]
                                emoji_name = e_pro[1]
                                if emoji_name.lower() == englishWordSofar.lower():
                                    self.matchedWords.insert(0, emoji) 
                        # / adding emojies ==================================
                        
                        if self.ruledOut == False or len(englishWordSofar) < len(self.preWord):
                            self.loopThroughList(EnglishwordsList,wordSofar,englishWordSofar)

                            if len(self.matchedWords) == 0:
                                self.ruledOut = True
                            elif len(self.matchedWords) != 0 and self.ruledOut == True: 
                                self.themeSignal.emit("green") 
                                currentWrdOutOfDic = False
                                self.ruledOut = False 

                       
                        if len(self.matchedWords) == 0 and self.ruledOutSimi == False:
                            self.startSimilarityThread(englishWordSofar, 'english')

                    # ========================================
                    if wordSofar[0] in banglaNumbs: # banglaNumbs
                        numberInWord = NumberToWord.convert_num_to_word(wordSofar)
                        self.matchedWords.append(numberInWord) 
                        splitedNumbersInword = ""
                        for i in range(len(wordSofar)):
                            splitedNumbersInword += f"{NumberToWord.convert_num_to_word(wordSofar[i])} "
                        
                        self.matchedWords.append(splitedNumbersInword.strip())

                    if wordSofar[0] in englishNumbers: # banglaNumbs
                        numberInWord = num2words(wordSofar)
                        self.matchedWords.append(numberInWord)
                        numberInWord = num2words(wordSofar, to='ordinal', lang='en')
                        self.matchedWords.append(numberInWord) 
                        splitedNumbersInword = ""
                        for i in range(len(wordSofar)):
                            splitedNumbersInword += f"{num2words(wordSofar[i])} "
                        
                        self.matchedWords.append(splitedNumbersInword.strip())  
                    
                    # ========================================    
                except Exception:
                    self.preWord = ""
                    pass


                self.matchedWordsSignal.emit(self.matchedWords)

                self.preWord = wordSofar
                self.preEngWrd = englishWordSofar

                # caretPos_str = ahk.run_script(getCaretPos_Script)
                # caretPos = str(caretPos_str).split(" ")
                # try:
                #     self.caretPosSignal.emit(int(caretPos[0]),int(caretPos[1]))
                # except Exception:
                #     pass

            time.sleep(0.1)
     
    def newCharecterIsPressedStateChange(self, state):
        self.newCharacterIsPressed = True
    def updateWord(self, wordSofar, englishWordSofar_local, bangla=""):
        self.wordSofar = wordSofar
        self.englishWordSofar_local = englishWordSofar_local
 
    def loopThroughList(self, wordList, wordSofar, englishWordSofar_local):

        # print(self.matchedWords)
        for wrd in wordList[:]:
            wordArray = wrd.split(",")
            if len(wordArray) == 1 and wordSofar != englishWordSofar_local:
                continue
            mainWord = wordArray[0]

            index = 0
            for wrd in wordArray[:]:
                if mainWord in self.matchedWords:
                    break
                # print(f"{wrd[:len(wordSofar)]} : {wordSofar}")
                if index == 0 and wrd[:len(wordSofar)] == wordSofar and wrd not in self.matchedWords: # and wrd not in self.matchedWords
                    self.matchedWords.append(mainWord)
                    break
                elif (wrd[:len(englishWordSofar_local)]).lower() == (englishWordSofar_local).lower() and mainWord not in self.matchedWords and englishWordSofar_local != "": # and wrd not in self.matchedWords
                    self.matchedWords.append(mainWord)
                    if len(wordSofar) > 3 and wrd.lower() == (englishWordSofar_local).lower() and mainWord != wordSofar and self.preACSig != (englishWordSofar_local).lower():
                        self.acSignal.emit(mainWord)
                        self.preWord = mainWord
                        self.preACSig = (englishWordSofar_local).lower()
                    break
                index += 1
            if len(self.matchedWords) >11 or self.newCharecterState == True:
                if self.newCharecterState == True:
                    print("loop Was breaked by new cherecter")
                break 

    def initFunc(self, sig):
        global currentWrdOutOfDic
        self.ruledOut = False
        self.ruledOutSimi = False
        currentWrdOutOfDic = False

        # print("init signal")
    
    def startSimilarityThread(self,englishWordSofar_local,currentLang):
        
        # filter ==========
        for i in range(len(englishWordSofar_local)):
            if englishWordSofar_local[i] not in englishAlphabets:
                return
        # ============
        global word_submitted_lang
        global word_submitted_for_similarity
        global newCherecterIspressed
        global currentWrdOutOfDic
        # global wordSofar
        self.themeSignal.emit("yellow")
        currentWrdOutOfDic = True
        newCherecterIspressed  = False
        word_submitted_lang = currentLang
        word_submitted_for_similarity = englishWordSofar_local # this could be bangla word so far when osk is pressed!
        
        # if word_submitted_lang == "english":    
        #     word_submitted_for_similarity = englishWordSofar_local # this could be bangla word so far when osk is pressed!
        # else:
        #     word_submitted_for_similarity = wordSofar # this could be bangla word so far when osk is pressed!

    def ruledOutSimiStateChange(self, state):
        self.ruledOutSimi = state
        self.similarTheredIsRunning = False
    
    def addSimiWordsFunc(self, wordList):
        self.matchedWordsSignal.emit(wordList)
        # self.themeSignal.emit("yellow")
    def initFunc(self, sig):
        self.ruledOut = False
        self.ruledOutSimi = False
        self.ruledOutEngla = False
        self.mainRuledOut = False

        # self.themeSignal.emit("yellow")
        global word_submitted_lang
        global word_submitted_for_similarity

        word_submitted_for_similarity = ""
        self.preACSig = '' 
    def stop(self):
        self.is_running = False
        self.terminate()


class wordThread(QtCore.QThread):
    matched_Word_signal = QtCore.pyqtSignal(list)
    hideSignal = QtCore.pyqtSignal(str)
    themeSignal = QtCore.pyqtSignal(str)
    acWordSignal = QtCore.pyqtSignal(str)

    newCherecterIspressed = QtCore.pyqtSignal(bool)
    initSignal = QtCore.pyqtSignal(str)
    caretPosSignal = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(wordThread, self).__init__()
        self.is_running = True
        self.ruledOut = False
        self.ruledOutSimi = False
        self.similarTheredIsRunning = False
        self.dicThreadIsRunning = False
        self.preWord = ""
        self.ruledOutEngla = False

        # self.loopThread = loopThroughListThread()

        self.whileLoopThread = WhileloopThroughListThread()
        self.whileLoopThread.matchedWordsSignal.connect(self.addSimiWordsFunc)
        self.whileLoopThread.caretPosSignal.connect(self.emitCaretPos)
        self.whileLoopThread.acSignal.connect(self.sendAcSignal)
        self.whileLoopThread.finished.connect(self.whileLoopThread.deleteLater)
        self.whileLoopThread.themeSignal.connect(self.emitTheme)
        self.initSignal.connect(self.whileLoopThread.initFunc)
        self.newCherecterIspressed.connect(self.whileLoopThread.newCharecterIsPressedStateChange)
        # self.ruledOutSig.connect(self.whileLoopThread.initFunc)

        self.whileLoopThread.start()


        self.whileSimiThread = similarity_While_Thread()
        self.whileSimiThread.mostMatchedWords.connect(self.addSimiWordsFunc)
        self.initSignal.connect(self.whileSimiThread.initFunc)
        self.whileSimiThread.start()

    def emitCaretPos(self, posX, posY):
        self.caretPosSignal.emit(posX, posY)
    
    def run(self, wordSofar = "", englishWordSofar_local = "", currentLang = ""):
        
        # self.currentLang = currentLang

        # if self.similarTheredIsRunning == True or self.dicThreadIsRunning == True:    
        #     self.newCherecterIspressed.emit(True)
        # self.wordSofar = wordSofar
        # self.englishWordSofar = englishWordSofar_local
        

        if wordSofar in ["", " "]:
            return
        try:
            self.hideSignal.emit("show")    
            return

        except Exception as e:
            print(traceback.format_exc()) 
    
    def sendAcSignal(self, acWord):
        self.acWordSignal.emit(acWord)
        pass

    def dicThreadReturnFunc(self, matchedWords):
        self.matched_Word_signal.emit(matchedWords) 
        self.dicThreadIsRunning = False

    def addSimiWordsFunc(self, simiWords):
        global wordSofar
        global englishWordSofar

        self.matchedWords = []
        self.matchedWords.append(englishWordSofar)
        self.matchedWords.append(wordSofar)
        for w in simiWords:
            self.matchedWords.append(w)
        self.matched_Word_signal.emit(self.matchedWords)     


    def emitTheme(self, theme):
        self.themeSignal.emit(theme)

    def initFunc(self, sig):
        self.initSignal.emit("hjh")
        self.themeSignal.emit("green")
 


def similarity_ration_btween(first_string, second_string):
    temp = difflib.SequenceMatcher(None,first_string , second_string)
    return temp.ratio()    


greenStyleSheet = 'QPushButton{\n	font:  12pt "MS Shell Dlg 2";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(62, 255, 41, 255), stop:1 rgba(5, 240, 255, 255));\nborder:2px solid rgb(0, 187, 255);\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(9, 198, 250, 200));\nborder:1px solid rgb(0, 187, 255);}\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n}'


class similarityThreadForOsk(QtCore.QThread):
    mostMatchedWords = QtCore.pyqtSignal(list)
    ruledOutSimiSignal = QtCore.pyqtSignal(bool)            # call preventer signal 1
    similarTheredIsRunningSignal = QtCore.pyqtSignal(bool, bool, str)  # call preventer signal 2
    def __init__(self, BanglaWordsofar = ""):
        super(similarityThreadForOsk, self).__init__()
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
        # User32.SetWindowLongW(int(self.dockWidget.winId()), -20, 134217728)
        # self.dockWidget.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint)
        # User32.SetWindowLongW(int(self.dockWidget.winId()), -20, 134217728)
        # print(int(self.dockWidget.winId()))
        self.CloseButton.clicked.connect(lambda: self.close())
        # self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        self.clicked = False
        self.WinOsk.clicked.connect(self.oenWinOsk)
        self.tabWidget.currentChanged.connect(self.tabChangedFunc)
        self.SFXcheckBox.clicked.connect(self.sfxStatechanged)
        
        # CurrentWord = ""
        self.RecomendationList = []
        self.RecomendationBtns = [self.RB1,self.RB2,self.RB3,self.RB4,self.RB5,self.RB6,self.RB7,self.RB8,self.RB9, self.RB10]
        self.numDic = {'1':'???','2':'???','3':'???','4':'???','5':'???','6':'???','7':'???','8':'???','9':'???','0':'???',}

        self.emojiLoaded = False
        self.characterLoaded = False
        
        self.OskHistory = QSettings("OSK_History")

        self.CharHistory = self.OskHistory.value("spChaHis")

        self.SFXcheckBox.setChecked(bool(self.OskHistory.value("sfxState")))

        self.capsLocked = False
        self.shiftState = False
        self.ctrlState = False
        self.altState = False
        self.winState = False

        self.pushButton_35.setStyleSheet("")

        self.state = self.saveState()
        # self.RestoreCharacPushButton.clicked.connect(self.RestoreCharac)
        

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.listWidget.setStyleSheet("background: transparent;")

        blur = QtWidgets.QGraphicsBlurEffect()
        blur.setBlurRadius(10)
        # self.listWidget.setGraphicsEffect(blur)  action replay

        # self.frame.setGraphicsEffect(blur)
        # self.frame.setWindowOpacity(0.8)



        # self.pushButton_201.clicked.connect(self.spaceClicked)
        self.pushButton_198.clicked.connect(self.tabClicked)            
        # self.pushButton_199.clicked.connect(self.BackSpaceClicked)
        self.pushButton_200.clicked.connect(self.deleteClicked)
        self.pushButton_197.clicked.connect(self.EnterClicked)
# /banglakeyboard connectors =========================== 
        
        # functions ==========================================================
        self.pushButton_2.clicked.connect(lambda: kb.tap(Key.f1))
        self.pushButton_3.clicked.connect(lambda: kb.tap(Key.f2))
        self.pushButton_18.clicked.connect(lambda: kb.tap(Key.f3))
        self.pushButton_17.clicked.connect(lambda: kb.tap(Key.f4))
        self.pushButton_16.clicked.connect(lambda: kb.tap(Key.f5))
        self.pushButton_15.clicked.connect(lambda: kb.tap(Key.f6))
        self.pushButton_14.clicked.connect(lambda: kb.tap(Key.f7))
        self.pushButton_13.clicked.connect(lambda: kb.tap(Key.f8))
        self.pushButton_12.clicked.connect(lambda: kb.tap(Key.f9))
        self.pushButton_11.clicked.connect(lambda: kb.tap(Key.f10))
        self.pushButton_10.clicked.connect(lambda: kb.tap(Key.f11))
        self.pushButton_9.clicked.connect(lambda: kb.tap(Key.f12))
        
        # /function ==========================================================
        self.changeStatedStylesheet = "background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1.197, fx:0.489, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(72, 173, 255, 255));"
        # media controll =====================================================
        self.pushButton_8.clicked.connect(lambda: kb.tap(Key.media_volume_down))
        self.pushButton_7.clicked.connect(lambda: kb.tap(Key.media_volume_up))
        self.pushButton_6.clicked.connect(lambda: kb.tap(Key.media_previous))
        self.pushButton_5.clicked.connect(lambda: kb.tap(Key.media_play_pause))
        self.pushButton_4.clicked.connect(lambda: kb.tap(Key.media_next))
        # /media controll   ===================================================
        
        self.pushButton_35.clicked.connect(self.CapsClicked)

        self.latter_btns = [self.pushButton_65, self.pushButton_66,self.pushButton_67,self.pushButton_68,self.pushButton_69,
            self.pushButton_70,self.pushButton_71,self.pushButton_72,self.pushButton_73,self.pushButton_74,self.pushButton_36,self.pushButton_37,self.pushButton_38,self.pushButton_39,self.pushButton_40,self.pushButton_41,self.pushButton_42,self.pushButton_43,self.pushButton_44,
            self.pushButton_84, self.pushButton_102,self.pushButton_106, self.pushButton_107, self.pushButton_108, self.pushButton_109, self.pushButton_110]

        self.norCha = ["`","1","2","3","4","5","6","7","8","9","0","-","=","[","]",' \ ', ";", "'", ",", ".", "/"]
        self.shiftCha = ["~","!","@","#","$","%","^","&&","*","(",")","_","+", "{", "}", "|", ":", '"', "<", ">", "?"]
        self.karList = ["???","???","???","???","???","???","???","???","???","???"]
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
    

        # self.BanglawordThread = BanglawordThread()
        # self.BanglawordThread.matched_Word_signal.connect(self.populateWords)
        # self.bangla_word_signal.connect(self.BanglawordThread.run)
        # self.initBanglaThread_signal.connect(self.BanglawordThread.initFunc)
        # self.BanglawordThread.start()

        self.loadCharacters()
        self.loadEmojies()

        # hWnd = self.winId()
        # print(hWnd)
        # blur(hWnd)

    def on_click(self, x, y, button, pressed):
        # print("I am here!")
        global CurrentWord
        if GetWindowText(WindowFromPoint(GetCursorPos())) != self.windowTitle():
            CurrentWord = ""
            self.recomendFunc()
            # self.initState() 
            self.initThread_signal.emit("init")
            pass
    
    def trim(self, l):
        global CurrentWord
        
        CurrentWord = CurrentWord[:-l]
        for i in range(l):  
            kb.tap(Key.backspace)
    def cleanRecomendations(self):
        for btn in self.RecomendationBtns:
            btn.setText("")
    def populateWords(self, words):
        self.cleanRecomendations()
        for wrd, btn in zip(words, self.RecomendationBtns):
            btn.setText(wrd)
        pass
      
    def recChaClicked(self, ser):
        try:
            cha = self.CharHistory[int(ser)]
        except Exception as e:
            print(cha)
            print(e)
            print("i am here 1") 
            cha = ""    

        try:    
            kb.type(cha) 
        except Exception:     
            with io.open("dalal.ahk", 'w', encoding="utf-16") as f:
                f.write(f"send,{cha}")
            os.system('AutoHotkeyU64.exe "dalal.ahk"')
    def logEmojie(self, Cha): 
        try:    
            kb.type(Cha) 
        except Exception:     
            with io.open("dalal.ahk", 'w', encoding="utf-16") as f:
                f.write(f"send,{Cha}")
            os.system('AutoHotkeyU64.exe "dalal.ahk"')
        self.initState()
        self.sfx()
    def tabChangedFunc(self, index):
        global CurrentWord
        
        r = 0
        c = 0
        for btn in self.RecomendationBtns:
            if self.tabWidget.currentIndex() == 0:    
                self.gridLayout_3.addWidget(btn,r, c)
            elif self.tabWidget.currentIndex() == 1:
                self.gridLayout_5.addWidget(btn,r, c)
            c+=1
            if c == 5:
                c= 0
                r+=1
        CurrentWord = ""
        self.recomendFunc()

        # if index == 2 and self.characterLoaded == False:
        #     self.loadCharacters()
        #     self.characterLoaded = True
        # if index == 3 and self.emojiLoaded == False:
        #     self.loadEmojies()
        #     self.emojiLoaded = True
                
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
        kb.tap(Key.esc)
        self.initState()   
        self.sfx()  
    def logCha(self, Cha): 
        try:    
            kb.type(Cha) 
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
        self.sfx()
    def winClicked(self):
        if self.winState == False:
            kb.press(Key.cmd)
            self.winState = True
            self.pushButton_50.setStyleSheet(self.changeStatedStylesheet)  
            return
        if self.winState == True:
            kb.release(Key.cmd)
            self.winState = False
            self.pushButton_50.setStyleSheet("")
            return  
        self.sfx()      
    def altClicked(self):
        if self.altState == False:
            kb.press(Key.alt)
            self.altState=True
            self.pushButton_51.setStyleSheet(self.changeStatedStylesheet)
            self.pushButton_53.setStyleSheet(self.changeStatedStylesheet)
            return
        if self.altState == True:
            kb.release(Key.alt)
            self.altState=False
            self.pushButton_51.setStyleSheet("")
            self.pushButton_53.setStyleSheet("")
        self.sfx()    
    def ctrlClicked(self):
        if self.ctrlState == False:
            kb.press(Key.ctrl)
            self.ctrlState = True
            self.pushButton_49.setStyleSheet(self.changeStatedStylesheet)
            return
        if self.ctrlState == True:
            kb.release(Key.ctrl)
            self.ctrlState = False
            self.pushButton_49.setStyleSheet("")
            return
        self.sfx()       
    def shiftClicked(self):
        if self.shiftState == False:
            kb.press(Key.shift)
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
            kb.release(Key.shift)
            
            for btn in self.latter_btns:
                btnText = (btn.text()).lower()
                btn.setText(btnText)  
            for btn, cha in zip(self.btsForNorChar, self.norCha):
                btn.setText(cha)
            self.shiftState = False
            self.pushButton_81.setStyleSheet("")    
            self.pushButton_115.setStyleSheet("")    

            return 
        self.sfx()         
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
        self.sfx()     
    def engishLogIn(self, char): 
        if self.BanglishCheckBox.isChecked() == False or any([self.ctrlState, self.altState, self.winState]):
            if any([self.ctrlState, self.altState, self.winState]):
                kb.tap(char)  
            else:
                kb.type(char)
                CurrentWord += char
                self.recomendFunc()

            self.initState()     
        elif self.BanglishCheckBox.isChecked() == True:
            self.sendBanglishFor(char) 
        self.sfx()        
    def EnterClicked(self):
        kb.tap(Key.enter)
        self.initState()
        self.sfx()
    def deleteClicked(self):
        kb.tap(Key.delete)
        self.initState()
        self.sfx()
    def BackSpaceClicked(self):
        kb.tap(Key.backspace)
        global wordSofar
        global CurrentWord
        if CurrentWord != "": 
            try:
                CurrentWord = CurrentWord[:-1]
            except Exception:
                CurrentWord = "" 
                self.cleanRecomendations()

            self.initState()
        elif wordSofar != "":
            try:
                wordSofar = wordSofar[:-1]
            except Exception:
                wordSofar = ""
                self.cleanRecomendations()

        self.sfx()
    def tabClicked(self):
        kb.tap(Key.tab)
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
    def returnCurrentWord(self):
        global CurrentWord
        
        return CurrentWord
    def completFunc(self, selectedWord):
        # global wordSofar
        global CurrentWord

        # if CurrentWord == "":
        #     CurrentWord = wordSofar
        
        kb.type(self.subsTrack(selectedWord, CurrentWord))
        if self.SpaceCheckBox.isChecked() == True:
            kb.type(" ")
        CurrentWord = ""
        self.recomendFunc()
    
    def recomendFunc(self):
        global CurrentWord
        
        if CurrentWord == "":
            for btn in self.RecomendationBtns:
                btn.setText("")
            return    
        self.RecomendationList = []

        # if self.tabWidget.currentIndex() == 0:
        #     list_ = BanglaWords

        if self.tabWidget.currentIndex() == 1:
            list_ = EnglishwordsList
            
        for word in list_[:]:
            if word[:len(CurrentWord)] == CurrentWord and word not in self.RecomendationList:
                self.RecomendationList.append(word)
            if len(self.RecomendationList) > 9:
                break
        if len(self.RecomendationList) == 0:
            for word in list_:
                similarity = similarity_ration_btween(word, CurrentWord)
                if similarity > 0.70 and word not in self.RecomendationList:
                    self.RecomendationList.append(word) 
        for wrd, btn in zip(self.RecomendationList, self.RecomendationBtns):
            btn.setText(wrd)

    def logIn(self, char): # bangla cha log in  ==========================================> 
        global CurrentWord
        
        if self.UnicodeRadioButton.isChecked():   
            kb.type(char)
        if char == "???":
            kb.tap(Key.left)
            kb.type(convert("???"))
            kb.tap(Key.right)
            kb.type(convert("???"))
        if char == "???":
            kb.tap(Key.left)
            kb.type(convert("???"))
            kb.tap(Key.right)
            kb.type("X")  
        if self.ANSI_radioButton.isChecked() and char not in ["???", "???"]:  
            sendClip(convert(char))
            # kb.type(convert(char))  
            pass
        CurrentWord += char
        
        self.bangla_word_signal.emit(CurrentWord)
        self.sfx()
    def sfx(self):
        if self.SFXcheckBox.isChecked() == True:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            pass
    def spaceClicked(self):
        global CurrentWord
        
        kb.tap(Key.space)
        if CurrentWord != "":
            CurrentWord = ""
            self.recomendFunc()
            self.initState() 
            self.englishWordSofar = ""
            self.previous_word = ""
            self.formar_previous_word = ""
            self.previous_formar_previous_word = ""
            self.formar_previous_formar_previous_word = ""
            self.initBanglaThread_signal.emit("dfdf")
            self.initThread_signal.emit("init") 
        self.cleanRecomendations()
        initGlobal()
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

                if cha in ["???", "???", "???"]:
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
            try:    
                groupCharec = (groupParts[1].split("|"))
            except Exception:
                print(groupName)
                continue
            groupBox = QGroupBox()
            groupBox.setTitle(groupName)

            self.gridLayout2 = QGridLayout(groupBox)
            self.gridLayout2.setContentsMargins(0,0, 0,0)
            self.gridLayout2.setSpacing(1)
            rowcount = 0
            columnCount = 0
            columnNum = 20

            global emojiDictionary 
            global emoji_list

            for cha in groupCharec[:]:
                if len(cha) == 0:
                    continue
                try:
                    chaParts = cha.split(",")

                    emoji = chaParts[0]
                    
                    if len(emoji) != 1 and groupName != "flag":
                        continue

                    name = chaParts[1].replace("\n", "")

                    emoji_propa = []
                    emoji_propa.append(emoji)
                    emoji_propa.append(name)
                    emojiDictionary.append(emoji_propa)
                    emoji_list.append(emoji) 

                    self.btn2 = QPushButton((emoji).replace("\n", ""))

                    self.btn2.setMinimumSize(25, 25)

                    text = self.btn2.text()
                    try:    
                        self.btn2.clicked.connect(lambda ch, text=text : self.logEmojie(text))
                    except Exception as e:
                        print(e)
                        pass
                    self.btn2.setToolTip(name)
                    self.gridLayout2.addWidget(self.btn2,rowcount, columnCount)
                    columnCount +=1
                    if columnCount == columnNum:
                        rowcount +=1
                        columnCount = 0 
                except Exception:
                    print(cha)

            # print(emojiDictionary)
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
        if self.BanglishCheckBox.isChecked() == True:
           self.BanglishCheckBox.setChecked(False)
        self.close()
        # self.hide()  

class listContextClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(listContextClass, self).__init__()
        uic.loadUi('.//Uis//ListContextUi.ui', self)
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        User32.SetWindowLongW(int(self.winId()), -20, 134217728)
class NumberWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.number_layout = QVBoxLayout()

        self.number_layout.setContentsMargins(0, 2, 0, 2)

        self.setLayout(self.number_layout)

    def add_number(self, number):
        label = QLabel(str(number))
        self.number_layout.addWidget(label)

    def clear_numbers(self):
        while self.number_layout.count() > 0:
            item = self.number_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()



class listViewClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(listViewClass, self).__init__()
        uic.loadUi('.//Uis//Completor.ui', self)
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        User32.SetWindowLongW(int(self.winId()), -20, 134217728)

        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000
        
        hWnd = int(self.winId())
        currentStyle = ctypes.windll.user32.GetWindowLongW(hWnd, GWL_EXSTYLE)

        ctypes.windll.user32.SetWindowLongW(hWnd, GWL_EXSTYLE, currentStyle | WS_EX_NOACTIVATE)

        self.pined = False
        self.PinPushButton.clicked.connect(self.pinStateChanged)
        # self.listWidget.itemClicked.connect(self.WordClicked)c   clalaustrophobic claustrophobic
        self.listWidget.setUniformItemSizes(True)


        # self.listWidget.setWindowOpacity(0.8)
        # self.listWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.listWidget.setStyleSheet("background: transparent;")

        blur = QtWidgets.QGraphicsBlurEffect()
        blur.setBlurRadius(5)
        # self.listWidget.setGraphicsEffect(blur)  action replay

        # self.frame_2.setGraphicsEffect(blur) 
        # self.frame_2.setWindowOpacity(0.9)


        # Make the list widget text clearly readable
        # opacity_effect = QGraphicsOpacityEffect()
        # opacity_effect.setOpacity(0.9)
        # self.frame_2.setGraphicsEffect(opacity_effect)


        self.matchedWords = []
        self.currentWords = []
        self.clicked = False
        self.comButtonsBlocked = False
        self.Doc_pad = Script_pad.Ui_nms_pad()

        self.SpellCheckPushButton.setToolTip("Spell Check")

        self.SpellCheckPushButton.clicked.connect(self.spellCheckFunc)
        self.threadRunning = False

        self.Settings_menu_for_completor = QMenu("Settings")

        self.dont_show_on_this_window_menu = QAction('Do not suggest for this window', self) # can you here me bro
        self.cancel_menu = QAction('Cancel', self)
        
        self.Settings_menu_for_completor.addAction(self.dont_show_on_this_window_menu)

        self.Settings_btn.setMenu(self.Settings_menu_for_completor)

        self.number_widget = NumberWidget()
        self.verticalLayout.addWidget(self.number_widget)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frame.setVisible(False)

    def action1_triggered(self):
        # selected_item = self.listWidget.currentItem()
        
        # print(self.listWidget.itemFromIndex(self.index).text())
        
        # item_text = selected_item.text()
        # print(item_text)        
        pass

    def spellCheckFunc(self):
        global wordSofar
        global englishWordSofar
        self.SpellCheckPushButton.setEnabled(False)
        self.spellCheckThread = AdvanceSimilarityThread(wordSofar, englishWordSofar)
        self.spellCheckThread.mostMatchedWords.connect(self.populateWithSimilarWords)
        self.spellCheckThread.start()
        pass
    
    def threadRunningStateChangeFunc(self, state):
        self.threadRunning = state
        self.SpellCheckPushButton.setEnabled(not state)
    def pinStateChanged(self):
        if self.pined == False:
            self.pined = True
            self.PinPushButton.setText("????")
        else:
            self.pined = False
            self.PinPushButton.setText("????")

        pass
        kb.press(Key.f23)
        kb.release(Key.f23)
    @QtCore.pyqtSlot(list)
    def populateWithSimilarWords(self, words):
        self.populateWords(words)
        self.SpellCheckPushButton.setEnabled(True)

    @QtCore.pyqtSlot(list)
    def populateWords(self, words):
        # self.show()
        # print(words)
        global using_functionKeys
        try:
            while("" in words):
                words.remove("")
            self.listWidget.clear()
            c = 0
            self.number_widget.clear_numbers()
            for item in words[:10]:
                if self.listWidget.findItems(item, Qt.MatchExactly) or "??????" in item or "??????" in item:
                    continue
                
                if c== 1:
                    bold_font = QFont()
                    bold_font.setBold(True)
                    item1 = QListWidgetItem(item)
                    item1.setFont(bold_font)
                    self.listWidget.addItem(item)    
                else:
                    self.listWidget.addItem(item)    
                

                c += 1
                if using_functionKeys:    
                    self.number_widget.add_number(c)
                # self.listWidget.addItems(words)  action peplay why are action action
            self.currentRow = 0
            
            # self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 8 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth()+ 8)   
            # self.frame_2.setFixedSize(self.listWidget.sizeHintForColumn(0) + 5 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth()) 
            
            self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 12 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 4 * self.listWidget.frameWidth()+ 14)   
            self.frame_2.setFixedSize(self.listWidget.sizeHintForColumn(0) + 12 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 4 * self.listWidget.frameWidth()) 
            

            # self.GetCaretPosInWindow()

        except Exception as e:
            print(f"{e} , in populate words function listview")    
    @QtCore.pyqtSlot(list)
    def populateSimilarWords(self, simiWords):
        self.listWidget.addItems(simiWords)
        self.currentRow = 0
        self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 10 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth())   
    def initSelf(self):
        if self.isHidden() == False:    
            self.listWidget.clear()
            self.showHideFunc("hide")
            # print("green them called!")
    def showHideFunc(self, sig):
        if sig == "show":
            if self.isHidden() == True:
                self.show()
                global using_tab
                global using_arrow
                if self.comButtonsBlocked == False:
                    try:
                        if using_arrow:
                            for i in [80, 72]: # 28 ,
                                kb2.block_key(i)
                        if using_tab:
                            kb2.block_key(15)     
                    except Exception as e:
                        print(traceback.format_exc()) 
                    self.comButtonsBlocked = True  
                self.changeTheme("green")
        if sig == "hide":    
            if self.pined == False:
                self.hide()
                try:
                    if self.comButtonsBlocked == True:
                        kb2.unhook_all()
                        self.comButtonsBlocked = False         
                except Exception as e:
                    pass 
        pass
    @QtCore.pyqtSlot(str)
    def changeTheme(self, theme):
        # print(theme)
        # return
        if theme == "green":
            self.frame_2.setStyleSheet(DefultTheme)
        if theme == "red":
            self.frame_2.setStyleSheet(RedTheme)
        if theme == "blue":
            self.frame_2.setStyleSheet(BlueTheme)  
        if theme == "yellow":
            self.frame_2.setStyleSheet(YellowTheme)
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
    def enterEvent(self, a0: QtCore.QEvent) -> None: # hover in 
        self.frame.setVisible(True)

        self.firstBtnAnimation = QPropertyAnimation(self.SpellCheckPushButton, b"geometry")
        self.firstBtnAnimation.setEasingCurve(QEasingCurve.Linear)
        self.firstBtnAnimation.setDuration(150)
        self.firstBtnAnimation.setStartValue(QRect(30, 1, 28, 20))
        self.firstBtnAnimation.setEndValue(QRect(2, 1, 28, 20))
        self.firstBtnAnimation.easingCurve
        self.firstBtnAnimation.start()


        self.SecondBtnAnimation = QPropertyAnimation(self.ACcheckBox, b"geometry")
        self.SecondBtnAnimation.setEasingCurve(QEasingCurve.Linear)
        self.SecondBtnAnimation.setDuration(150)
        self.SecondBtnAnimation.setStartValue(QRect(33, -21, 37, 20))
        self.SecondBtnAnimation.setEndValue(QRect(33, 1, 37, 20))
        self.SecondBtnAnimation.easingCurve
        self.SecondBtnAnimation.start()


        self.thirdBtnAnimation = QPropertyAnimation(self.PinPushButton, b"geometry")
        self.thirdBtnAnimation.setEasingCurve(QEasingCurve.Linear)
        self.thirdBtnAnimation.setDuration(150)
        self.thirdBtnAnimation.setStartValue(QRect(30, 1, 28, 20))
        self.thirdBtnAnimation.setEndValue(QRect(72, 1, 28, 20))
        self.thirdBtnAnimation.easingCurve
        self.thirdBtnAnimation.start()


        return super().enterEvent(a0)
    def leaveEvent(self, a0: QtCore.QEvent) -> None: # hover out
        self.frame.setVisible(False)
        return super().leaveEvent(a0)



class Ui(QtWidgets.QMainWindow):
    word_signal = pyqtSignal(str, str, str)
    initThread_signal = pyqtSignal(str)
    bangla_word_signal = pyqtSignal(str)
    initBanglaThread_signal = pyqtSignal(str)
    def __init__(self):
        super(Ui, self).__init__() 
        uic.loadUi('.//Uis//Main_GUI.ui', self) 
        
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint ) # | QtCore.Qt.Tool
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.move(890, 0)
        User32.SetWindowLongW(int(self.winId()), -20, 134217728)
    
        self.UANSI_pos = False
        self.progressBar.setVisible(False)
        # self.OCR_Btn.clicked.connect(self.Open_OCR)

        self.abbries_dic = {}
    # imgs ====================================
        # pixmap = QtGui.QPixmap(".//Uis//Imgs//Cursor.png")
        # cursor = QCursor(pixmap, 0, 0)
        # QApplication.setOverrideCursor(cursor)
        stop_icon = QtGui.QIcon()
        stop_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Stop 2 png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Stop_btn.setIcon(stop_icon)
        doc_icon = QtGui.QIcon()
        doc_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Doc pad PNG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ScriptPad_btn.setIcon(doc_icon)

        converter_icon = QtGui.QIcon()
        converter_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//OSK logo png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OnScreenKeyboardBtn.setIcon(converter_icon)

        wav_to_text_icon = QtGui.QIcon()
        wav_to_text_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Wav to text 2 png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Wav_to_Text_button.setIcon(wav_to_text_icon)
        Settings_icon = QtGui.QIcon()
        Settings_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Gear 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Settings_btn.setIcon(Settings_icon)
        Closer_icon = QtGui.QIcon()
        Closer_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Close final correction.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_btn.setIcon(Closer_icon)
        self.OCR_menu = QMenu()
        self.OCR_Btn.setMenu(self.OCR_menu)
        self.screen_shot_menu = self.OCR_menu.addAction('Screen Shot')
        self.screen_shot_menu.triggered.connect(self.screenShot)

        self.OCR_OPtion = self.OCR_menu.addAction('OCR')
        self.OCR_OPtion.triggered.connect(self.Open_OCR)

        self.OCR_OPtion = self.OCR_menu.addAction('OCR from Screen')
        self.OCR_OPtion.triggered.connect(self.Open_OCR_from_screen)
    # imgs ====================================

        self.oldPos = self.pos()
        self.first_animation = True 
        self.Listining_label.setVisible(False)
        self.show()
        self.Stop_btn.setVisible(False)
        self.Mic_btn.clicked.connect(self.Mic_pressed)
        self.Mic_btn.setFocusPolicy(Qt.NoFocus)
        self.Close_btn.clicked.connect(self.close_function)
        self.OnScreenKeyboardBtn.clicked.connect(self.Open_OSK)  
        self.Settings_menu = QMenu()
        self.Settings_btn.setMenu(self.Settings_menu)
        self.application_menue = QMenu()
        self.Close_btn.setMenu(self.application_menue)
        with open('.//Res//Use_ANSI.txt', "w") as UANSI:
            UANSI.write("False")
        with open('.//Res//Run_at_startup.txt', "r") as RKS:
            RKS_pos = RKS.read()                      
        # self.Lang_comboBox.currentIndexChanged.connect(self.update_lang)
        # self.Settings_menu.addSeparator()
        self.exit_menu = QAction('Exit', self)
        self.exit_menu.triggered.connect(self.close_function)
        close_icon = QtGui.QIcon()
        close_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//CloseIconPng.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_menu.setIcon(close_icon)
        self.Restart_menu = QAction('Restart', self)
        self.Restart_menu.triggered.connect(self.restart_function)
        

        self.Ansi_ = QAction('as ANSI', self, checkable=True, checked=False)
        self.Ansi_.triggered.connect(self.Ansi)
        self.Unicode_ = QAction('as Unicode', self, checkable=True, checked=True)
        self.Unicode_.triggered.connect(self.Unicode)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.listClass = listViewClass()
        self.listClass.hide()


        self.listClass.dont_show_on_this_window_menu.triggered.connect(self.DontShowFunc)



        self.taking_commend = QAction('Bijoy classic', self, checkable=True, checked=False)
        self.taking_commend.triggered.connect(self.Take_commend)
        self.taking_cmd = False 
        Bangla_output = self.Settings_menu.addMenu('Bangla Output')
        
        Bangla_output.addAction(self.Unicode_)
        Bangla_output.addAction(self.Ansi_)
        # Bangla_output.addAction(self.taking_commend)

        keyboard_layout_menu = self.Settings_menu.addMenu('Keyboard Layout')

        self.Banglish_layout = QAction('Banglish', self, checkable=True, checked=True)
        self.Banglish_layout.triggered.connect(lambda:self.Bijoy_layout.setChecked(not self.Banglish_layout.isChecked()))
        self.Bijoy_layout = QAction('Bijoy', self, checkable=True, checked=False)
        self.Bijoy_layout.triggered.connect(lambda: self.Banglish_layout.setChecked(not self.Bijoy_layout.isChecked()))
        
        keyboard_layout_menu.addAction(self.Banglish_layout)
        keyboard_layout_menu.addAction(self.Bijoy_layout)


        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.Settings_menu.addSeparator() # =================== menue
        # self.Settings_menu.addAction(self.taking_commend)
        self.Mic_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Settings_menu.addSeparator()
        self.Conveter = self.Settings_menu.addAction('Unicode from/to Bijoy conveter')
        self.Conveter.triggered.connect(self.Open_converter_exe)  # < ------------------
        conveter_icon = QtGui.QIcon()
        conveter_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Converter logo for main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Conveter.setIcon(conveter_icon)
        self.Settings_menu.addSeparator() # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.Options = self.Settings_menu.addAction('Settings')
        self.Options.triggered.connect(self.showSettings)
        settings_icon = QtGui.QIcon()
        settings_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//gear 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Options.setIcon(settings_icon)
        self.Settings_menu.addSeparator() # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # if RKS_pos == "True":
        #     self.RunAtAtartUpCheckBox.setChecked(True) 
        # if RKS_pos == "False":
        #     self.RunAtAtartUpCheckBox.setChecked(False)
        # self.RunAtAtartUpCheckBox.stateChanged.connect(self.Run_startup_fun)
        self.Settings_menu.addSeparator() # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.trackClipSetting = QSettings("TrackClip")
        
        # self.VocabularyMeni = self.Settings_menu.addMenu('Vocabulary List')
   
        self.wordManagerMenu = QAction('Word Manager', self)
        self.wordManagerMenu.triggered.connect(self.ShowWordManager)
        self.Settings_menu.addAction(self.wordManagerMenu)
        self.Settings_menu.addSeparator()
        self.About = self.Settings_menu.addAction('about Nms Kontho')
        Kontho_icon = QtGui.QIcon()
        Kontho_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Kontho png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.About.setIcon(Kontho_icon)
        self.About.triggered.connect(self.About_nms)
        # self.current_version = self.Settings_menu.addAction('Current Version')
        # self.current_version.triggered.connect(self.current_version_check)
        self.help_options = self.Settings_menu.addMenu('Help')
        self.help_options.addAction("Banglish Layout Map")
        self.help_options.triggered.connect(self.openBanglishLayout)
        self.clicked = False
        self.ScriptPad_btn.clicked.connect(self.Open_doc_pad) 
        self.Wav_to_Text_button.clicked.connect(self.Open_Wave_to_text_generator)
        self.Stop_btn.clicked.connect(self.Stop_thread)
        self.init_animation()

        self.dance_time = QTimer()
        self.dance_time.timeout.connect(self.aro_button_clicked)

        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.Stop_thread)
        

        self.settingsGUIClass = Options_UI()    # <------------------ 
        self.settingsGUIClass.RunAtAtartUpCheckBox.stateChanged.connect(self.Run_startup_fun)
        
        self.MainSettings = QSettings("MainSettings")
        self.ownSettings = OwnSettings()
        self.settingsGUIClass.AutoCloseCheckBox.stateChanged.connect(self.autoCloseBra)
        self.settingsGUIClass.UseAbrisCheckBox.stateChanged.connect(self.useAbries)
        self.settingsGUIClass.ShowReacorCheckBox.stateChanged.connect(self.showAudioReactor)
        self.settingsGUIClass.NumOfWrdPredictionSpinBox.valueChanged.connect(self.predictionValueChanged)
        self.settingsGUIClass.SimiDoubleSpinBox.valueChanged.connect(self.similarityValueChanged)
        self.settingsGUIClass.TabCheckBox.stateChanged.connect(self.using_tab_stateChanged)
        self.settingsGUIClass.ArrowCheckBox.stateChanged.connect(self.using_arrow_stateChanged)
        self.settingsGUIClass.Function_checkBox.stateChanged.connect(self.using_funcKeys_stateChanged)

        with open('.//Res//SuggestBangla.txt', "r") as file:
            self.suggestForBangla = (file.read())
        if self.suggestForBangla == "False":
            self.settingsGUIClass.banglaSuggestCheckBox.setChecked(False) 
            self.suggestForBangla = False
        else:
            self.settingsGUIClass.banglaSuggestCheckBox.setChecked(True) 
            self.suggestForEnglish = True

        with open('.//Res//SuggestEnglish.txt', "r") as file:
            self.suggestForEnglish = (file.read())

        if self.suggestForEnglish == "False":
            self.settingsGUIClass.EnglishSuggestCheckBox.setChecked(False)
        else:
            self.settingsGUIClass.EnglishSuggestCheckBox.setChecked(True)

        self.settingsGUIClass.banglaSuggestCheckBox.stateChanged.connect(self.banglaSuggest)
        self.settingsGUIClass.EnglishSuggestCheckBox.stateChanged.connect(self.englishSuggest)
        self.settingsGUIClass.SuggestEmojiesCheckBox.stateChanged.connect(self.emojiSuggest)
        self.settingsGUIClass.SelectionRadioButton.clicked.connect(self.triggerSelectionSettingFunc2)
        self.settingsGUIClass.EnterToSelectRadioButton.clicked.connect(self.triggerSelectionSettingFunc1)

        self.settingsGUIClass.SelectionRadioButton.setChecked(self.ownSettings.value("selection_checked2"))
        self.settingsGUIClass.EnterToSelectRadioButton.setChecked(self.ownSettings.value("selection_checked1"))
        # try:
        self.settingsGUIClass.RunAtAtartUpCheckBox.setChecked(bool(self.MainSettings.value("runAtStartUp")))  

        self.settingsGUIClass.AutoCloseCheckBox.setChecked(bool(self.MainSettings.value("AutoCloseBrackets")))
        self.AutoCloseBra = bool(self.MainSettings.value("AutoCloseBrackets"))
          
        self.settingsGUIClass.ShowReacorCheckBox.setChecked(bool(self.MainSettings.value("ShowAudioReactor")))  
        self.settingsGUIClass.NumOfWrdPredictionSpinBox.setValue(self.MainSettings.value("NumberOfPrediction"))  
        self.settingsGUIClass.SimiDoubleSpinBox.setValue(float(self.MainSettings.value("minimumSimilarity"))) 
        self.settingsGUIClass.ResetSimipushButton.clicked.connect(lambda: self.settingsGUIClass.SimiDoubleSpinBox.setValue(0.7))   


        self.settingsGUIClass.UseAbrisCheckBox.setChecked((self.ownSettings.value("UseAbries"))) 


        global suggestEmoji
        suggestEmoji = self.ownSettings.value("suggestEmojies")
        self.settingsGUIClass.SuggestEmojiesCheckBox.setChecked(suggestEmoji) 
         
        global using_tab
        using_tab = self.ownSettings.value("using_tab")
        self.settingsGUIClass.TabCheckBox.setChecked(using_tab)  
            
        global using_arrow
        using_arrow = (self.ownSettings.value("using_arrow"))
        self.settingsGUIClass.ArrowCheckBox.setChecked(using_arrow)

        try:
            global using_functionKeys
            using_functionKeys = (self.ownSettings.value("using_functionKeys"))
            
            self.settingsGUIClass.Function_checkBox.setChecked(using_functionKeys)


        except Exception:
            pass

        global minimun_Similarity_Ratio
        minimun_Similarity_Ratio = float(self.MainSettings.value("minimumSimilarity"))
        # except Exception as e:
        #     print(e)

        self.current_language = "English"
        self.Lang_Button.clicked.connect(self.update_lang) 

        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = ""
        self.shiftKeyBlocked = False
        self.keysBlocked = True
        
        self.converter_gui = Converter_for_main.Ui_converter()

        
        self.show_tray_menu = QAction('Move to tray', self)
        self.show_tray_menu.triggered.connect(self.show_tray_icon)
        
        self.tray_icon = QSystemTrayIcon()

        self.tray_icon.activated.connect(self.tray_icon_clicked)

        tray_menu = QMenu()
        self.show_top_bar_menu = QAction('Restore top bar', self)
        self.show_top_bar_menu.triggered.connect(self.show_top_bar)
        tray_menu.addAction(self.show_top_bar_menu)
        tray_menu.addMenu(self.Settings_menu)
        tray_menu.addSeparator()
        
        tray_menu.addAction(self.exit_menu)

        self.tray_icon.setContextMenu(tray_menu)

        
        self.application_menue.addAction(self.show_tray_menu)
        self.application_menue.addAction(self.Restart_menu)
        self.application_menue.addAction(self.exit_menu)
        

        
        self.numDic = {'1':'???','2':'???','3':'???','4':'???','5':'???','6':'???','7':'???','8':'???','9':'???','0':'???'}
        self.qoteDic = {'(':')', '[':']', '{':'}'}
        self.karList = ["???","???","???","???","???","???","???","???","???","???"]
        self.keysToBlock = [2,3,4,5,6,7,8,9,10,11,  16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,   44,45,46,47,48,49,50,  52]    
        self.keysToUnlock = [2,3,4,6,8,9,10,11,52]   # this keys are unlocked when shift is pressed 
        self.keysToBlockWhenShiftKeyIsPressed = [5,7, 16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,39,   44,45,46,47,48,49,50]
        self.wordSelectionKeys = [15,28,80,72]

        self.oskClass = OSK_UI()
        
    # osk class connectors ========================================================================>

        self.oskClass.pushButton_199.clicked.connect(self.OSKBackSpaceClicked)

        self.oskClass.pushButton_33.clicked.connect(lambda: self.on_osk_press(str("key.backspace")))

        self.oskClass.pushButton_78.clicked.connect(lambda: self.on_osk_press(str("key.delete")))
        self.oskClass.pushButton_47.clicked.connect(self.oskClass.EnterClicked)
        self.oskClass.pushButton_64.clicked.connect(self.oskClass.tabClicked)
        self.oskClass.pushButton_19.clicked.connect(self.oskClass.escFunc)
        
        self.oskClass.pushButton_201.clicked.connect(self.spaceClicked)
        self.oskClass.pushButton_52.clicked.connect(self.spaceClicked)
        self.oskClass.pushButton_20.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_20.text())))
        self.oskClass.pushButton_21.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_21.text())))
        self.oskClass.pushButton_22.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_22.text())))
        self.oskClass.pushButton_23.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_23.text())))
        self.oskClass.pushButton_24.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_24.text())))
        self.oskClass.pushButton_25.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_25.text())))
        self.oskClass.pushButton_26.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_26.text())))
        self.oskClass.pushButton_27.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_27.text())))
        self.oskClass.pushButton_28.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_28.text())))
        self.oskClass.pushButton_29.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_29.text())))
        self.oskClass.pushButton_30.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_30.text())))
        self.oskClass.pushButton_31.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_31.text())))
        self.oskClass.pushButton_32.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_32.text())))
        self.oskClass.pushButton_65.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_65.text())))
        self.oskClass.pushButton_66.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_66.text())))
        self.oskClass.pushButton_67.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_67.text())))
        self.oskClass.pushButton_68.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_68.text())))
        self.oskClass.pushButton_69.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_69.text())))
        self.oskClass.pushButton_70.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_70.text())))
        self.oskClass.pushButton_71.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_71.text())))
        self.oskClass.pushButton_72.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_72.text())))
        self.oskClass.pushButton_73.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_73.text())))
        self.oskClass.pushButton_74.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_74.text())))
        self.oskClass.pushButton_75.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_75.text())))
        self.oskClass.pushButton_76.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_76.text())))
        self.oskClass.pushButton_77.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_77.text())))
        self.oskClass.pushButton_36.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_36.text())))
        self.oskClass.pushButton_37.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_37.text())))
        self.oskClass.pushButton_38.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_87.text())))
        self.oskClass.pushButton_39.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_39.text())))
        self.oskClass.pushButton_40.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_40.text())))
        self.oskClass.pushButton_41.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_41.text())))
        self.oskClass.pushButton_42.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_42.text())))
        self.oskClass.pushButton_43.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_43.text())))
        self.oskClass.pushButton_44.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_44.text())))
        self.oskClass.pushButton_45.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_45.text())))
        self.oskClass.pushButton_46.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_46.text())))
        self.oskClass.pushButton_84.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_84.text())))
        self.oskClass.pushButton_102.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_102.text())))
        self.oskClass.pushButton_106.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_106.text())))
        self.oskClass.pushButton_107.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_107.text())))
        self.oskClass.pushButton_108.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_108.text())))
        self.oskClass.pushButton_109.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_109.text())))
        self.oskClass.pushButton_110.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_110.text())))
        self.oskClass.pushButton_111.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_111.text())))
        self.oskClass.pushButton_112.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_112.text())))
        self.oskClass.pushButton_113.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_113.text())))       
        self.oskClass.pushButton_38.clicked.connect(lambda: self.on_osk_press(str(self.oskClass.pushButton_38.text())))     
        self.oskClass.pushButton_114.clicked.connect(lambda: kb.tap(Key.up))
        self.oskClass.pushButton_54.clicked.connect(lambda: kb.tap(Key.left))
        self.oskClass.pushButton_55.clicked.connect(lambda: kb.tap(Key.down))
        self.oskClass.pushButton_56.clicked.connect(lambda: kb.tap(Key.right))
        self.oskClass.pushButton_48.clicked.connect(lambda: self.on_osk_press(str("key.home")))
        self.oskClass.pushButton_116.clicked.connect(lambda: self.on_osk_press(str("key.end")))

        self.oskClass.RB1.clicked.connect(self.rb1Clicked)
        self.oskClass.RB2.clicked.connect(self.rb2Clicked)
        self.oskClass.RB3.clicked.connect(self.rb3Clicked)
        self.oskClass.RB4.clicked.connect(self.rb4Clicked)
        self.oskClass.RB5.clicked.connect(self.rb5Clicked)
        self.oskClass.RB6.clicked.connect(self.rb6Clicked)
        self.oskClass.RB7.clicked.connect(self.rb7Clicked)
        self.oskClass.RB8.clicked.connect(self.rb8Clicked)
        self.oskClass.RB9.clicked.connect(self.rb9Clicked)
        self.oskClass.RB10.clicked.connect(self.rb10Clicked)

        self.oskClass.BanglishCheckBox.stateChanged.connect(self.BanglishCheckBoxStateChanged)
        self.oskClass.OpenLayOutPushButton.clicked.connect(lambda: self.openBanglishLayout())

        # bangla connectors ========================================================================

        # banglakeyboard connectors ===========================
        self.oskClass.Ao_pushButton.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.Aa_pushButton.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_85.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_80.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_82.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_88.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_87.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_79.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_83.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_86.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_89.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_155.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_156.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.Deghi_pushButton.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_158.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_159.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_160.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_161.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_162.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_163.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_164.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_101.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_91.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_96.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_133.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_138.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_148.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_93.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_141.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_92.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_145.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_150.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_151.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_135.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_153.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_140.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_143.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_104.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_132.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_99.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_103.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_142.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_131.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_94.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_147.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_100.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_95.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_134.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.Lo_pushButton.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_90.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_97.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_137.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_146.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_149.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_144.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_98.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_105.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_136.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_139.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_152.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_154.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_165.clicked.connect(lambda:self.logIn("??????"))
        self.oskClass.pushButton_166.clicked.connect(lambda:self.logIn("??????"))
        self.oskClass.pushButton_170.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_167.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_173.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_169.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_171.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_172.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_168.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_175.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_174.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_176.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_186.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_193.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_185.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_187.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_188.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_194.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_191.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_183.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_190.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_195.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_189.clicked.connect(lambda:self.logIn("?????????"))
        self.oskClass.pushButton_177.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_178.clicked.connect(lambda:self.logIn(","))
        self.oskClass.pushButton_179.clicked.connect(lambda:self.logIn("?"))
        self.oskClass.pushButton_180.clicked.connect(lambda:self.logIn(";"))
        self.oskClass.pushButton_181.clicked.connect(lambda:self.logIn(":"))
        self.oskClass.pushButton_182.clicked.connect(lambda:self.logIn("???"))
        self.oskClass.pushButton_192.clicked.connect(lambda:self.logIn("!"))
        self.oskClass.pushButton_184.clicked.connect(lambda:self.logIn("@"))
        self.oskClass.pushButton_196.clicked.connect(lambda:self.logIn("("))
        self.oskClass.pushButton.clicked.connect(lambda:self.logIn(")"))

# /osk class connectors ========================================================================>
        self.Doc_pad = Script_pad.Ui_nms_pad()
        self.lastActiveWindow = ""
        self.firstTime = True


        self.listClass.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listClass.listWidget.customContextMenuRequested.connect(self.open_menu)
        
        self.contextClass = listContextClass()
        self.contextClass.listWidget.itemClicked.connect(self.ContextMenuClicked)
        
        kb2.on_press(self.on_press_2)

        
        
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
        self.listener.start()

        # self.blockWordSelectionKeys()
        
        self.MouseListener = mouse.Listener(on_click = self.on_click)
        self.MouseListener.start()

        self.wordThread_ = wordThread()
        self.wordThread_.matched_Word_signal.connect(self.getRecomendedWords)
        self.wordThread_.caretPosSignal.connect(self.setListPos)
        self.wordThread_.acWordSignal.connect(self.AutoCompleate)
        self.wordThread_.hideSignal.connect(self.listClass.showHideFunc) # self.listClass.showHideFunc
        self.wordThread_.themeSignal.connect(self.listClass.changeTheme)
        self.word_signal.connect(self.wordThread_.run)
        self.initThread_signal.connect(self.wordThread_.initFunc)
        # self.wordThread_.start()

        self.trackingClipBoard = self.ownSettings.value("ClipBoardTracker_checked")
        self.settingsGUIClass.ClipBoardCheckBox.setChecked(self.trackingClipBoard) 
        
        self.clipThread = ClipBoardThreadClass()
        self.clipThread.copy_signal.connect(self.updateClipboard)

        if self.trackingClipBoard:
            self.clipThread.start()
        self.settingsGUIClass.ClipBoardCheckBox.stateChanged.connect(self.clipBoardTracker_stateChanged)    

        ahk.run_script(ahkScript, blocking=False)   # <-------------- 3333333333
        self.wordManagerClass = wordManagerClass()
        self.wordManagerClass.save_signal.connect(self.UpdateLists)

        self.loadAbbribiations()

        self.listClass.listWidget.itemClicked.connect(self.WordClickedMiddleFunc)
        self.autoCompletedWord = ""
        self.reserved = ""
        self.HotKeyPressed = False
        
        self.settingsGUIClass.OpenBanglaDic.clicked.connect(lambda: self.openDic(0))
        self.settingsGUIClass.OpenEnglishDic.clicked.connect(lambda: self.openDic(2))
        self.settingsGUIClass.OpenAbbris.clicked.connect(lambda: self.openDic(3))
        # kb2.unhook_all()
        self.bijoy_Uni_Map = {"q":"???","w":"???","e":"???","r":"???","t":"???","y":"???","u":"???","i":"???","o":"???","p":"???","a":"???","s":"???","d":"???","f":"???","g":"???","h":"???","j":"???","k":"???","l":"???","z":"??????","x":"???","c":"???","v":"???","b":"???","n":"???","m":"???","1":"???","2":"???","3":"???","4":"???","5":"???","6":"???","7":"???","8":"???","9":"???","0":"???","Q":"???","W":"???","E":"???","R":"???","T":"???","Y":"???","U":"???","I":"???","O":"???","P":"???","A":"??????","S":"???","D":"???","F":"???","G":"???","H":"???","J":"???","K":"???","L":"???","Z":"??????","X":"???","C":"???","V":"???","B":"???","N":"???","M":"???","$":"???","&":"???"}
        # ================


        # self.BanglawordThread = BanglawordThread()
        # self.BanglawordThread.matched_Word_signal.connect(self.oskClass.populateWords)
        # self.bangla_word_signal.connect(self.BanglawordThread.run)
        # self.initBanglaThread_signal.connect(self.BanglawordThread.initFunc)
        # self.BanglawordThread.start()
        # self.using_funcKeys_stateChanged()
        self.listClass.ACcheckBox.setChecked(self.ownSettings.value("AC_checked"))
        self.listClass.ACcheckBox.clicked.connect(self.ACBtnStateChanged)

    def clipBoardTracker_stateChanged(self):
        self.trackingClipBoard = self.settingsGUIClass.ClipBoardCheckBox.isChecked()
        self.ownSettings.setValue("ClipBoardTracker_checked", self.trackingClipBoard)

        if self.trackingClipBoard:
            self.clipThread.start()
        else:
            self.clipThread.stop()

    def updateClipboard(self, sig):
        if self.wordManagerClass.isHidden() == False:
            self.wordManagerClass.loadClip()
    def ACBtnStateChanged(self):
        self.ownSettings.setValue("AC_checked", self.listClass.ACcheckBox.isChecked())
    def using_funcKeys_stateChanged(self):
        global using_functionKeys
        using_functionKeys = self.settingsGUIClass.Function_checkBox.isChecked()
        self.listClass.groupBox_3.setVisible(using_functionKeys)
        # print(self.listClass.groupBox_3.isVisible())
        self.ownSettings.setValue("using_functionKeys", using_functionKeys)
    def OSKBackSpaceClicked(self):
        self.listener.stop()
        kb.tap(Key.backspace)
        global wordSofar
        if wordSofar != "":
            try:
                wordSofar = wordSofar[:-1]
            except Exception:
                wordSofar = ""
                self.oskClass.cleanRecomendations()
        
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
        self.listener.start()  
        self.sfx()
    def triggerSelectionSettingFunc2(self):
        state = self.settingsGUIClass.SelectionRadioButton.isChecked()
        self.ownSettings.setValue("selection_checked2", state)
    def triggerSelectionSettingFunc1(self):
        state = self.settingsGUIClass.EnterToSelectRadioButton.isChecked()
        self.ownSettings.setValue("selection_checked1", state)    
    def tempoComplition(self, current, selectedText):
        try:
            print(f"current: {current}, selectedText: {selectedText}")
            times_to_tap_backspace, restOfWord = self.smertCompletor(current, selectedText) 
            self.listener.stop()  
            # print(f"times_to_tap_backspace: {times_to_tap_backspace}, restOfWord: {restOfWord} ")
            
            for i in range(times_to_tap_backspace):
                kb.tap(Key.backspace)
            kb.type(restOfWord)
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
            self.listener.start() 
        except Exception:
            pass
    def stringModarator(self, current, selectedText ):
        for i in range(current):
            pass
    def using_arrow_stateChanged(self):
        global using_arrow
        state = self.settingsGUIClass.ArrowCheckBox.isChecked()  
        using_arrow = state
        self.ownSettings.setValue("using_arrow", state)
    def using_tab_stateChanged(self, state):
        global using_tab
        state = self.settingsGUIClass.TabCheckBox.isChecked()  
        using_tab = state
        self.ownSettings.setValue("using_tab", state)
        # self.MainSettings.setValue("using_tab", str(state))
    def logIn(self, char): # bangla cha log in  ==========================================> 
        global wordSofar
        global CurrentWord
        global englishWordSofar
        
        self.listener.stop()
        if self.oskClass.UnicodeRadioButton.isChecked():   
            kb.type(char)
            wordSofar += char
            englishWordSofar = ""
        # if char == "???":
        #     kb.tap(Key.left)
        #     kb.type(convert("???"))
        #     kb.tap(Key.right)
        #     kb.type(convert("???"))
        # if char == "???":
        #     kb.tap(Key.left)
        #     kb.type(convert("???"))
        #     kb.tap(Key.right)
        #     kb.type("X")  
        if self.oskClass.ANSI_radioButton.isChecked() and char not in ["???", "???"]:  
            # sendClip(convert(char))
            kb.type(convert(char))  
            pass
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
        self.listener.start()  
        # CurrentWord += char
        
        # self.bangla_word_signal.emit(CurrentWord)
        
        self.sfx()
    def spaceClicked(self):
        global CurrentWord
        
        kb.tap(Key.space)
        if CurrentWord != "":
            CurrentWord = ""
            self.oskClass.recomendFunc()
            self.oskClass.initState() 
            self.oskClass.englishWordSofar = ""
            self.oskClass.previous_word = ""
            self.oskClass.formar_previous_word = ""
            self.oskClass.previous_formar_previous_word = ""
            self.oskClass.formar_previous_formar_previous_word = ""
            self.initBanglaThread_signal.emit("dfdf")
            self.oskClass.initThread_signal.emit("init") 
        self.oskClass.cleanRecomendations()
        initGlobal()
    def similarityValueChanged(self, val):
        self.MainSettings.setValue("minimumSimilarity", val)
        global minimun_Similarity_Ratio
        minimun_Similarity_Ratio = val
    def openDic(self, index):
        # if self.wordManagerClass.stufLoaded == False:
            # self.wordManagerClass.loadStuff()
        if index == 0 and self.wordManagerClass.banglaWordsLoaded == False:
            self.wordManagerClass.loadCompleteBanglaWordList()
        if index == 1 and self.wordManagerClass.englishWordsLoaded == False:
            self.wordManagerClass.loadCompleteEnglaWordList()    
        if index == 2 and self.wordManagerClass.englishWordsLoaded == False:
            self.wordManagerClass.loadCompleteEnglishWordList()  
        self.wordManagerClass.show()
        self.wordManagerClass.tabWidget.setCurrentIndex(index)
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            print("Tray icon was double-clicked.")
        elif reason == QSystemTrayIcon.Trigger:
            self.update_lang()
            self.setTrayIcon()
        elif reason == QSystemTrayIcon.MiddleClick:
            print("Tray icon was middle-clicked.")
    def show_top_bar(self):
        self.show()
        self.tray_icon.hide()
        pass
    def setTrayIcon(self):
        try_menu_icon = QtGui.QIcon()
        
        if self.current_language == "English":
            try_menu_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Eng.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.current_language == "Bangla":        
            try_menu_icon.addPixmap(QtGui.QPixmap(".//Uis//Imgs//Ban.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.tray_icon.setIcon(try_menu_icon)
    def show_tray_icon(self):
        
        self.setTrayIcon()
        self.tray_icon.show()
        self.hide()
        pass
    def banglaSuggest(self, state):
        state = self.settingsGUIClass.banglaSuggestCheckBox.isChecked()
        self.suggestForBangla = state
        with open('.//Res//SuggestBangla.txt', "w") as UANSI:
            UANSI.write(str(state))
    def englishSuggest(self, state):                                                   
        state = self.settingsGUIClass.EnglishSuggestCheckBox.isChecked()
        self.suggestForEnglish = state
        with open('.//Res//SuggestEnglish.txt', "w") as UANSI:
            UANSI.write(str(state))
    def emojiSuggest(self):
        state = self.settingsGUIClass.SuggestEmojiesCheckBox.isChecked()
        self.ownSettings.setValue("suggestEmojies", state)  
        global suggestEmoji
        suggestEmoji = state
    def DontShowFunc(self):
        print("I am here")
        pass
    def setListPos(self, posX, posY):
        self.listClass.move(posX, posY)
    def UpdateLists(self, path):
        try:
            with io.open(path, "r", encoding="utf-8") as wordTxt:
                STR = wordTxt.read()
            if path == banglaDictionaryPath:
                global wordsList
                wordsList = STR.split("|")
            if path == englaDictionaryPath:
                global englaList
                englaList = STR.split("|")    
            if path == englaDictionaryPath:
                global EnglishwordsList
                with io.open(englishDictionaryPath, "r", encoding="utf-8") as wordTxt:
                    EnglishWordsSTR = wordTxt.read()
                EnglishwordsList = EnglishWordsSTR.split("|")
            if path == AbbreviationsPath:
                self.loadAbbribiations()  

        except Exception as e:
            self.showError(str(traceback.format_exc()))    
    def open_menu(self, position):
        global currentWrdOutOfDic 
        x, y = pyautogui.position()
        self.index = self.listClass.listWidget.indexAt(position)
        
        self.listClass.listWidget.setCurrentIndex(self.index)

        indx = self.listClass.listWidget.currentRow()
        # print(indx)
        if self.index.isValid():
            
            self.contextClass.listWidget.clear()
            self.contextClass.listWidget.addItem("Copy") 
            if indx == 0 and currentWrdOutOfDic == True:
                self.contextClass.listWidget.addItem("Save") 
            elif indx == 0 and currentWrdOutOfDic == False:
                pass
            elif indx > 0 and currentWrdOutOfDic == False:     
                self.contextClass.listWidget.addItem("Edit")
            elif indx > 0 and currentWrdOutOfDic == True:     
                self.contextClass.listWidget.addItem("Edit")    
            self.contextClass.show()
            self.contextClass.setGeometry(x, y, 100, 100)
    def ContextMenuClicked(self, item):
        c_i = self.listClass.listWidget.currentItem()

        menu_tag = item.text()
        wrd = c_i.text()
        # print(menu_tag)
        if menu_tag == "Copy":
            pc.copy(wrd) 
        if menu_tag == "Edit":
            # if self.wordManagerClass.stufLoaded == False:
            #     self.wordManagerClass.loadStuff() excellent 
            try:
                if wrd[0] in englishAlphabets:
                    if self.wordManagerClass.englishWordsLoaded == False:
                        self.wordManagerClass.loadCompleteEnglishWordList()
                    # ===========
                    
                    # self.matching_items = self.wordManagerClass.EnglishTableWidget.findItems(wrd, Qt.MatchExactly) 
                    # if not self.matching_items:

                    self.wordManagerClass.tabWidget.setCurrentIndex(2)
                else:
                    if self.wordManagerClass.banglaWordsLoaded == False:
                        self.wordManagerClass.loadCompleteBanglaWordList()
                    self.wordManagerClass.tabWidget.setCurrentIndex(0)
                
                self.wordManagerClass.search2(wrd)
                self.showActive(self.wordManagerClass)
            except Exception as e:
                print(traceback.format_exc())    
        if menu_tag == "Save":
            if self.current_language == "English":
                pureWord = True
                for i in range(len(wrd)):
                    if wrd[i] not in englishAlphabets:
                        pureWord = False
                if pureWord:
                    EnglishwordsList.append(wrd)
                    with io.open(englishDictionaryPath, "a", encoding="utf-8") as wordTxt:
                        wordTxt.write(f"|{wrd}")
                    if self.wordManagerClass.englishWordsLoaded:
                        
                        self.wordManagerClass.itemChangedByUndoFunc = True
                        r_pos = self.wordManagerClass.EnglishTableWidget.rowCount()
                        self.wordManagerClass.EnglishTableWidget.insertRow(r_pos)
                        item = QTableWidgetItem(wrd.format(0, 0))
                        self.wordManagerClass.EnglishTableWidget.setItem(r_pos, 0, item)
                        self.wordManagerClass.itemChangedByUndoFunc = False

            # if wrd in EnglishwordsList:
        if menu_tag == "Search Google":
            webbrowser.open('https://www.google.com/search?q='+wrd)
            pass
        self.contextClass.hide() 
    def sfx(self):
        if self.oskClass.SFXcheckBox.isChecked() == True:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            pass      
    def predictionValueChanged(self, val):
        self.MainSettings.setValue("NumberOfPrediction", val)
    def BanglishCheckBoxStateChanged(self):
        if self.oskClass.BanglishCheckBox.isChecked() == True:
            self.oskClass.pushButton_52.setText("???????????????")
        else:
            self.oskClass.pushButton_52.setText("English")
        self.initialize()  
    def showAudioReactor(self, state):
        self.MainSettings.setValue("ShowAudioReactor", (state))  
    def autoCloseBra(self, state):
        self.MainSettings.setValue("AutoCloseBrackets", (state))  
        self.AutoCloseBra = state
    def useAbries(self, state):
        state = self.settingsGUIClass.UseAbrisCheckBox.isChecked()
        self.ownSettings.setValue("UseAbries", (state))  
    def AutoCompleate(self, theWord):
        try:
            global wordSofar
            global ansi_wordSOFar
            if self.listClass.ACcheckBox.isChecked():
                
                self.listener.stop() 
                if self.Unicode_.isChecked() == True:    
                    times_to_tap_backspace, restOfWord = self.smertCompletor(wordSofar, theWord) 
                if self.Ansi_.isChecked() == True:
                    times_to_tap_backspace, restOfWord = self.smertCompletor(ansi_wordSOFar, theWord) 
                
                # print(f"times_to_tap_backspace: {times_to_tap_backspace}, restOfWord: {restOfWord}")
                
                for i in range(times_to_tap_backspace):
                    kb.tap(Key.backspace)
                kb.type(restOfWord)
                self.autoCompletedWord = theWord
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                

                # print(theWord)
            pass
        except Exception:
            pass
    def smertCompletor(self, word_soFar, the_word):
        try:    
            i = 0
            same_index = 0
            for x in range(len(the_word)):
                try:
                    if (the_word[i]).lower() == (word_soFar[i]).lower():
                        same_index = i
                        pass
                    else:
                        break
                    i += 1
                except Exception:
                    same_index = i  
            # if len(word_soFar) <= len(the_word) and self.current_language == "Bangla":
            return_slot = len(word_soFar[same_index:]), the_word[same_index:]
            # else:    
            #     return_slot = len(word_soFar[same_index+1:]), the_word[same_index+1:]

            return return_slot
        except Exception as e:
            print(traceback.format_exc())
            print(f"word_soFar: {word_soFar}, the_word: {the_word}") 
    def WordClickedMiddleFunc(self, item):
        # print(item.text())
        # self.WordClicked()
        global wordSofar
        selectedText = item.text()

        self.listener.stop()
        
        if selectedText in emoji_list:
            sendClip(selectedText)
            initGlobal()
            self.listClass.showHideFunc("hide") 
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
            self.listener.start() 
            return

        if self.Unicode_.isChecked() == True: 
            if selectedText[:len(wordSofar)] == wordSofar:  
                kb.type(selectedText[len(wordSofar):])
            
            else:
                # print(wordSofar)
                # print(selectedText)
                times_to_tap_backspace, restOfWord = self.smertCompletor(wordSofar, selectedText) 
                # print(f"times_to_tap_backspace: {times_to_tap_backspace}")
                # print(f"restOfWord: {restOfWord}")
                for i in range(times_to_tap_backspace):
                    kb.tap(Key.backspace)
                kb.type(restOfWord)
        if self.Ansi_.isChecked():
            ansi_wordSofar = convert(wordSofar)
            if convert(selectedText[:len(wordSofar)]) == ansi_wordSofar:  
                kb.type(convert(selectedText[len(wordSofar):]))
            else:
                times_to_tap_backspace, restOfWord = self.smertCompletor(ansi_wordSofar, convert(selectedText))   
                for i in range(times_to_tap_backspace):
                    kb.tap(Key.backspace)
                kb.type(restOfWord)
        
        
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        self.listener.start() 

        initGlobal()
        self.listClass.showHideFunc("hide") 
    def WordClicked(self, item):    # this function is called when u select a word using keyboard
        global completorTraegered
        global wordSofar
        global CurrentWord
        global emoji_list
        # ==========
        # if self.Ansi_.isChecked() == True:
        
        try:
            wordSelected = item   # this item is a string

            if wordSelected in emoji_list:
                self.listener.stop()
                sendClip(wordSelected)
                initGlobal()
                self.listClass.showHideFunc("hide")
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                return

            if len(wordSofar) == 0 and len(item) > 1:
                c_wrd = CurrentWord    # this means current word is written by the OSk 
            else:
                c_wrd = wordSofar   # current word written by keyboard 
        
            if self.Ansi_.isChecked() and self.current_language == "Bangla":
                self.listener.stop() 
                
                ansi_wordSofar = convert(wordSofar)
                if convert(wordSelected[:len(wordSofar)]) == ansi_wordSofar:  
                    kb.type(convert(wordSelected[len(wordSofar):]))
                else:
                    times_to_tap_backspace, restOfWord = self.smertCompletor(ansi_wordSofar, convert(wordSelected))   
                    for i in range(times_to_tap_backspace):
                        kb.tap(Key.backspace)
                    kb.type(restOfWord)

                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start()  
                initGlobal()
                self.listClass.showHideFunc("hide") 
                return

            if self.autoCompletedWord != "" and wordSofar == item: 
                self.listener.stop() 
                for i in range(len(self.autoCompletedWord)):
                    kb.tap(Key.backspace) 
                completorTraegered = True
                kb.type(wordSelected)
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                completorTraegered = False 
                
            
            if wordSelected[:len(c_wrd)] == c_wrd.lower():
                self.listener.stop()
                if self.oskClass.capsLocked == True:
                    restOfWord = (wordSelected[len(c_wrd):]).upper()
                else:
                    restOfWord = wordSelected[len(c_wrd):]

                kb.type(restOfWord)  
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start()            
            elif len(c_wrd) == 1:
                self.listener.stop()
                kb.tap(Key.backspace)
                kb.type(wordSelected)
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                wordSofar = wordSelected
            else:
                self.listener.stop() 
                
                times_to_tap_backspace, restOfWord = self.smertCompletor(c_wrd, wordSelected) 
                for i in range(times_to_tap_backspace):
                    kb.tap(Key.backspace)
                completorTraegered = True
                kb.type(restOfWord)
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                completorTraegered = False 
            initGlobal()
            # self.listClass.showHideFunc("hide")  
        except Exception:
            pass   
    def getRecomendedWords(self, words):
        global wordSofar
        if wordSofar in ["", " "]:
            return
        if self.listClass.isHidden() == False:
            self.listClass.populateWords(words)
        if self.oskClass.isHidden() == False:
            self.oskClass.populateWords(words[2:])
    def loadAbbribiations(self):
        try:
            kb2.unhook_all()
            with io.open('.//Res//Abbreviations.txt', "r", encoding="utf-8") as RKS:
                abriStr = RKS.read()
            abris = abriStr.split("\n")

            self.abbries_dic = {}
            
            for ab in abris[:]:
                if ab == "":
                    return
                parts = ab.split("::")
                if len(parts) == 0:
                    return
                # kb2.add_abbreviation(parts[0], parts[1]) 
                
                self.abbries_dic[parts[0]] = parts[1]
                # print(self.abbries_dic)
        except Exception as e:
            self.showError(e)
        if self.current_language != "English":
            self.blockKeys()
    def blockKeys(self):
        if self.current_language == "Bangla":
            self.listener.stop()
            for i in self.keysToBlock:
                kb2.block_key(i)
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
            self.listener.start()
            self.listClass.hide()
            # self.initialize()
    def trim(self, l):
        global wordSofar
        self.listener.stop()
        wordSofar = wordSofar[:-l]
        if self.Unicode_.isChecked() == True:
            for i in range(l):  
                kb.tap(Key.backspace)
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        self.listener.start()
    
    def on_osk_press(self, key):
    
        # print(self.listener.running)
        global wordSofar
        if key == "key.end":
            kb.tap(Key.end)
            self.oskClass.initState()
            self.initialize()
            return
        if key == "key.home":
            kb.tap(Key.home)
            self.oskClass.initState()
            self.initialize()
            return
        if key == "key.delete":
            kb.tap(Key.delete)
            self.oskClass.initState()
            self.initialize()
            return

        if key == "key.backspace":
            self.listener.stop()
            kb.tap(Key.backspace)
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
            self.listener.start()
            global wordSofar
            global CurrentWord
            if CurrentWord != "": 
                try:
                    CurrentWord = CurrentWord[:-1]
                except Exception:
                    CurrentWord = "" 
                    # self.oskClass.cleanRecomendations()
                    self.initialize()

                self.oskClass.initState()
            elif wordSofar != "":
                try:
                    wordSofar = wordSofar[:-1]
                except Exception:
                    wordSofar = "" 
                    self.oskClass.cleanRecomendations()
            return
        if self.oskClass.BanglishCheckBox.isChecked() == False or any([self.oskClass.ctrlState, self.oskClass.altState, self.oskClass.winState]):
            self.listener.stop()
            if any([self.oskClass.ctrlState, self.oskClass.altState, self.oskClass.winState]):
                kb.tap(key)  
            else:
                kb.type(key)
                if key in englishLatters:    
                    wordSofar += key
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
            self.listener.start()
            self.oskClass.initState()    
            return   
        if self.oskClass.BanglishCheckBox.isChecked() == True:
            if key in englishLatters:   
                self.listener.stop()
                # print("I am still here")
                global completorTraegered
                completorTraegered = True
                self.convertTobangla(key) 
                completorTraegered = False

                # self.listClass.showHideFunc("hide")
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
                # self.listClass.showHideFunc("hide") 
            else:
                self.listener.stop()
                kb.type(key)      
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
            self.oskClass.initState()   
        # self.on_press(key)
            # self.listClass.showHideFunc("hide")
        self.sfx()

    def triggerAbbribiation(self, key):
        # self.listener.stop()
        for i in range(len(key)+1):  
            kb.tap(Key.backspace)
        
        # pyautogui.write(self.abbries_dic[key]) 
        sendClip(self.abbries_dic[key])
        
        # self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        # self.listener.start()
    def on_press_2(self, event):
        pass
    def selectNextWord(self):
        if self.listClass.listWidget.currentRow() == -1 or self.listClass.listWidget.currentRow() == self.listClass.listWidget.count()-1:
            self.listClass.listWidget.setCurrentRow(1)
        else:
            self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.currentRow()+1) 
    
    def on_press(self, key):
        # print(key)
        global wordSofar 
        global englishWordSofar
        global previous_word
        global formar_previous_word
        global ansi_wordSOFar
        global sentencece_sofar
        global using_functionKeys

        try:
            if self.AutoCloseBra:
                qote = (str(key)).replace("'", "")
                if qote in self.qoteDic:
                    kb.release(Key.shift)
                    kb.type(self.qoteDic[qote])
                    kb.tap(Key.left)
                    self.initialize()
                    return

            # ==================================== !!! 
            stringKey = (str(key)).replace("'","")
            
            if str(key) == "Key.space" : # or (str(key)).replace("'", "") in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "`", "~"]
                if wordSofar in self.abbries_dic and self.settingsGUIClass.UseAbrisCheckBox.isChecked() == True:
                    self.triggerAbbribiation(wordSofar)
                sentencece_sofar += f"{wordSofar} "
                self.initialize()
                self.initThread_signal.emit("init")

                # print(sentencece_sofar)
                return
            
            if str(key) == "Key.backspace":
                if wordSofar != "":    
                    if len(wordSofar) > 1:   
                        wordSofar = wordSofar[:-1]
                        try:
                            ansi_wordSOFar = ansi_wordSOFar[:-1]
                        except Exception as e:
                            pass    
                        englishWordSofar = englishWordSofar[:-1]
                        # self.word_signal.emit(wordSofar, englishWordSofar, "bangla")
                    else:
                        self.initialize() 
                     
            if stringKey in ["Key.f1","Key.f2","Key.f3","Key.f4","Key.f5","Key.f6","Key.f7","Key.f8","Key.f9","Key.f10","Key.f11","Key.f12"] and  using_functionKeys == True and self.listClass.isHidden() == False:
                try:
                    fun_no = stringKey[5:]
                    item = self.listClass.listWidget.item(int(fun_no)-1)

                    self.WordClicked(item.text())
                    self.listClass.showHideFunc("hide")
                except Exception as e:
                    print(e)    
                pass

            if str(key) in ["Key.down", "Key.up", "Key.enter", "Key.tab"]:
                if self.listClass.isHidden() == False:
                    
                    if str(key) in ["Key.down", "Key.tab"]:
                        global using_tab
                        global using_arrow
                        if any([using_tab, using_arrow]):
                            try:
                                kb2.block_key(28) # enter key
                            except Exception as e:
                                print(traceback.format_exc()) 

                            if self.listClass.listWidget.currentRow() == -1:
                                current = wordSofar
                            else:
                                item = self.listClass.listWidget.currentItem()
                                current = item.text() 
                        if str(key) == "Key.down" and using_arrow == True:
                            self.selectNextWord()
                        elif str(key) == "Key.tab" and using_tab == True:
                            self.selectNextWord()  
                        else:
                            self.initialize()
                            self.initThread_signal.emit("init") 
                            return
                        
                        if self.settingsGUIClass.SelectionRadioButton.isChecked():
                            item = self.listClass.listWidget.currentItem()
                            self.tempoComplition(current, item.text())
                            return
                            
                    if str(key) in ["Key.up"] and using_arrow == True:
                        if self.listClass.listWidget.currentRow() == 1:
                            self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.count()-1)
                        else:    
                            self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.currentRow()-1)

                        if self.settingsGUIClass.SelectionRadioButton.isChecked():
                            item = self.listClass.listWidget.currentItem()
                            self.tempoComplition(current, item.text())
                            return
                        
                        # if str(key) == "Key.up" and self.settingsGUIClass.ArrowCheckBox.isChecked():
                        #     self.selectNextWord()
                        # if str(key) == "Key.tab" and self.settingsGUIClass.TabCheckBox.isChecked():
                        #     self.selectNextWord()
                    if str(key) == "Key.enter":
                        if self.listClass.listWidget.currentRow() != -1 and self.settingsGUIClass.EnterToSelectRadioButton.isChecked() == True:    
                            item = self.listClass.listWidget.currentItem()

                            if item.text() in emoji_list:
                                self.listener.stop()
                                sendClip(item.text())
                                initGlobal()
                                self.listClass.showHideFunc("hide") 
                                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                                self.listener.start() 
                                return
                            self.WordClicked(item.text())
                            self.listClass.showHideFunc("hide")
                        else:
                            sentencece_sofar = ""
                            self.initialize()
                            self.initThread_signal.emit("init")
                            
                else:
                    # print("in else")
                    # self.listener.stop()
                    # kb.tap(key)
                    # self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                    # self.listener.start() 
                    self.initialize()
                    self.initThread_signal.emit("init")
                    return

            if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"] and self.keysBlocked == True: 
                if self.current_language != "English":    
                    kb2.unhook_all()
                    self.keysBlocked = False
                self.HotKeyPressed = True    
                self.old_initialize()
                return
            
            if self.current_language == "English":
                if self.HotKeyPressed == True and stringKey in englishNumbers: 
                    self.initialize()
                    self.HotKeyPressed = False
                    return

                if stringKey in englishNumbers:
                    # if wordSofar != "":
                    #     if wordSofar[0] not in englishNumbers:
                    #         self.initialize()
                    wordSofar += stringKey
                      
                if stringKey in englishAlphabets:    
                    wordSofar += stringKey
                    englishWordSofar = wordSofar
                if stringKey in special_characters_of_keyboard:
                    wordSofar += stringKey
                    # print("i am here bro!")
        # ===========================================
            if self.current_language == "Bangla":
                if str(key) == "Key.shift" and self.Unicode_.isChecked() == True: # and self.shiftKeyBlocked == False
                    # for i in self.keysToUnlock:
                    #     try:
                    #         kb2.unblock_key(i)
                    #     except Exception:
                    #         pass
                    # kb2.unblock_key(2)
                    kb2.unhook_all()
                    for i in self.keysToBlockWhenShiftKeyIsPressed:
                        try: 
                            kb2.block_key(i)
                        except Exception:
                            pass
                    self.shiftKeyBlocked = True
                if str(key) == "Key.shift" and self.Unicode_.isChecked() == False:
                    return 
                    
                if self.keysBlocked == False:
                    return        
                if str(key) == "'.'":
                    kb.type("???")
                    self.initialize()
                    return
                
                if completorTraegered == True:
                    return

                if self.Unicode_.isChecked() == True:    
                    # print("i am here!")
                    if self.Banglish_layout.isChecked() == True:    
                        self.convertTobangla(key)
                    if self.Bijoy_layout.isChecked() == True: 
                        self.convertToBijoy(stringKey)
                if self.Ansi_.isChecked() == True:
                    if stringKey not in englishLatters and stringKey not in ["$","^","&"]:
                        return
                    
                    if stringKey in self.numDic:
                        self.listener.stop()
                        kb.type(convert(self.numDic[stringKey]))
                        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                        self.listener.start()
                        if wordSofar != "":
                            if wordSofar[0] not in banglaNumbs:
                                self.initialize()
                        wordSofar += self.numDic[stringKey]
                        
                    if self.Banglish_layout.isChecked() == True and stringKey not in self.numDic: 
                        try:
                            bangla_wordSoFar_unicode = self.convertTobangla(key) 
                            ansi_Bangla =  convert(bangla_wordSoFar_unicode)  
                            self.listener.stop()
                            if ansi_wordSOFar != "":    
                                if ansi_Bangla[:len(ansi_wordSOFar)] == ansi_wordSOFar:
                                    restOfWord = ansi_Bangla[len(ansi_wordSOFar):]
                                else:
                                    times_to_tap_backspace, restOfWord = self.smertCompletor(ansi_wordSOFar, ansi_Bangla)   
                                    for i in range(times_to_tap_backspace):
                                        kb.tap(Key.backspace)
                            else:
                                restOfWord = ansi_Bangla
                            kb2.write(restOfWord)
                            ansi_wordSOFar = ansi_Bangla
                            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                            self.listener.start()
                        except Exception as e:
                            print(e)
                    if self.Bijoy_layout.isChecked() == True and stringKey not in self.numDic:    # < ------------------------ 
                        if stringKey in ['d', 'c', 'C']:
                            bijoy_unicode = ""
                            if stringKey == 'd':
                                bijoy_ANSI = "w"
                            if stringKey == 'c':
                                bijoy_ANSI = "???" 
                            if stringKey == 'C':
                                bijoy_ANSI = "???"   
                                    
                        else:
                            bijoy_unicode = self.bijoy_Uni_Map[stringKey] # just a character 
                            bijoy_ANSI = convert(bijoy_unicode) # just a character  in bijoy
                    
                        self.listener.stop()
                        if len(ansi_wordSOFar) > 0:
                            if ansi_wordSOFar[-1] == "&":
                                if len(wordSofar) > 1:
                                    if wordSofar[-2] in self.karList:
                                        if len(wordSofar) > 2:     
                                            jukto_uni = wordSofar[-3]+wordSofar[-1]+bijoy_unicode
                                            bijoy_ANSI = convert(jukto_uni)
                                            for i in range(2):  
                                                kb.tap(Key.backspace)
                                    else:
                                        jukto_uni = wordSofar[-2:]+bijoy_unicode
                                        bijoy_ANSI = convert(jukto_uni)
                                        for i in range(2):  
                                            kb.tap(Key.backspace)

                        if len(wordSofar) > 0:
                            if stringKey in ["f", 'X'] and wordSofar[-1] == "???":
                                wordSofar =  wordSofar[:-1]
                                if stringKey == "f":
                                    bijoy_unicode = "???"
                                if stringKey == "X":
                                    bijoy_unicode = "???"

                        
                        kb2.write(bijoy_ANSI)

                        wordSofar += str(bijoy_unicode+self.reserved)
                        ansi_wordSOFar += bijoy_ANSI
                        # print(wordSofar)
                        self.formar_previous_formar_previous_word = self.previous_formar_previous_word
                        self.previous_formar_previous_word = formar_previous_word
                        formar_previous_word = previous_word
                        previous_word = bijoy_unicode
                        englishWordSofar += bijoy_unicode


                        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                        self.listener.start()

                        if stringKey in ['d', 'c', 'C']:
                            self.reserved = self.bijoy_Uni_Map[stringKey] 
                        else:
                            self.reserved = ""    
                
            
            if self.lastActiveWindow in [self.Doc_pad.windowTitle()]:
                self.Doc_pad.activateWindow()
            if self.lastActiveWindow in [self.wordManagerClass.windowTitle()]:
                self.wordManagerClass.activateWindow()    
            if self.lastActiveWindow in [self.converter_gui.windowTitle()]:
                self.converter_gui.activateWindow()  
            
            if self.settingsGUIClass.banglaSuggestCheckBox.isChecked() == False and self.current_language == "Bangla":
                return
            if self.settingsGUIClass.EnglishSuggestCheckBox.isChecked() == False and self.current_language == "English":
                return      
            
            
            if stringKey not in englishLatters and stringKey not in special_characters_of_keyboard:
                return
            
            
            if GetWindowText(GetForegroundWindow()) in ["Word manager"]:
                # print("i am here!")
                return  
            
            self.word_signal.emit(wordSofar, englishWordSofar, "bangla")

        except Exception as e:
            # print(e)
            print(traceback.format_exc())
            # self.showError(traceback.format_exc())
        pass
    def on_click(self, x, y, button, pressed):
        if GetWindowText(WindowFromPoint(GetCursorPos())) not in [self.listClass.windowTitle(), self.oskClass.windowTitle(), self.contextClass.windowTitle()]:
            self.lastActiveWindow = GetWindowText(WindowFromPoint(GetCursorPos()))
            self.initialize()
            global sentencece_sofar
            global currentWrdOutOfDic 
            currentWrdOutOfDic = False
            sentencece_sofar = ""

    def on_release(self, key):
        global block_up_down
        if key == keyboard.Key.up or key == keyboard.Key.down:
            if block_up_down:
                return False

        if self.current_language == "English":
            if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"]: # and keysBlocked == False
                self.HotKeyPressed = False
            return
        # print("I am the bitch u r looking for")
        if str(key) == "Key.shift":
            for i in self.keysToUnlock:
                kb2.block_key(i)
            self.shiftKeyBlocked = False    

        if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"]: # and keysBlocked == False
            for i in self.keysToBlock:    
                kb2.block_key(i)
            self.keysBlocked = True 
            
            # if self.listClass.isHidden() == False:
            #     for i in [28, 72, 80]:
            #         kb2.block_key(i)
    
    def convertToBijoy(self, key):
        if key not in englishAlphabets:
            return
        global wordSofar 
        global englishWordSofar
        global previous_word
        global formar_previous_word
        
        
        if key in ['d', 'c', 'C']:
            self.reserved = self.bijoy_Uni_Map[key]
            return
   

        # if len(wordSofar)> 0:
        #     print(key)
        #     print(wordSofar[-1])

        if self.reserved != "":
            toSendKey = f"{self.bijoy_Uni_Map[key]}{self.reserved}"
        elif key in ["f", 'X'] and wordSofar[-1] == "???":
            self.trim(1)

            if key == "f":
                toSendKey = "???"
            if key == "X":
                toSendKey = "???"
        else:
            toSendKey = self.bijoy_Uni_Map[key]
        
        self.listener.stop()
        kb.type(toSendKey)
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        self.listener.start()

        if self.reserved != "":
            self.reserved = ""

        wordSofar += str(toSendKey)
        self.formar_previous_formar_previous_word = self.previous_formar_previous_word
        self.previous_formar_previous_word = formar_previous_word
        formar_previous_word = previous_word
        previous_word = toSendKey
        englishWordSofar += toSendKey
        pass
    def convertTobangla(self, key):
        global wordSofar 
        global englishWordSofar
        global previous_word
        global formar_previous_word
        bnglaKey = ""
        stringKey = (str(key)).replace("'", "")

        # takes english characters one by one as banglish word latters and types bangla
        if stringKey in self.numDic:
            kb.type(self.numDic[stringKey])
            
            if wordSofar != "":
                if wordSofar[0] not in banglaNumbs:
                    self.initialize()
            wordSofar += self.numDic[stringKey]
            # self.initialize()   
            return
        

        if stringKey == '^':
            bnglaKey = "???"
        if stringKey == ':':
            bnglaKey = "???"
        if stringKey == '$':
            bnglaKey = "???"
        if stringKey == "a":
            if wordSofar == "":
                bnglaKey = "???"
            elif previous_word == "a":
                bnglaKey = "??????"
            # elif previous_word == formar_previous_word and previous_word != "" and previous_word in ["c", ]:
            #     self.trim(1)
            #     bnglaKey = "?????????"
            else:
                if wordSofar[-1] == "???":
                    self.trim(1)
                    bnglaKey = "??????"
                else:
                    bnglaKey = "???"

            if len(wordSofar) > 0:
                if wordSofar[-1] in self.karList:
                    bnglaKey = "???"         
        if stringKey == "A":
            bnglaKey = "???"
        if stringKey == "b":
            if previous_word in ["b","r"] and self.checkIndex(-2) != "???":
                bnglaKey= "??????"
            else:
                bnglaKey= "???"
        if stringKey == "c":
            if previous_word in ["c","h"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            elif previous_word in ["n","G"]:
                bnglaKey = "?????????"
                self.trim(1)
            else:
                bnglaKey= "???"  
        if stringKey == "d":
            if previous_word in ["n","b", "d", "l", "k"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"    
            else:
                bnglaKey = "???"    
        if stringKey == "D":
            if previous_word in ["n","D", "l"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"    
            else:
                bnglaKey = "???"
        if stringKey == "e":
            if wordSofar == "":
                bnglaKey = "???"
            elif previous_word == 't' and formar_previous_word == 'n':
                bnglaKey = "??????"
                self.trim(2)
            else:
                bnglaKey = "???"
        if stringKey == "E":
            if wordSofar == "":
                bnglaKey = "???"
            else:
                bnglaKey = "???"
        if stringKey == "f" or stringKey == "F":
            bnglaKey = "???"
        if stringKey == "g":
            if previous_word == "n" or previous_word == "N":
                if previous_word == "n": 
                    bnglaKey= "???"
                if previous_word == "N": 
                    bnglaKey= "???"
                self.trim(1)
            elif previous_word == "r" and self.checkIndex(-2) != "???": 
                bnglaKey= "??????"
            elif previous_word == "g":
                bnglaKey= "?????????" 
                self.trim(1)
            else: 
                bnglaKey= "???" 
        if stringKey == "G":
            if previous_word == "N":
                bnglaKey= "???" 
                self.trim(1) 
            else:
                bnglaKey= "???" 
        if stringKey == "h":
            if previous_word == "K":
                bnglaKey = "??????"
            elif previous_word == "c":
                bnglaKey= "???" 
                self.trim(1)
            elif previous_word == "j":
                bnglaKey = "???" 
                self.trim(1) 
            elif previous_word == "k": 
                if formar_previous_word == "k":
                    bnglaKey = "???"     
                else:
                    bnglaKey = "???"
                    self.trim(1)    
            elif previous_word == "p":
                bnglaKey = "???"
                self.trim(1)  
            elif previous_word == "g":
                bnglaKey = "???"
                self.trim(1)  
            elif previous_word == "d":
                if formar_previous_word == "g":
                    bnglaKey = "??????"
                    self.trim(1)
                else:
                    bnglaKey = "???"
                self.trim(1)  
            elif previous_word == "D":
                bnglaKey = "???"
                self.trim(1)
            elif previous_word == "b":
                if formar_previous_word == "d":
                    bnglaKey = "??????"
                else:
                    bnglaKey = "???"
                self.trim(1)
            elif previous_word == "R":
                bnglaKey = "???"
                self.trim(1) 
            elif previous_word == "s":
                bnglaKey = "???"
                self.trim(1)
            elif previous_word == "S":
                self.trim(1)
                bnglaKey = "???"
                
            elif previous_word == "t":
                bnglaKey = "???"
                self.trim(1)  
            elif previous_word == "T":
                bnglaKey = "???"
                self.trim(1)  
            elif previous_word == "v":
                pass
            else:
                bnglaKey = "???" 
        if stringKey == "H":
            if previous_word == "K":
                bnglaKey = "??????"
            elif previous_word == "T":
                bnglaKey = "???"
                self.trim(1)
        if stringKey == "i":
            if wordSofar == "" or wordSofar[-1] in self.karList or wordSofar[-1] in ["???","???","???", "???", "???","???","???","???", "???", "???", "???"]:
                bnglaKey= "???"
            elif previous_word == "r" and formar_previous_word == "r":
                bnglaKey= "???"
                self.trim(3)
            elif previous_word == "o" or previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey= "???"
                    self.trim(1)
                else:
                    bnglaKey= "???"
            else:
                bnglaKey= "???"
        if stringKey == "I":
            if previous_word == "o" or previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey= "???"
                    self.trim(1)
                else:
                    bnglaKey= "???"
            elif wordSofar == "" or wordSofar[-1] in self.karList:
                bnglaKey = "???"    
            else:
                bnglaKey = "???"
        if stringKey == "j":
            if previous_word == "n":
                bnglaKey= "?????????"
                self.trim(1)
            elif previous_word in ["j", "J"] and self.checkIndex(-2) != "???":
                bnglaKey= "??????" 
            else:
                bnglaKey= "???"
        if stringKey == "J":
            bnglaKey= "???"    
        if stringKey == "k":
            if previous_word in ["k", "K", "l", "s", "r"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            elif previous_word == "h" and formar_previous_word == "s":
                bnglaKey = "?????????"
                self.trim(1)  
            elif previous_word == "n":
                bnglaKey = "?????????"
                self.trim(1)      
            elif previous_word == "g" and formar_previous_word == "N":
                bnglaKey = "??????"
            else:
                bnglaKey = "???"
        if stringKey == "K":
            bnglaKey = "???"
        if stringKey == "l":
            if previous_word == "l" and self.checkIndex(-2) != "???":
                bnglaKey= "??????"
            else:
                bnglaKey= "???"         
        if stringKey == "m":
            if previous_word == "h" and formar_previous_word not in ["s", "S", "k", "t", "T", "g", "G", "p", "P", "d", "D", "c", "C", "b", "B"]:
                bnglaKey = "?????????"
                self.trim(1) 
            elif previous_word in ["d", "l", "n", "s", "t", "g", "m", "h"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????" 
            else:
                bnglaKey = "???" 
        if stringKey == "M":
            bnglaKey = "??????" 
        if stringKey == "n":
            # print(previous_word)
            if previous_word in ["n", "p", "t", "g", "h", "m", "s", "r"] and self.checkIndex(-2) != "???":
                bnglaKey= "??????"
            else:
                bnglaKey= "???"      
        if stringKey == "N":
            if previous_word == "r" and self.checkIndex(-2) != "???":
                bnglaKey = "??????" 
            else:
                bnglaKey = "???" 
        if stringKey == "o":
            if previous_word == formar_previous_word != "": 
                if previous_word == "g":
                    bnglaKey = "??????"
                else:
                    self.trim(1) 
                    bnglaKey = "???"   
            elif wordSofar == "":
                bnglaKey = "???"
            elif previous_word == "g" and formar_previous_word == "n":
                bnglaKey = "?????????"
                self.trim(1)  
            # elif previous_word == "h" and formar_previous_word == "r":   
            # elif previous_word == formar_previous_word and 
            elif previous_word in ["p", "s", "t", "T", "c", "d", "z", "m", "O", "k", "b", "n", "r", "g", "j", "l", "h", "y", "S"]: 
                previous_word = "o"
                pass 
            else:
                if wordSofar[-1] in self.karList:    
                    bnglaKey = "???"
                else:    
                    bnglaKey = "???"
        if stringKey == "O":
            if wordSofar == "":
                bnglaKey = "???"
            else:
                bnglaKey = "???"
        if stringKey in ["p", "P"] :
            if previous_word == "s" and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            else:
                bnglaKey = "???"
        if stringKey in ["q", "Q"]:
            bnglaKey = "???"
        if stringKey == "r":
            if previous_word in ["t","b","k","f","g","h","j","c","d","n","p","s","v","T","D","z","F", "m"]:
                bnglaKey = "??????" 
            else:
                bnglaKey = "???"
        if stringKey == "R":
            if wordSofar == "":
                bnglaKey = "???" 
            else:
                bnglaKey = "???"  
        if stringKey == "s":
            if previous_word in ["r", "n", "k", "n"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            elif previous_word == "H":
                bnglaKey = "???"
                self.trim(1)
            else:
                bnglaKey = "???"  
        if stringKey == "S":
            bnglaKey = "???" 
        if stringKey == "t":
            # print(self.checkIndex(-2))
            if previous_word in ["n","t", "p", "r", "s"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            elif previous_word == "k": 
                bnglaKey = "?????????"
                self.trim(1)
            else:
                bnglaKey = "???"
        if stringKey == "T":
            # print(wordSofar)
            if previous_word in ["h", "k","l","n", "p", "s","T"] and formar_previous_word not in ["g"] and self.checkIndex(-2) != "???":
                bnglaKey = "??????"
            else:
                bnglaKey = "???"
        if stringKey == "u":
            
            if previous_word in ["O", "o"]:
                bnglaKey = "???"
                self.trim(1)  
            elif wordSofar == "":
                bnglaKey = "???"  
            else:
                bnglaKey = "???" 

            if len(wordSofar) > 0:
                if wordSofar[-1] in self.karList:
                    bnglaKey = "???"         
        if stringKey == "U":
            if wordSofar == "":
                bnglaKey = "???"
            elif previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey = "???"
                else:
                    bnglaKey = "???"
                self.trim(1) 
            else:
                bnglaKey = "???"

            if len(wordSofar) > 0:
                if wordSofar[-1] in self.karList:
                    bnglaKey = "???"     
        if stringKey in ["v", "V"] : 
            if previous_word in ["m", "d"]:
                bnglaKey = "??????"
            else:
                bnglaKey = "???"
        if stringKey in  ["w", "W"]:
            if wordSofar == "":
                bnglaKey = "???"
            else:
                bnglaKey = "??????"
        if stringKey in  ["y", "Y"]:
                bnglaKey = "???"
        if stringKey == "z":
            if previous_word == "r":
                bnglaKey = "??????"
            else:
                bnglaKey = "???"
        if stringKey == "Z":
            bnglaKey== "??????"  
                 
        if bnglaKey != "" or stringKey == "o":
            
            wordSofar += str(bnglaKey)
            self.formar_previous_formar_previous_word = self.previous_formar_previous_word
            self.previous_formar_previous_word = formar_previous_word
            formar_previous_word = previous_word
            previous_word = stringKey
            englishWordSofar += stringKey

            if self.Ansi_.isChecked() == True:
                return wordSofar
            kb.type(str(bnglaKey))

    def checkIndex(self, indx):
        try:
            global wordSofar
            return wordSofar[indx]
        except Exception:
            return NONE    
    def initialize(self):
        global wordSofar
        global englishWordSofar
        global previous_word
        global formar_previous_word
        global ruledOut 
        global CurrentWord
        global ansi_wordSOFar
        global word_submitted_for_similarity
        global word_submitted_lang
        global newCharacterIsPressed
        
        # saving new word +++++++++++++++++++++++++++

        # if len(wordSofar) > 2 and wordSofar not in englishDictionaryPath:
        
        CurrentWord = ""
        self.autoCompletedWord = ""
        previous_word = ""
        wordSofar = ""
        ansi_wordSOFar = ""
        englishWordSofar = ""
        formar_previous_word = ""
        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = "" 
        ruledOut = False 
        self.listClass.initSelf()
        self.reserved = ""
        
        word_submitted_for_similarity = ""
        
        newCharacterIsPressed = False

        self.blockKeys()
        self.oskClass.cleanRecomendations()
        self.contextClass.hide()   
    def old_initialize(self):
        global wordSofar
        global englishWordSofar
        global previous_word
        global formar_previous_word
        global ruledOut 
        global CurrentWord

        global word_submitted_lang
        global newCharacterIsPressed
        global word_submitted_for_similarity

        CurrentWord = ""
        self.autoCompletedWord = ""
        previous_word = ""
        wordSofar = ""
        englishWordSofar = ""
        formar_previous_word = ""
        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = "" 

        word_submitted_for_similarity = ""
        
        newCharacterIsPressed = False

        ruledOut = False 
        self.listClass.initSelf()
        self.oskClass.cleanRecomendations()
        self.contextClass.hide() 
    def rb1Clicked(self):
        self.WordClicked(str(self.oskClass.RB1.text())) 
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb2Clicked(self):
        self.WordClicked(str(self.oskClass.RB2.text()))
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb3Clicked(self):
        self.WordClicked(str(self.oskClass.RB3.text()))
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb4Clicked(self):
        self.WordClicked(str(self.oskClass.RB4.text()))  
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb5Clicked(self):
        self.WordClicked(str(self.oskClass.RB5.text()))
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space) 
            self.initialize()   
    def rb6Clicked(self):
        self.WordClicked(str(self.oskClass.RB6.text())) 
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space) 
            self.initialize()
    def rb7Clicked(self):
        self.WordClicked(str(self.oskClass.RB7.text())) 
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb8Clicked(self):
        self.WordClicked(str(self.oskClass.RB8.text())) 
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space) 
            self.initialize()  
    def rb9Clicked(self):
        self.WordClicked(str(self.oskClass.RB9.text()))
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space)
            self.initialize()
    def rb10Clicked(self):
        self.WordClicked(str(self.oskClass.RB10.text()))
        if self.oskClass.SpaceCheckBox.isChecked():    
            kb.tap(Key.space) 
            self.initialize() 
    def ShowWordManager(self):
        try:
            if self.wordManagerClass.banglaWordsLoaded == False:
                self.wordManagerClass.loadCompleteBanglaWordList()
            self.showActive(self.wordManagerClass)
            # self.wordManagerClass.show()
        except Exception as e:
            self.showError(e)
    def GetCaretPosInWindow(self):
        rect = GetWindowRect(GetForegroundWindow())
        Window_x_pos = rect[0]
        Window_y_pos = rect[1]

        fg_win = GetForegroundWindow()
        fg_thread, fg_process = win32process.GetWindowThreadProcessId(fg_win)
        current_thread = win32api.GetCurrentThreadId()
        win32process.AttachThreadInput(current_thread, fg_thread, True)
        try:    
                caret = GetCaretPos()      
        finally:
                win32process.AttachThreadInput(current_thread, fg_thread, False)     
        caret_x_pos =caret[0]
        caret_y_pos =caret[1]
        return caret_x_pos + Window_x_pos, caret_y_pos # + Window_y_pos      
    def Open_OCR_from_screen(self):
        try:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            self.Ocr_app = ScreenShort.OCR_app()
            self.Ocr_app.forOcr = True
            self.Ocr_app.Show_self() 
        except Exception as e:
            self.showError(e) 
        pass
    def Open_OCR(self):
        try:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            # self.Ocr_app = OCR.Ui_OCR()
            # self.Ocr_app.ShowSelf() 
            self.Ocr_app = ScreenShort.OCR_app()
            self.Ocr_app.forOcr = False
            self.Ocr_app.Show_self() 
        except Exception as e:
            self.showError(e) 
    def screenShot(self):
        try:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            self.Ocr_app = ScreenShort.OCR_app()
            self.Ocr_app.forOcr = False
            self.Ocr_app.Show_self() 
        except Exception as e:
            self.showError(e) 
    def Open_OSK(self):
        try:
            try:
                self.oskClass.show()
            except Exception as e:
                self.showError(e)     
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
        except Exception as e:
            self.showError(e)    
        pass
    def Run_startup_fun(self, state):
        try:
            if state:
                creat_shortcut()
                
                self.MainSettings.setValue("runAtStartUp", True)

                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"
                                "font: 12pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Kontho")
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                msg.setText("Next time Nms Kontho will run automatically at system startup.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                try:
                    home = str(Path.home())
                    path = os.path.join(home, "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Kontho.lnk")
                    os.remove(path)
                except Exception as e:
                    print(e) 
                with open('.//Res//Run_at_startup.txt', "w") as RKS:
                    RKS.write("False")    
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"
                                "font: 12pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Kontho")
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                msg.setText("Next time Nms Kontho won't run at system startup.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()       
            pass
        except Exception as e:
            self.showError(e)
            
    def Open_converter_exe(self):
        try: 
            
            self.converter_gui.show_converter()
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
        except Exception as e:
            self.showError(e)    
    def Open_converter(self):
        try:
            # os.startfile("OnScreen Keyboard.exe")

            oskClass = OSK_UI()
            oskClass.show()
        except Exception as e:
            self.showError(e)      
    def Open_Wave_to_text_generator(self):
        try:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            self.wav_to_text = Mic.Ui_Text_genarator()
            self.wav_to_text.Show_self()
        except Exception as e:
            self.showError(e)     
    def Open_doc_pad(self):
        try:
            self.showActive(self.Doc_pad)
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
        except Exception as e: 
            self.showError(e)       
    def showSettings(self):
        self.showActive(self.settingsGUIClass)
    def showActive(self, obj):
        if obj.isHidden():
            obj.show()
        else:
            obj.activateWindow()        
    def Ansi(self):
        self.Ansi_.setChecked(True)
        self.Unicode_.setChecked(False)
        self.UANSI_pos = True 
    def Unicode(self):    
        self.Ansi_.setChecked(False)
        self.Unicode_.setChecked(True)
        self.UANSI_pos = False 
    def Take_commend(self):
        if self.taking_commend.isChecked() == False:
            # self.taking_commend.setChecked(True) 
            self.taking_cmd = True   
        else:
            # self.taking_commend.setChecked(False) 
            self.taking_cmd = False        
    def Use_punction(self):
        self.impAct0.setChecked(True)
        self.impAct1.setChecked(False)
        with open('.//Res//Use_punction.txt', "w") as USP:
            USP.write('True') 
    def Dont_use_punction(self): 
        self.impAct1.setChecked(True)
        self.impAct0.setChecked(False) 
        with open('.//Res//Use_punction.txt', "w") as USP:
            USP.write('False')   
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
    def Mic_pressed(self):
        
        # self.listener.stop()
        CLT_pos = self.current_language
        if CLT_pos == 'English (US)':
            self.lang = 'en-US'
        if CLT_pos == 'English (UK)':
            self.lang = 'en-GB'
        if CLT_pos == 'Bangla':
            self.lang = 'bn-BD'
        if CLT_pos == 'English':
            self.lang = 'en-IN'
        
        mic_index = self.settingsGUIClass.MicSettings.value('mic_index_in_sr_mic_list')
        mic_name = self.settingsGUIClass.MicSettings.value('SelectedMic')
        mic_energy = self.settingsGUIClass.MicSettings.value('Energy')
        mic_pause = self.settingsGUIClass.MicSettings.value('Pause')
        mic_phrase = self.settingsGUIClass.MicSettings.value('Phrase')
        mic_nonSpeakingDuration = self.settingsGUIClass.MicSettings.value('Non_speaking_daration')

        self.thread = whileThreadClass(self.lang, self.UANSI_pos, self.taking_cmd,mic_index,mic_name,mic_energy,mic_pause,mic_phrase,mic_nonSpeakingDuration, parent=None)
        self.thread.any_signal.connect(self.vissible_signal)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        if self.settingsGUIClass.ShowReacorCheckBox.isChecked() == True:
            self.progressBar.setVisible(True)
            self.reactor_thread = ThreadClass(parent=None)
            self.reactor_thread.any_signal.connect(self.update_prograss)  
            self.reactor_thread.start()
        else:
            self.progressBar.setVisible(False)
        
        self.main_timer.start(int(self.settingsGUIClass.MicSettings.value('TimeOut')))

        self.Listining_label.setVisible(True)
        self.Lang_Button.setVisible(False)
        self.Listining_label.setText('Initialising..')
        self.Stop_btn.setVisible(True)
        self.Mic_btn.setVisible(False)
    def update_prograss(self, volume_level):
        self.progressBar.setValue(volume_level*8)
    def Reset_function(self, info):   
        self.thread.stop()
        self.Listining_label.setVisible(False)
        self.Lang_Button.setVisible(True)
        self.Mic_btn.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".//Imgs//Mic 2 png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Mic_btn.setIcon(icon)
        self.Mic_btn.clicked.connect(self.Mic_pressed)
        if info == "recognition connection failed: [Errno 11001] getaddrinfo failed":
            with open('.//Res//Dont_show_tag_msg.txt', "r") as DSTM:
                DSTM_pos = DSTM.read()
            if  DSTM_pos != "checked":
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"
                                "font: 12pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Error")
                msg.setText("Recognition connection failed.\nMaybe it was an internet connection problem or you haven't selected the correct language.")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                cb = QtWidgets.QCheckBox(msg)
                cb.setText("Don't show this message again!")
                cb.setGeometry(QtCore.QRect(20, 90, 250, 20))
                cb.setStyleSheet("QCheckBox{\n"
                                                "        background: transparent;\n"
                                                "        color: black;\n"

                                                "        \n"
                                                "    font: 75 10pt \"Arial\";\n"
                                                "}\n"
                                                "\n"
                                                "QCheckBox:hover{\n"
                                                "        color: white;\n"

                                                "        font: 75 8pt \"Arial\";\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "QCheckBox::indicator{\n"
                                                "        border: 2px solid rgb(72, 201, 176);\n"
                                                "        width: 10 px;\n"
                                                "        height: 10px;\n"
                                                "        border-radius:3px;\n"
                                                "        background:transparent;\n"
                                                "}\n"
                                                "\n"
                                                "QCheckBox::indicator:hover{\n"
                                                "        border: 2px solid rgb(163, 228, 215);\n"
                                                "        width: 9 px;\n"
                                                "        height: 9px;\n"
                                                "        border-radius:4px;\n"
                                                "        \n"
                                                "}\n"
                                                "\n"
                                                "QCheckBox::indicator:checked{\n"
                                                "        border: 3px solid rgb(163, 228, 215);\n"
                                                "        width: 12 px;\n"
                                                "        height: 12px;\n"
                                                "        border-radius:5px;\n"
                                                "       \n"
                                                "        image: url(Tic_seign.png);\n"
                                            

                                                "}\n"
                                                "\n"
                                                "\n"
                                                "")
                cb.clicked.connect(self.Dont_show_tag_msg)
                msg_exec = msg.exec_()
    
        if info == "[WinError 10060]\nA connection attempt failed because the connected party did not properly respond after a period of time,\n or established connection failed because connected host has failed to respond":
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"
                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Error")
            msg.setText("[WinError 10060]\nA connection attempt failed because the connected party did not properly respond after a period of time,\n or established connection failed because connected host has failed to respond")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()
    def Stop_thread(self):  
        try:
            self.main_timer.stop()
            self.progressBar.setVisible(False)
            try:
                self.start_thread = threading.Thread(target=stop_sig)
                self.start_thread.start()
            except Exception as e:
                pass
            try:
                self.thread.stop()
                if self.settingsGUIClass.ShowReacorCheckBox.isChecked() == True:    
                    try:    
                        self.reactor_thread.stop()
                    except Exception:
                        pass
                self.Listining_label.setVisible(False)   
                self.Stop_btn.setVisible(False)
                self.Mic_btn.setVisible(True)
                self.Lang_Button.setVisible(True)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                self.Listining_label.setVisible(False)   
                self.Stop_btn.setVisible(False)
                self.Mic_btn.setVisible(True)
                self.Lang_Button.setVisible(True)   
                try:
                    self.thread.stop()
                except Exception as e:
                    pass
        except Exception as e:
            print(e+'803') 
    def inint_cmd(self):  
        try:
            self.progressBar.setVisible(False)
            try:
                self.start_thread = threading.Thread(target=stop_sig)
                self.start_thread.start()
            except Exception as e:
                print('line 620')
                pass
            try:
                self.thread.any_signal.connect()
                self.thread.stop()
                self.Listining_label.setVisible(False)   
                self.Stop_btn.setVisible(False)
                self.Mic_btn.setVisible(True)
                self.Lang_Button.setVisible(True)
            except Exception as e:
                self.Listining_label.setVisible(False)   
                self.Stop_btn.setVisible(False)
                self.Mic_btn.setVisible(True)
                self.Lang_Button.setVisible(True)   
        except Exception as e:
            print(e+'803')               
    def vissible_signal(self, info):
        try:    
            if info == 'commend compleated brauh!':
                self.inint_cmd()
                pass
            if info == 'Stop':
                self.listener.stop()
                return
            if info == 'Start':    
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
                self.listener.start()
                return
            if info == 'Listening...':    
                self.Listining_label.setText('Listening..')
                self.progressBar.setVisible(True)
            if info == 'Listining completed!':
                self.Listining_label.setText('Recognising..')   
            if info == 'recognition complete':
                self.Listining_label.setText('Listening..')
                self.progressBar.setVisible(True)
            if info == "recognition connection failed: [Errno 11001] getaddrinfo failed":
                self.Stop_thread()
                with open('.//Res//Dont_show_tag_msg.txt', "r") as DSTM:
                    DSTM_pos = DSTM.read()
                if  DSTM_pos != "checked":
                    msg = QMessageBox()
                    msg.setStyleSheet("QMessageBox{\n"
                                    "color: white;\n"
                                    "background-color: rgb(108, 177, 223);\n"
                                    "font: 12pt \"MS Shell Dlg 2\";\n"
                                    "gridline-color: #EAEDED;\n"
                                    "}")
                    msg.setWindowTitle("Error")
                    msg.setText("Recognition connection failed.\nMaybe it was an internet connection problem or you haven't selected the correct language.")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                    cb = QtWidgets.QCheckBox(msg)
                    cb.setText("Don't show this message again!")
                    cb.setGeometry(QtCore.QRect(20, 90, 250, 20))
                    cb.setStyleSheet("QCheckBox{\n"
                                                    "        background: transparent;\n"
                                                    "        color: black;\n"

                                                    "        \n"
                                                    "    font: 75 10pt \"Arial\";\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox:hover{\n"
                                                    "        color: white;\n"

                                                    "        font: 75 8pt \"Arial\";\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "QCheckBox::indicator{\n"
                                                    "        border: 2px solid rgb(72, 201, 176);\n"
                                                    "        width: 10 px;\n"
                                                    "        height: 10px;\n"
                                                    "        border-radius:3px;\n"
                                                    "        background:transparent;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:hover{\n"
                                                    "        border: 2px solid rgb(163, 228, 215);\n"
                                                    "        width: 9 px;\n"
                                                    "        height: 9px;\n"
                                                    "        border-radius:4px;\n"
                                                    "        \n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked{\n"
                                                    "        border: 3px solid rgb(163, 228, 215);\n"
                                                    "        width: 12 px;\n"
                                                    "        height: 12px;\n"
                                                    "        border-radius:5px;\n"
                                                    "       \n"
                                                    "        image: url(Tic_seign.png);\n"
                                                

                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "")
                    cb.clicked.connect(self.Dont_show_tag_msg)
                    msg_exec = msg.exec_()
                    self.Stop_thread()
            if info == "Audio recording problem problem":
                self.Listining_label.setText('Not listining!')
            if 'Audio recording problem problem' in info:
                
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"
                                "font: 12pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Error")
                msg.setText(f"Recognition connection failed.\n{info}")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                msg.exec_()
                # self.Stop_thread()

        except Exception:
            print('vissible_signal error!')
            pass                
    def current_version_check(self):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{\n"
                        "color: white;\n"
                        "background-color: rgb(108, 177, 223);\n"
                        "font: 12pt \"MS Shell Dlg 2\";\n"
                        "gridline-color: #EAEDED;\n"
                        "}")
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Current version")
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.setText("It's BETA version of Kontho!")
        msg.setIcon(QMessageBox.Information)
        msg_exec = msg.exec_()
    def Dont_show_tag_msg(self):
        with open('.//Res//Dont_show_tag_msg.txt', "r") as DSTM:
            DSTM_pos = DSTM.read()
        if DSTM_pos == "unchecked":    
            with open('.//Res//Dont_show_tag_msg.txt', "w") as DSTM:
                DSTM.write("checked")
        if DSTM_pos == "checked":    
            with open('.//Res//Dont_show_tag_msg.txt', "w") as DSTM:
                DSTM.write("unchecked")        
        pass   
    
    def update_lang(self):  
        if self.current_language == "Bangla":
            self.current_language = "English"
            self.Lang_Button.setText("English")
            kb2.unhook_all()
            
            # self.listener.stop()

            self.initialize()
    
            self.listClass.listWidget.setStyleSheet(EnglishTheme)

        else:
            self.current_language = "Bangla"
            self.Lang_Button.setText("Bangla")

            self.listener.stop()
            for i in self.keysToBlock:
                kb2.block_key(i)
            
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
            self.listener.start()
            self.listClass.hide()
            self.initialize()

            self.listClass.listWidget.setStyleSheet(BanglaTheme)


            pass
        try:
            sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Switch_lang_SFX.wav', winsound.SND_FILENAME))
            sound_thread.start()
        except Exception:
            pass
    def init_animation(self):
        func_btn_ani_duration = 150
        frame_animation_duration = 300

        self.SettingsBtn_anim = QPropertyAnimation(self.Settings_btn, b"geometry")
        self.SettingsBtn_anim.setDuration(func_btn_ani_duration)
        self.SettingsBtn_anim.setStartValue(QRect(211, 2, 25,25))
        self.SettingsBtn_anim.setEndValue(QRect(211, 30, 25,25))
        self.SettingsBtn_anim.start()

        self.WavtoTextBtn_anim = QPropertyAnimation(self.Wav_to_Text_button, b"geometry")
        self.WavtoTextBtn_anim.setDuration(func_btn_ani_duration)
        self.WavtoTextBtn_anim.setStartValue(QRect(130, 2, 25,25))
        self.WavtoTextBtn_anim.setEndValue(QRect(130, 30, 25,25))
        self.WavtoTextBtn_anim.start()

        self.OCR_Btn_anim = QPropertyAnimation(self.OCR_Btn, b"geometry")
        self.OCR_Btn_anim.setDuration(func_btn_ani_duration)
        self.OCR_Btn_anim.setStartValue(QRect(184, 2, 25,25))
        self.OCR_Btn_anim.setEndValue(QRect(184, 30, 25,25))
        self.OCR_Btn_anim.start()

        self.ConvertBtn_anim = QPropertyAnimation(self.OnScreenKeyboardBtn, b"geometry")
        self.ConvertBtn_anim.setDuration(func_btn_ani_duration)
        self.ConvertBtn_anim.setStartValue(QRect(157, 2, 25,25))
        self.ConvertBtn_anim.setEndValue(QRect(157, 30, 25,25))
        self.ConvertBtn_anim.start()

        self.DocpadBtn_anim = QPropertyAnimation(self.ScriptPad_btn, b"geometry")
        self.DocpadBtn_anim.setDuration(func_btn_ani_duration)
        self.DocpadBtn_anim.setStartValue(QRect(103, 2, 25,25))
        self.DocpadBtn_anim.setEndValue(QRect(103, 30, 25,25))
        self.DocpadBtn_anim.start()

        self.CloseBtn_anim = QPropertyAnimation(self.Close_btn, b"geometry")
        self.CloseBtn_anim.setDuration(frame_animation_duration)
        self.CloseBtn_anim.setStartValue(QRect(237, 2, 25,25))
        self.CloseBtn_anim.setEndValue(QRect(102, 2, 25,25))
        self.CloseBtn_anim.start()

        self.Lang_Button.setGeometry(QRect(29, 2, 72, 24))
        self.progressBar.setGeometry(QRect(29, 2, 72, 24))

        self.Main_anim = QPropertyAnimation(self.frame, b"geometry")
        self.Main_anim.setDuration(frame_animation_duration)
        self.Main_anim.setStartValue(QRect(0, 0, 266, 29))
        self.Main_anim.setEndValue(QRect(0, 0, 130, 29))
        self.Main_anim.start()
        pass
    def aro_button_clicked(self):
        
        self.DocpadBtn_anim.stop()
        self.ConvertBtn_anim.stop()
        self.WavtoTextBtn_anim.stop()
        self.SettingsBtn_anim.stop()

        self.CloseBtn_anim.stop()
        self.OCR_Btn_anim.stop()
        # self.Close_btn.setVisible(False)

        func_btn_ani_duration = 120
        frame_animation_duration = 200

        self.SettingsBtn_anim = QPropertyAnimation(self.Settings_btn, b"geometry")
        self.SettingsBtn_anim.setDuration(func_btn_ani_duration)
        self.SettingsBtn_anim.setStartValue(QRect(211, 2, 25,25))
        self.SettingsBtn_anim.setEndValue(QRect(211, 30, 25,25))
        self.SettingsBtn_anim.start()

        self.WavtoTextBtn_anim = QPropertyAnimation(self.Wav_to_Text_button, b"geometry")
        self.WavtoTextBtn_anim.setDuration(func_btn_ani_duration)
        self.WavtoTextBtn_anim.setStartValue(QRect(130, 2, 25,25))
        self.WavtoTextBtn_anim.setEndValue(QRect(130, 30, 25,25))
        self.WavtoTextBtn_anim.start()

        self.OCR_Btn_anim = QPropertyAnimation(self.OCR_Btn, b"geometry")
        self.OCR_Btn_anim.setDuration(func_btn_ani_duration)
        self.OCR_Btn_anim.setStartValue(QRect(184, 2, 25,25))
        self.OCR_Btn_anim.setEndValue(QRect(184, 30, 25,25))
        self.OCR_Btn_anim.start()

        self.ConvertBtn_anim = QPropertyAnimation(self.OnScreenKeyboardBtn, b"geometry")
        self.ConvertBtn_anim.setDuration(func_btn_ani_duration)
        self.ConvertBtn_anim.setStartValue(QRect(157, 2, 25,25))
        self.ConvertBtn_anim.setEndValue(QRect(157, 30, 25,25))
        self.ConvertBtn_anim.start()

        self.DocpadBtn_anim = QPropertyAnimation(self.ScriptPad_btn, b"geometry")
        self.DocpadBtn_anim.setDuration(func_btn_ani_duration)
        self.DocpadBtn_anim.setStartValue(QRect(103, 2, 25,25))
        self.DocpadBtn_anim.setEndValue(QRect(103, 30, 25,25))
        self.DocpadBtn_anim.start()

        self.CloseBtn_anim = QPropertyAnimation(self.Close_btn, b"geometry")
        self.CloseBtn_anim.setEasingCurve(QEasingCurve.Linear) 

        self.CloseBtn_anim.setDuration(frame_animation_duration)
        self.CloseBtn_anim.setStartValue(QRect(238, 2, 25,25))
        self.CloseBtn_anim.setEndValue(QRect(102, 2, 25,25))
        self.CloseBtn_anim.start()

        # self.Listining_label.setGeometry(QRect(30, 2, 90, 24))
        self.Lang_Button.setGeometry(QRect(29, 2, 72, 24))
        self.progressBar.setGeometry(QRect(29, 2, 72, 24))

        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(".//Imgs//Right aro for main.png"))
        # self.Aro_btn.setIcon(icon2)
        # self.Aro_btn_2.setIcon(icon2)


        # self.AroBtn_anim = QPropertyAnimation(self.Aro_btn, b"geometry")
        # self.AroBtn_anim.setDuration(250)
        # self.AroBtn_anim.setStartValue(QRect(238, 2, 25,25))
        # self.AroBtn_anim.setEndValue(QRect(121, 2, 25,25))
        # self.AroBtn_anim.start()

        # self.AroBtn_anim2 = QPropertyAnimation(self.Aro_btn_2, b"geometry")
        # self.AroBtn_anim2.setDuration(250)
        # self.AroBtn_anim2.setStartValue(QRect(238, 2, 25,25))
        # self.AroBtn_anim2.setEndValue(QRect(121, 2, 25,25))
        # self.AroBtn_anim2.start()

        self.Main_anim = QPropertyAnimation(self.frame, b"geometry")
        self.Main_anim.setEasingCurve(QEasingCurve.Linear)
        self.Main_anim.setDuration(frame_animation_duration)
        self.Main_anim.setStartValue(QRect(0, 0, 266, 29))
        self.Main_anim.setEndValue(QRect(0, 0, 130, 29))
        self.Main_anim.start()
    
        # self.Aro_btn.setVisible(False)
        # self.Aro_btn_2.setVisible(True)
        self.dance_time.stop()

        pass
    def aro_button_clicked_again(self): #hover in animation
        # ============ Stop animation ==================================================
        if self.first_animation == False:
            # ============ Stop animation ==================================================
            self.Main_anim.stop()
            # self.AroBtn_anim.stop()
            self.DocpadBtn_anim.stop()
            self.ConvertBtn_anim.stop()
            self.WavtoTextBtn_anim.stop()
            self.SettingsBtn_anim.stop()
            self.CloseBtn_anim.stop()
            self.OCR_Btn_anim.stop()
            # ============ Stop animation ==================================================     
        else:
            self.first_animation = False
        
        
        func_btn_ani_duration = 200
        frame_animation_duration = 125
        
        # ============ Stop animation ==================================================

        self.Main_anim = QPropertyAnimation(self.frame, b"geometry")
        self.Main_anim.setEasingCurve(QEasingCurve.Linear)
        self.Main_anim.setDuration(frame_animation_duration)
        self.Main_anim.setStartValue(QRect(0, 0, 149, 29))
        self.Main_anim.setEndValue(QRect(0, 0, 266, 29))
        self.Main_anim.easingCurve
        self.Main_anim.start()


        self.CloseBtn_anim = QPropertyAnimation(self.Close_btn, b"geometry")
        self.CloseBtn_anim.setEasingCurve(QEasingCurve.Linear) 

        self.CloseBtn_anim.setDuration(frame_animation_duration)
        self.CloseBtn_anim.setStartValue(QRect(121, 2, 25,25))
        self.CloseBtn_anim.setEndValue(QRect(238, 2, 25,25))
        self.CloseBtn_anim.start()
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(".//Imgs//Left aro for main.png"))
        # self.Aro_btn.setIcon(icon2)
        # self.Aro_btn_2.setIcon(icon2)


        # self.AroBtn_anim = QPropertyAnimation(self.Aro_btn, b"geometry")
        # self.AroBtn_anim.setDuration(200)
        # self.AroBtn_anim.setStartValue(QRect(121, 2, 25,25))
        # self.AroBtn_anim.setEndValue(QRect(238, 2, 25,25))
        # self.AroBtn_anim.start()

        # self.AroBtn_anim_2 = QPropertyAnimation(self.Aro_btn_2, b"geometry")
        # self.AroBtn_anim_2.setDuration(200)
        # self.AroBtn_anim_2.setStartValue(QRect(121, 2, 25,25))
        # self.AroBtn_anim_2.setEndValue(QRect(238, 2, 25,25))
        # self.AroBtn_anim_2.start()
        self.DocpadBtn_anim = QPropertyAnimation(self.ScriptPad_btn, b"geometry")
        self.DocpadBtn_anim.setEasingCurve(QEasingCurve.Linear)
        self.DocpadBtn_anim.setDuration(150)
        self.DocpadBtn_anim.setStartValue(QRect(103, 30, 25,25))
        self.DocpadBtn_anim.setEndValue(QRect(103, 2, 25,25))
        self.DocpadBtn_anim.start()

        self.WavtoTextBtn_anim = QPropertyAnimation(self.Wav_to_Text_button, b"geometry")
        self.WavtoTextBtn_anim.setEasingCurve(QEasingCurve.Linear)
        self.WavtoTextBtn_anim.setDuration(175)
        self.WavtoTextBtn_anim.setStartValue(QRect(130, 30, 25,25))
        self.WavtoTextBtn_anim.setEndValue(QRect(130, 2, 25,25))
        self.WavtoTextBtn_anim.start()

        self.ConvertBtn_anim = QPropertyAnimation(self.OnScreenKeyboardBtn, b"geometry")
        self.ConvertBtn_anim.setEasingCurve(QEasingCurve.Linear)
        self.ConvertBtn_anim.setDuration(200)
        self.ConvertBtn_anim.setStartValue(QRect(157, 30, 25,25))
        self.ConvertBtn_anim.setEndValue(QRect(157, 2, 25,25))
        self.ConvertBtn_anim.start()

        self.OCR_Btn_anim = QPropertyAnimation(self.OCR_Btn, b"geometry")
        self.OCR_Btn_anim.setEasingCurve(QEasingCurve.Linear)
        self.OCR_Btn_anim.setDuration(225)
        self.OCR_Btn_anim.setStartValue(QRect(184, 30, 25,25))
        self.OCR_Btn_anim.setEndValue(QRect(184, 2, 25,25))
        self.OCR_Btn_anim.start()
        
        self.SettingsBtn_anim = QPropertyAnimation(self.Settings_btn, b"geometry")
        self.SettingsBtn_anim.setEasingCurve(QEasingCurve.Linear)
        self.SettingsBtn_anim.setDuration(250)
        self.SettingsBtn_anim.setStartValue(QRect(211, 30, 25,25))
        self.SettingsBtn_anim.setEndValue(QRect(211, 2, 25,25))
        self.SettingsBtn_anim.start()
        

        self.Close_btn.setVisible(True)

        # self.Listining_label.setGeometry(QRect(30, 2, 95, 24))
        self.Lang_Button.setGeometry(QRect(29, 2, 72, 24))
        self.progressBar.setGeometry(QRect(29, 2, 72, 24))


        modifierPressed = QApplication.keyboardModifiers()
        modifierName = ''
        # if (modifierPressed & Qt.ShiftModifier) == Qt.ShiftModifier:
        # if (modifierPressed) == Qt.ShiftModifier:  
        if kb2.is_pressed("Shift"):  
            self.Main_anim = QPropertyAnimation(self.frame, b"geometry")
            self.Main_anim.setEasingCurve(QEasingCurve.Linear)
            self.Main_anim.setDuration(frame_animation_duration)
            self.Main_anim.setStartValue(QRect(0, 0, 266, 29))
            self.Main_anim.setEndValue(QRect(0, 0, 266, 55))
            self.Main_anim.easingCurve
            self.Main_anim.start()
    def About_nms(self):
        webbrowser.open('https://docs.google.com/document/d/1_xTSV9MIDumzBs6Hq2roEPRuhvT1XDnkwZ113_jK2Ow/edit?usp=sharing')   
    def close_function(self): 
        # os.system("TASKKILL /F /IM FocusRestrorer.exe")
        # os.system("TASKKILL /F /IM Nms_Keyboard_Layout_BETA.exe")
        # self.KeyBoardLayout.stop()
        QApplication.quit()
    def restart_function(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.aro_button_clicked_again()
        return super().enterEvent(a0)
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.aro_button_clicked()
        return super().leaveEvent(a0)  
    def Dance_Movement(self):
        if self.first_animation == False:
            # ============ Stop animation ==================================================
            # self.Main_anim.stop()
            # self.AroBtn_anim.stop()
            self.DocpadBtn_anim.stop()
            self.ConvertBtn_anim.stop()
            self.WavtoTextBtn_anim.stop()
            self.SettingsBtn_anim.stop()
            # ============ Stop animation ==================================================     
        else:
            self.first_animation = False

        self.Main_anim = QPropertyAnimation(self.frame, b"geometry")
        self.Main_anim.setDuration(200)
        self.Main_anim.setStartValue(QRect(0, 0, 149, 29))
        self.Main_anim.setEndValue(QRect(0, 0, 266, 29))
        self.Main_anim.start()

        self.CloseBtn_anim = QPropertyAnimation(self.Close_btn, b"geometry")
        self.CloseBtn_anim.setDuration(250)
        self.CloseBtn_anim.setStartValue(QRect(121, 2, 25,25))
        self.CloseBtn_anim.setEndValue(QRect(238, 2, 25,25))
        self.CloseBtn_anim.start()

        self.SettingsBtn_anim = QPropertyAnimation(self.Settings_btn, b"geometry")
        self.SettingsBtn_anim.setDuration(100)
        self.SettingsBtn_anim.setStartValue(QRect(212, 30, 25,25))
        self.SettingsBtn_anim.setEndValue(QRect(212, 2, 25,25))
        self.SettingsBtn_anim.start()
        
        self.WavtoTextBtn_anim = QPropertyAnimation(self.Wav_to_Text_button, b"geometry")
        self.WavtoTextBtn_anim.setDuration(100)
        self.WavtoTextBtn_anim.setStartValue(QRect(185, 30, 25,25))
        self.WavtoTextBtn_anim.setEndValue(QRect(185, 2, 25,25))
        self.WavtoTextBtn_anim.start()

        self.ConvertBtn_anim = QPropertyAnimation(self.OnScreenKeyboardBtn, b"geometry")
        self.ConvertBtn_anim.setDuration(100)
        self.ConvertBtn_anim.setStartValue(QRect(158, 10, 25,25))
        self.ConvertBtn_anim.setEndValue(QRect(158, 2, 25,25))
        self.ConvertBtn_anim.start()

        self.DocpadBtn_anim = QPropertyAnimation(self.ScriptPad_btn, b"geometry")
        self.DocpadBtn_anim.setDuration(100)
        self.DocpadBtn_anim.setStartValue(QRect(131, 30, 25,25))
        self.DocpadBtn_anim.setEndValue(QRect(131, 2, 25,25))
        self.DocpadBtn_anim.start()

        self.Close_btn.setVisible(True)
        self.Lang_Button.setGeometry(QRect(30, 2, 100, 24))
        self.progressBar.setGeometry(QRect(30, 2, 100, 24))

        self.dance_time.start(300)
    def openBanglishLayout(self):
        try:
            os.startfile("Nms KboardLayout Map.pdf")
        except Exception as e:
            self.showError(e)
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
    def closeEvent(self, event):
        self.close_function()    

counter = 10

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

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(10)
        self.ui = Ui()
        self.ui.show()

    def progress(self):

        global counter

        self.progressBar.setValue(counter)

        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            self.close()
            # self.ui = Ui()
            # self.ui.show()   < --------trigar to show the main gui after the flashscreen


        # INCREASE COUNTER
        counter += 1

class Ui_Error(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Error, self).__init__() 
        uic.loadUi('.//Uis//ErrorUi.ui', self)
    def showError(self, e):
        self.plainTextEdit.setPlainText(e)
        self.show()

if __name__ == "__main__":
    print("application openning....")
    try:
        app = QApplication(sys.argv)
        ex = Ui()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)   
        # print(traceback.format_exc()) 
        app2 = QApplication(sys.argv)
        error_class = Ui_Error()
        error_class.show()
        error_class.showError(str(traceback.format_exc()))
        sys.exit(app2.exec_())    