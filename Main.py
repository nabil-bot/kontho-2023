# -*- coding:utf-8 -*-

import time
from tkinter.tix import Tree
import keyboard as kb2
import speech_recognition as sr
from pynput.keyboard import Controller, Key
kb = Controller()
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QTimer, QSettings, QEasingCurve, QEvent
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QApplication, QMessageBox, QGraphicsDropShadowEffect, QVBoxLayout, QGridLayout, QPushButton, QGroupBox
from PyQt5.QtGui import QPainter, QColor 
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
User32 = ctypes.WinDLL('User32.dll')

from win32gui import GetWindowText, GetCursorPos, WindowFromPoint, GetForegroundWindow, GetWindowRect, GetCaretPos, GetCursorInfo
from AddNewWord import AddNewWordsClass
from WordManager import wordManagerClass
from LoadWords import wordsList,englaList,EnglishwordsList,englishLatters, banglaNumbs
from pynput import keyboard
import NumberToWord


# ++++++++++++++++global variables ====================
similarTheredIsRunning = False
previous_word = ""
formar_previous_word = ""
previous_formar_previous_word = ""
formar_previous_formar_previous_word = ""
wordSofar = ""
englishWordSofar = ""
shiftKeyBlocked = False
keysBlocked = True
completorTraegered = False 
CurrentWord = ""
ruledOut = False
minimun_Similarity_Ratio = 0.70

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





ahkScript = "global pinedState := 0 \nreviousXPos := 0\npreviousYPos := 0\nSetTimer, setPos, 100\nsetPos:\nglobal pinedState\nif pinedState = 0\n{\n	WinGetActiveTitle, wintitle\n	WinGetPos, perant_X, perant_Y,,, %wintitle%\n	position_X := A_CaretX + perant_X\n	position_Y := A_CaretY + perant_Y\n	if position_X != previousXPos and position_Y != previousYPos\n		WinMove, Nms_completer,, position_X, position_Y\n		previousXPos = %position_X%\n		previousYPos = %position_Y%\n}\nIfWinNotExist, Nms Voice pad\n{\n	ExitApp\n}\nreturn\nF23::\nglobal pinedState\nif pinedState = 0\n{\n	pinedState = 1\n	return\n}\nif pinedState = 1\n{\n	pinedState = 0\n}\nreturn\nF12::\nExitApp"


keysToBlock = [2,3,4,5,6,7,8,9,10,11,  16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,   44,45,46,47,48,49,50,  52]    
upDownKey = [ 79 , 80]


def convert(text):
    text = text.replace('ড়', 'ড়')
    text = text.replace('ঢ়', 'ঢ়')
    text = text.replace('য়', 'য়')
    test = converter.Unicode()
    demo_text = ('2007 এ ফিলিস্তিনের নির্ধারিত গাজা ভূখণ্ডে নির্ধারণ প্রতিষ্ঠা করা হয়')
    toPrint = test.convertUnicodeToBijoy(f'{demo_text} {text}')
    rang = len(toPrint)
    if '©' in toPrint:      # this reset rep  
        pass_loop = -1
        custom_text = ''
        for index in range(rang):  
            if index == pass_loop:
                custom_text += toPrint[index]
                custom_text += '©'
                continue
            if toPrint[index] == '©':
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
                    if toPrint[index + 1] == 'w' or toPrint[index + 1] == '‡' or toPrint[index + 1] == '‰' or toPrint[index + 1] == 'Š':
                        pass_loop = loop_count + 1
                        index_l = toPrint[index]
                    else:
                        custom_text += toPrint[index]   
                        
                else:
                    custom_text += toPrint[index] 
            except Exception:
                pass    
        pass

    if 'ª¨' in custom_text:
        fixed_text = custom_text.replace('ª¨', '¨')
        custom_text = fixed_text
    if 'i‌¨v' in custom_text:
        fixed_text = custom_text.replace('i‌¨v', 'i¨v')
        custom_text = fixed_text
    if 'h©v' in custom_text: 
        fixed_text = custom_text.replace('h©v', 'i¨v')
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
        

class Main_recognation(QtCore.QThread):	
    recognize_signal = QtCore.pyqtSignal(str)
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
            if self.UANSI_pos == 'False':    
                if self.lang == 'bn-BD':
                    # for word, initial in {"1":"১", "2":"২", "3":"৩", "4":"৪", "5":"৫", "6":"৬", "7":"৭", "8":"৮", "9": "৯", "0": "০"  }.items():
                    #     text = text.replace(word, initial)
                    for word, initial in {"পর‍্যায় ":"পর্যায়"}.items():
                        text = text.replace(word, initial)
                    if 'র্যা' in text:
                        text = text.replace('র্যা', 'র‍্যা') 
                    if ' প্রশ্নবোধক চিহ্ন' in text or ' জিজ্ঞাসা বোধক চিহ্ন' in text or ' প্রশ্ন বোধক চিহ্ন' in text:
                        if ' প্রশ্নবোধক চিহ্ন' in text:
                            text = text.replace(' প্রশ্নবোধক চিহ্ন', '?')
                        if ' প্রশ্ন বোধক চিহ্ন' in text:
                            text = text.replace(' প্রশ্ন বোধক চিহ্ন', '?')    
                        if ' জিজ্ঞাসা বোধক চিহ্ন' in text: 
                            text = text.replace(' জিজ্ঞাসা বোধক চিহ্ন', '?')       
                    if ' আশ্চর্যবোধক চিহ্ন' in text or ' বিস্ময়বোধক চিহ্ন' in text or ' আশ্চর্য বোধক চিহ্ন' in text  or ' বিস্ময় বোধক চিহ্ন' in text or ' সম্বোধন চিহ্ন' in text:
                        if ' আশ্চর্য বোধক চিহ্ন' in text:
                            text = text.replace(' আশ্চর্য বোধক চিহ্ন', '!') 
                        if ' আশ্চর্যবোধক চিহ্ন' in text:
                            text = text.replace(' আশ্চর্যবোধক চিহ্ন', '!') 
                                
                        if ' বিস্ময়বোধক চিহ্ন' in text:
                            text = text.replace(' বিস্ময়বোধক চিহ্ন', '!') 
                        if ' বিস্ময় বোধক চিহ্ন' in text:
                            text = text.replace(' বিস্ময় বোধক চিহ্ন', '!') 
                        if ' সম্বোধন চিহ্ন' in text:
                            text = text.replace(' সম্বোধন চিহ্ন', '!')     
                    if ' দাড়ি চিহ্ন' in text or ' পূর্ণচ্ছেদ চিহ্ন' in text:
                        if ' দাড়ি চিহ্ন' in text:
                            text = text.replace(' দাড়ি চিহ্ন', '।')
                        if ' পূর্ণচ্ছেদ চিহ্ন' in text:
                            text = text.replace(' পূর্ণচ্ছেদ চিহ্ন', '।') 
                    if ' কমা চিহ্ন' in text or ' পাদচ্ছেদ চিহ্ন' in text:
                        if ' কমা চিহ্ন' in text:
                            text = text.replace(' কমা চিহ্ন', ',')
                        if ' পাদচ্ছেদ চিহ্ন' in text:
                            text = text.replace(' পাদচ্ছেদ চিহ্ন', ',')
                    if ' সেমি কোলন চিহ্ন' in text or ' সেমিকোলন চিহ্ন' in text:
                        if ' সেমি কোলন চিহ্ন' in text:
                            text = text.replace(' সেমি কোলন চিহ্ন', ';')
                        if ' সেমিকোলন চিহ্ন' in text:
                            text = text.replace(' সেমিকোলন চিহ্ন', ';')
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
                    words = txt_.split(' ')
                    if words[-1] in ["কি", "কেন", "কীভাবে", "কোথায়", "কোথাকার"]: 
                        words[-1] = words[-1]+"?"    
                    for w in words:
                        kb.type(w)  
                        pyautogui.write(' ') 
                    
                except Exception as e:
                    print('type error; UANSI_pos == False')
                    print(e)
            if self.UANSI_pos == 'True':    
                if self.lang == 'bn-BD':    
                    toPrint = convert(text)
                else:
                    toPrint = text
                try:

                    words = toPrint.split(' ')
                    for w in words:
                        kb.type(w)  
                        pyautogui.write(' ')    
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
                                for word, initial in {"1":"১", "2":"২", "3":"৩", "4":"৪", "5":"৫", "6":"৬", "7":"৭", "8":"৮", "9": "৯", "0": "০"  }.items():
                                    text = text.replace(word, initial)
                                if 'র্যা' in text:
                                    text = text.replace('র্যা', 'র‍্যা') 
                                if ' প্রশ্নবোধক চিহ্ন' in text or ' জিজ্ঞাসা বোধক চিহ্ন' in text or ' প্রশ্ন বোধক চিহ্ন' in text:
                                    if ' প্রশ্নবোধক চিহ্ন' in text:
                                        text = text.replace(' প্রশ্নবোধক চিহ্ন', '?')
                                    if ' প্রশ্ন বোধক চিহ্ন' in text:
                                        text = text.replace(' প্রশ্ন বোধক চিহ্ন', '?')    
                                    if ' জিজ্ঞাসা বোধক চিহ্ন' in text: 
                                        text = text.replace(' জিজ্ঞাসা বোধক চিহ্ন', '?')       
                                if ' আশ্চর্যবোধক চিহ্ন' in text or ' বিস্ময়বোধক চিহ্ন' in text or ' আশ্চর্য বোধক চিহ্ন' in text  or ' বিস্ময় বোধক চিহ্ন' in text or ' সম্বোধন চিহ্ন' in text:
                                    if ' আশ্চর্য বোধক চিহ্ন' in text:
                                        text = text.replace(' আশ্চর্য বোধক চিহ্ন', '!') 
                                    if ' আশ্চর্যবোধক চিহ্ন' in text:
                                        text = text.replace(' আশ্চর্যবোধক চিহ্ন', '!') 
                                            
                                    if ' বিস্ময়বোধক চিহ্ন' in text:
                                        text = text.replace(' বিস্ময়বোধক চিহ্ন', '!') 
                                    if ' বিস্ময় বোধক চিহ্ন' in text:
                                        text = text.replace(' বিস্ময় বোধক চিহ্ন', '!') 
                                    if ' সম্বোধন চিহ্ন' in text:
                                        text = text.replace(' সম্বোধন চিহ্ন', '!')     
                                if ' দাড়ি চিহ্ন' in text or ' পূর্ণচ্ছেদ চিহ্ন' in text:
                                    if ' দাড়ি চিহ্ন' in text:
                                        text = text.replace(' দাড়ি চিহ্ন', '।')
                                    if ' পূর্ণচ্ছেদ চিহ্ন' in text:
                                        text = text.replace(' পূর্ণচ্ছেদ চিহ্ন', '।') 
                                if ' কমা চিহ্ন' in text or ' পাদচ্ছেদ চিহ্ন' in text:
                                    if ' কমা চিহ্ন' in text:
                                        text = text.replace(' কমা চিহ্ন', ',')
                                    if ' পাদচ্ছেদ চিহ্ন' in text:
                                        text = text.replace(' পাদচ্ছেদ চিহ্ন', ',')
                                if ' সেমি কোলন চিহ্ন' in text or ' সেমিকোলন চিহ্ন' in text:
                                    if ' সেমি কোলন চিহ্ন' in text:
                                        text = text.replace(' সেমি কোলন চিহ্ন', ';')
                                    if ' সেমিকোলন চিহ্ন' in text:
                                        text = text.replace(' সেমিকোলন চিহ্ন', ';')
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
                                toPrint = convert(text)
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

class similarityThread(QtCore.QThread):
    mostMatchedWords = QtCore.pyqtSignal(list)
    ruledOutSimiSignal = QtCore.pyqtSignal(bool)            # call preventer signal 1
    similarTheredIsRunningSignal = QtCore.pyqtSignal(bool, bool, str)  # call preventer signal 2
    def __init__(self, englishWordSoFar = "", currentLang = "", parent=None):
        super(similarityThread, self).__init__(parent)
        self.is_running = True
        
        self.englishWordSoFar = englishWordSoFar
        self.currentLang = currentLang
        self.ruledOutSimi = False
        self.brokenByNewCharacter = False
               
    def run(self):
        global minimun_Similarity_Ratio
        self.newCharacterIsPressed = False 
        self.similarTheredIsRunningSignal.emit(True, self.brokenByNewCharacter, self.englishWordSoFar)
        self.similarWords = []
        self.heighestMatchedRatio = 0  
        
        if self.currentLang == "bangla":
            currentwordsList = wordsList
        else:
            currentwordsList = EnglishwordsList


        for wrd in currentwordsList[:]: 
            if self.currentLang == "bangla":
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
            
            similarity = self.similarity_ration_btween(englishWord, englishWordSofar)   
            if len(englishWordSofar) < 5:
                minimumSimi = minimun_Similarity_Ratio
            else:
                minimumSimi = minimun_Similarity_Ratio   
            if similarity > minimumSimi:
                if similarity > self.heighestMatchedRatio:
                    if self.currentLang == "bangla":    
                        self.similarWords.insert(0, banglaWord)
                    else:
                        self.similarWords.insert(0, englishWord)

                    self.heighestMatchedRatio = similarity
                else:
                    if self.currentLang == "bangla":    
                        self.similarWords.append(banglaWord)
                    else:
                        self.similarWords.append(englishWord)

                        
            if len(self.similarWords) > 9 or self.newCharacterIsPressed == True:
                if self.newCharacterIsPressed == True:  
                    self.brokenByNewCharacter = True
                    # print("broken By new character")
                    # return
                break
        if len(self.similarWords) == 0:
            self.ruledOutSimi = True
            self.ruledOutSimiSignal.emit(True)
            return
        self.mostMatchedWords.emit(self.similarWords)
        self.similarTheredIsRunningSignal.emit(False, self.brokenByNewCharacter, self.englishWordSoFar)
        pass
    def similarity_ration_btween(self, x, y):
        seq = difflib.SequenceMatcher(None,x,y)
        d = seq.ratio()
        return d                
    def newCharecterIsPressedStateChange(self, state):
        self.newCharacterIsPressed = True
    def stop(self):
        self.is_running = False
        # 
        self.terminate()
        


class WhileloopThroughListThread(QtCore.QThread):
    matchedWordsSignal = QtCore.pyqtSignal(list)
    ruledOutSignal = QtCore.pyqtSignal(bool)
    newCherecterIspressed = QtCore.pyqtSignal(bool)
    themeSignal = QtCore.pyqtSignal(str)

    acSignal = QtCore.pyqtSignal(str) # autoCurrect

    def __init__(self, parent=None):
        super(WhileloopThroughListThread, self).__init__(parent)
        
        self.newCharecterState = False
        self.is_running = True
        self.ruledOut = False
        self.ruledOutEngla = False
        self.preWord = ""

        self.ruledOutSimi = False
        self.similarTheredIsRunning = False

        pass
    def run(self):
        while self.is_running:
            global wordSofar
            global englishWordSofar
            if self.preWord != wordSofar and wordSofar != "":   

                self.newCherecterIspressed.emit(True)
                self.matchedWords = []
                try:
                    if wordSofar[0] not in englishLatters and wordSofar[0] not in banglaNumbs:
                        if self.ruledOut == False or len(englishWordSofar) < len(self.preWord):  
                            self.loopThroughList(wordsList,wordSofar,englishWordSofar)    # this gonna check in main dictionary
                            if len(self.matchedWords) == 0:
                                self.ruledOut = True

                        if self.ruledOut == True and self.ruledOutEngla == False:  # englawords dictionary
                            self.loopThroughList(englaList,wordSofar,englishWordSofar)
                            if len(self.matchedWords) == 0:
                                self.ruledOutEngla = True
                            else:    
                                self.themeSignal.emit("blue")


                        if len(self.matchedWords) == 0 and self.ruledOutSimi == False:
                            self.startSimilarityThread(englishWordSofar, 'bangla')   

                    if wordSofar[0] in englishLatters:
                        # ================================
                        englishWordSofar = wordSofar
                        
                        if self.ruledOut == False or len(englishWordSofar) < len(self.preWord):
                            self.loopThroughList(EnglishwordsList,wordSofar,englishWordSofar)
                            if len(self.matchedWords) == 0:
                                self.ruledOut = True

                        if len(self.matchedWords) == 0 and self.ruledOutSimi == False:
                            self.startSimilarityThread(englishWordSofar, 'english')
                        # print(self.matchedWords)

                    # ========================================
                    if wordSofar[0] in banglaNumbs: # banglaNumbs
                        numberInWord = NumberToWord.convert_num_to_word(wordSofar)
                        self.matchedWords.append(numberInWord) 
                        splitedNumbersInword = ""
                        for i in range(len(wordSofar)):
                            splitedNumbersInword += f"{NumberToWord.convert_num_to_word(wordSofar[i])} "
                        
                        self.matchedWords.append(splitedNumbersInword.strip()) 
                    # ========================================    
                except Exception:
                    self.preWord = ""
                    pass


                self.matchedWordsSignal.emit(self.matchedWords)
                self.preWord = wordSofar
            time.sleep(0.1)
     
    def newCharecterIsPressedStateChange(self, state):
        self.newCharacterIsPressed = True
    def updateWord(self, wordSofar, englishWordSofar_local, bangla=""):
        self.wordSofar = wordSofar
        self.englishWordSofar_local = englishWordSofar_local
 
    def loopThroughList(self, wordList, wordSofar, englishWordSofar_local):

        for wrd in wordList[:]:
            wordArray = wrd.split(",")
            if len(wordArray) == 1 and wordSofar !=englishWordSofar_local:
                continue
            mainWord = wordArray[0]
            index = 0
            for wrd in wordArray[:]:
                if mainWord in self.matchedWords:
                    break
                if index == 0 and wrd[:len(wordSofar)] == wordSofar : # and wrd not in self.matchedWords
                    self.matchedWords.append(mainWord)
                    break
                elif (wrd[:len(englishWordSofar_local)]).lower() == (englishWordSofar_local).lower() and mainWord not in self.matchedWords: # and wrd not in self.matchedWords
                    self.matchedWords.append(mainWord)
                    if len(wordSofar) > 3 and wrd.lower() == (englishWordSofar_local).lower() and mainWord != wordSofar:
                        self.acSignal.emit(mainWord)
                        self.preWord = mainWord
                    break
                index += 1
            if len(self.matchedWords) >11 or self.newCharecterState == True:
                if self.newCharecterState == True:
                    print("loop Was breaked by new cherecter")
                break 
          
    def initFunc(self, sig):
        self.ruledOut = False
        self.ruledOutSimi = False
        # print("init signal")
    
    def startSimilarityThread(self,englishWordSofar_local,currentLang):
        
        self.similarityThread = similarityThread(englishWordSofar_local, currentLang)
        if self.similarityThread.isRunning() == False:
            self.similarityThread.ruledOutSimiSignal.connect(self.ruledOutSimiStateChange)
            self.similarityThread.mostMatchedWords.connect(self.addSimiWordsFunc)
            self.newCherecterIspressed.connect(self.similarityThread.newCharecterIsPressedStateChange)
            self.similarityThread.start()
        else:
            print("thread is running")    
    def ruledOutSimiStateChange(self, state):
        self.ruledOutSimi = state
        self.similarTheredIsRunning = False
    
    def addSimiWordsFunc(self, wordList):
        self.matchedWordsSignal.emit(wordList)
        self.themeSignal.emit("yellow")
    def initFunc(self, sig):
        self.ruledOut = False
        self.ruledOutSimi = False
        self.ruledOutEngla = False
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
        self.whileLoopThread.acSignal.connect(self.sendAcSignal)
        self.whileLoopThread.finished.connect(self.whileLoopThread.deleteLater)
        self.whileLoopThread.themeSignal.connect(self.emitTheme)
        self.initSignal.connect(self.whileLoopThread.initFunc)
        self.newCherecterIspressed.connect(self.whileLoopThread.newCharecterIsPressedStateChange)
        # self.ruledOutSig.connect(self.whileLoopThread.initFunc)

        self.whileLoopThread.start()


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
                self.similarityThreadForOsk = similarityThreadForOsk(BanglaWord)
                self.similarityThreadForOsk.ruledOutSimiSignal.connect(self.ruledOutSimiStateChange)
                self.similarityThreadForOsk.mostMatchedWords.connect(self.addSimiWordsFunc)
                self.similarityThreadForOsk.similarTheredIsRunningSignal.connect(self.similarTheredIsRunningStateChange)
                self.similarTheredIsRunning = True
                self.newCherecterIspressed.connect(self.similarityThreadForOsk.newCharecterIsPressedStateChange)
                self.similarityThreadForOsk.start()
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
            self.similarityThreadForOsk = similarityThreadForOsk(englishWordSofar)
            self.similarityThreadForOsk.ruledOutSimiSignal.connect(self.ruledOutSimiStateChange)
            self.similarityThreadForOsk.mostMatchedWords.connect(self.addSimiWordsFunc)
            self.similarityThreadForOsk.similarTheredIsRunningSignal.connect(self.similarTheredIsRunningStateChange)
            self.similarTheredIsRunning = True
            self.newCherecterIspressed.connect(self.similarityThreadForOsk.newCharecterIsPressedStateChange)
            self.similarityThreadForOsk.start()

    def ruledOutSimiStateChange(self, state):
        self.ruledOutSimi = state
        self.similarTheredIsRunning = False
        
        # try:    
        #     self.similarityThreadForOsk.stop()
        # except Exception:
        #     pass 

    def initFunc(self, sig):
        self.ruledOut = False
        self.ruledOutSimi = False
        self.similarTheredIsRunning = False
        try:    
            self.similarityThreadForOsk.stop()
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
        # User32.SetWindowLongW(int(self.dockWidget.winId()), -20, 134217728)
        # self.dockWidget.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint)
        # User32.SetWindowLongW(int(self.dockWidget.winId()), -20, 134217728)
        # print(int(self.dockWidget.winId()))
        self.CloseButton.clicked.connect(lambda: self.close())
        self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        self.clicked = False
        self.WinOsk.clicked.connect(self.oenWinOsk)
        self.tabWidget.currentChanged.connect(self.tabChangedFunc)
        self.SFXcheckBox.clicked.connect(self.sfxStatechanged)
        
        # CurrentWord = ""
        self.RecomendationList = []
        self.RecomendationBtns = [self.RB1,self.RB2,self.RB3,self.RB4,self.RB5,self.RB6,self.RB7,self.RB8,self.RB9, self.RB10]
        self.numDic = {'1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯','0':'০',}

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

        self.pushButton_201.clicked.connect(self.spaceClicked)
        self.pushButton_198.clicked.connect(self.tabClicked)            
        self.pushButton_199.clicked.connect(self.BackSpaceClicked)
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
    
        # self.MouseListener = mouse.Listener(on_click = self.on_click)
        # self.MouseListener.start()
        # self.RestoreCharacPushButton.setVisible(False)
        # self.dockWidget.dockLocationChanged.connect(lambda:self.RestoreCharacPushButton.setVisible(True))

        self.BanglawordThread = BanglawordThread()
        self.BanglawordThread.matched_Word_signal.connect(self.populateWords)
        self.bangla_word_signal.connect(self.BanglawordThread.run)
        self.initBanglaThread_signal.connect(self.BanglawordThread.initFunc)
        self.BanglawordThread.start()

        self.loadCharacters()
        self.loadEmojies()

    # def RestoreCharac(self):
    #     self.dockWidget.show()
    #     self.restoreDockWidget(self.dockWidget)
    #     self.gridLayout_7.addWidget(self.dockWidget)
    #     self.RestoreCharacPushButton.setVisible(False)


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
                kb.tap(char)  
            else:
                kb.type(char)
                CurrentWord += char
                self.recomendFunc()

            self.initState()     
        elif self.BanglishCheckBox.isChecked() == True:
            self.sendBanglishFor(char) 
                
    def EnterClicked(self):
        kb.tap(Key.enter)
        self.initState()
    def deleteClicked(self):
        kb.tap(Key.delete)
        self.initState()
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

            # self.recomendFunc()
            self.initState()
        elif wordSofar != "":
            try:
                wordSofar = wordSofar[:-1]
            except Exception:
                wordSofar = "" 
                self.cleanRecomendations()


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
        print("in function")
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
        kb.type(char)
        if self.SFXcheckBox.isChecked() == True:
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            pass
        CurrentWord += char
        self.bangla_word_signal.emit(CurrentWord)

        
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

                chaParts = cha.split(",")

                emoji = chaParts[0]
                name = chaParts[1]

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



class listViewClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(listViewClass, self).__init__()
        uic.loadUi('.//Uis//Completor.ui', self)
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        User32.SetWindowLongW(int(self.winId()), -20, 134217728)

        self.pined = False
        self.PinPushButton.clicked.connect(self.pinStateChanged)
        # self.listWidget.itemClicked.connect(self.WordClicked)
        self.listWidget.setUniformItemSizes(True)
        self.matchedWords = []
        self.currentWords = []
        self.clicked = False
        self.comButtonsBlocked = False
        self.Doc_pad = Script_pad.Ui_nms_pad()

        self.SpellCheckPushButton.setToolTip("Spell Check")

        self.SpellCheckPushButton.clicked.connect(self.spellCheckFunc)
        self.threadRunning = False

        self.context_menu = QMenu(self.listWidget)
        self.context_menu.setTitle("conTitle")
        self.action1 = QAction("Action 1", self)
        self.action1.triggered.connect(self.action1_triggered)
        self.context_menu.addAction(self.action1)
        

        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.open_menu)
        # self.listWidget.installEventFilter(self)
    def open_menu(self, position):
        # indexes = self.listWidget.selectedIndexes()
        # print(indexes)
        # if len(indexes) > 0:
        #     self.context_menu.exec_(self.listWidget.viewport().mapToGlobal(position))

        self.index = self.listWidget.indexAt(position)
        # Select the item
        self.listWidget.setCurrentIndex(self.index)
        if self.index.isValid():
            print(self.context_menu.winId())
            self.context_menu.exec_(self.listWidget.viewport().mapToGlobal(position))


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
            self.PinPushButton.setText("📍")
        else:
            self.pined = False
            self.PinPushButton.setText("📌")

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
        while("" in words):
            words.remove("")
        self.listWidget.clear()
        self.listWidget.addItems(words)
        self.currentRow = 0
        self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 10 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth())   
        # self.GetCaretPosInWindow()
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
                if self.comButtonsBlocked == False:
                    try:
                        for i in [80, 72]: # 28 ,
                            kb2.block_key(i)
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
                        # for i in [28, 80, 72]:    
                        #     try:    
                        #         kb2.unblock_key(i)
                        #     except Exception as e:
                        #         # print(e)  
                        #         pass
                        for i in keysToBlock:
                            kb2.block_key(i)
                        self.comButtonsBlocked = False         
                except Exception as e:
                    pass 
        pass
    @QtCore.pyqtSlot(str)
    def changeTheme(self, theme):
        
        if theme == "green":
            self.listWidget.setStyleSheet('QListWidget{\n	font: 12pt "Kalpurush";\n	border-radius:2px;\n	background-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(2,200,255,255));\n	border: 2px solid rgb(0, 255, 0);\n}')
        if theme == "red":
            self.listWidget.setStyleSheet('QListWidget{\n	font: 12pt "Kalpurush";\n	border-radius:2px;\n	background-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(2,200,255,255));\n	border: 2px solid rgb(255, 0, 0);\n}')
        if theme == "blue":
            self.listWidget.setStyleSheet('QListWidget{\n	font: 12pt "Kalpurush";\n	border-radius:2px;\n	background-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(2,200,255,255));\n	border: 2px solid rgb(0, 0, 255);\n}')  
        if theme == "yellow":
            self.listWidget.setStyleSheet('QListWidget{\n	font: 12pt "Kalpurush";\n	border-radius:2px;\n	background-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(2,200,255,255));\n	border: 2px solid rgb(255, 255, 0);\n}')              
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
class Ui(QtWidgets.QMainWindow):
    word_signal = pyqtSignal(str, str, str)
    initThread_signal = pyqtSignal(str)

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
        self.application_menue.addAction(self.exit_menu)
        self.application_menue.addAction(self.Restart_menu)
        self.Ansi_ = QAction('Output as ANSI', self, checkable=True, checked=False)
        self.Ansi_.triggered.connect(self.Ansi)
        self.Unicode_ = QAction('Output as Unicode', self, checkable=True, checked=True)
        self.Unicode_.triggered.connect(self.Unicode)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.taking_commend = QAction('Take single Cdm.', self, checkable=True, checked=False)
        self.taking_commend.triggered.connect(self.Take_commend)
        self.taking_cmd = False 
        Speech_to_text_menu = self.Settings_menu.addMenu('Speech to text')
        Speech_to_text_menu.addAction(self.taking_commend)
        Speech_to_text_menu.addAction(self.Ansi_)
        Speech_to_text_menu.addAction(self.Unicode_)
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
        self.trackClipSetting = QSettings("TrackClip")
        
        self.VocabularyMeni = self.Settings_menu.addMenu('Vocabulary List')
        self.AddNewWordMenu = QAction('Add New Words', self)
        self.AddNewWordMenu.triggered.connect(self.ShowAddWordsClass)

        if bool(self.trackClipSetting.value('checked')) == True:
            try:
                # self.Track_clip_thread.start()  
                pass
            except Exception as e:
                print(e)    
        self.wordManagerMenu = QAction('Word Manager', self)
        self.wordManagerMenu.triggered.connect(self.ShowWordManager)
        self.VocabularyMeni.addAction(self.AddNewWordMenu)
        self.VocabularyMeni.addAction(self.wordManagerMenu)
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
        
        self.main_settings = QSettings("MainSettings")
        self.settingsGUIClass.AutoCloseCheckBox.stateChanged.connect(self.autoCloseBra)
        self.settingsGUIClass.UseAbrisCheckBox.stateChanged.connect(self.useAbries)
        try:
            self.settingsGUIClass.RunAtAtartUpCheckBox.setChecked(bool(self.main_settings.value("runAtStartUp")))  
            self.settingsGUIClass.AutoCloseCheckBox.setChecked(bool(self.main_settings.value("AutoCloseBrackets"))) 
            self.AutoCloseBra = bool(self.main_settings.value("AutoCloseBrackets"))
            self.settingsGUIClass.setChecked(bool(self.main_settings.value("UseAbries")))      
        except Exception as e:
            print(e)

        self.current_language = "English"
        self.Lang_Button.clicked.connect(self.update_lang) 

        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = ""
        self.shiftKeyBlocked = False
        self.keysBlocked = True
        
        self.converter_gui = Converter_for_main.Ui_converter()

        self.numDic = {'1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯','0':'০'}
        self.qoteDic = {'(':')', '[':']', '{':'}'}
        self.karList = ["া","ি","ী","ু","ূ","ৃ","ে","ৈ","ো","ৌ"]
        self.keysToBlock = [2,3,4,5,6,7,8,9,10,11,  16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,   44,45,46,47,48,49,50,  52]    
        self.keysToUnlock = [2,3,4,5,6,7,8,9,10,11,52]
        
        self.listClass = listViewClass()
        self.listClass.hide()

        self.oskClass = OSK_UI()
        
# osk class connectors ========================================================================>

        # self.oskClass.pushButton_33.clicked.connect(self.oskClass.BackSpaceClicked)

        self.oskClass.pushButton_33.clicked.connect(lambda: self.on_osk_press(str("key.backspace")))

        self.oskClass.pushButton_78.clicked.connect(lambda: self.on_osk_press(str("key.delete")))
        self.oskClass.pushButton_47.clicked.connect(self.oskClass.EnterClicked)
        self.oskClass.pushButton_64.clicked.connect(self.oskClass.tabClicked)
        self.oskClass.pushButton_19.clicked.connect(self.oskClass.escFunc)
        self.oskClass.pushButton_52.clicked.connect(lambda: self.oskClass.spaceClicked())
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
# /osk class connectors ========================================================================>
        self.Doc_pad = Script_pad.Ui_nms_pad()
        self.lastActiveWindow = ""
        self.firstTime = True

        
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
        self.listener.start()

        self.MouseListener = mouse.Listener(on_click = self.on_click)
        self.MouseListener.start()

        self.wordThread_ = wordThread()
        self.wordThread_.matched_Word_signal.connect(self.getRecomendedWords)
        self.wordThread_.acWordSignal.connect(self.AutoCompleate)
        self.wordThread_.hideSignal.connect(self.listClass.showHideFunc)
        self.wordThread_.themeSignal.connect(self.listClass.changeTheme)
        self.word_signal.connect(self.wordThread_.run)
        self.initThread_signal.connect(self.wordThread_.initFunc)
        # self.wordThread_.start()

        ahk.run_script(ahkScript, blocking=False)
        self.wordManagerClass = wordManagerClass()
        self.wordManagerClass.save_signal.connect(self.loadAbbribiations)

        self.loadAbbribiations()

        self.listClass.listWidget.itemClicked.connect(self.WordClickedMiddleFunc)
        self.autoCompletedWord = ""
    def BanglishCheckBoxStateChanged(self):
        if self.oskClass.BanglishCheckBox.isChecked() == True:
            self.oskClass.pushButton_52.setText("বাংলা")
        else:
            self.oskClass.pushButton_52.setText("English")
        self.initialize()  

    def autoCloseBra(self, state):
        self.main_settings.setValue("AutoCloseBrackets", bool(state))  
        self.AutoCloseBra = state
    def useAbries(self, state):
        self.main_settings.setValue("UseAbries", bool(state))  
        if state:
            self.loadAbbribiations()
        else:
            kb2.unhook_all()
            self.blockKeys()
        pass
    def AutoCompleate(self, theWord):
        global wordSofar
        if self.listClass.ACcheckBox.isChecked():
            self.listener.stop() 

            times_to_tap_backspace, restOfWord = self.smertCompletor(wordSofar, theWord) 
            for i in range(times_to_tap_backspace):
                kb.tap(Key.backspace)
            kb.type(restOfWord)

            self.autoCompletedWord = theWord
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
            self.listener.start() 
            
            # print(theWord)
        pass
    def smertCompletor(self, word_soFar, the_word):
        for i in range(len(the_word))[:]:
            if the_word[i] == word_soFar[i]:
                pass
            else:
                same_index = i
                break
        return len(word_soFar[same_index:]), the_word[same_index:]  
    def WordClickedMiddleFunc(self, item):
        # print(item.text())
        # self.WordClicked()
        global wordSofar
        selectedText = item.text()

        self.listener.stop()
        if selectedText[:len(wordSofar)] == wordSofar:
            kb.type(selectedText[len(wordSofar):])
        else:
            print("i am actually here")
            for i in range(len(wordSofar)):
                kb.tap(Key.backspace)
            kb.type(selectedText)      
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        self.listener.start() 

        initGlobal()
        self.listClass.showHideFunc("hide") 
    def WordClicked(self, item):    # this function is called when u select a word using keyboard
        global completorTraegered
        global wordSofar
        global CurrentWord
        # print("in this function")
        
        try:
            wordSelected = item

            if len(wordSofar) == 0 and len(item) > 1:
                c_wrd = CurrentWord
            else:
                c_wrd = wordSofar

            # print(wordSelected)
            # print(c_wrd)
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
            self.listClass.showHideFunc("hide")  
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

            for ab in abris[:]:
                if ab == "":
                    return
                parts = ab.split("::")
                if len(parts) == 0:
                    return
                kb2.add_abbreviation(parts[0], parts[1])   
        except Exception as e:
            self.showError(e)
        self.blockKeys()
    def blockKeys(self):
        if self.current_language == "Bangla":
            self.listener.stop()
            for i in self.keysToBlock:
                kb2.block_key(i)
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
            self.listener.start()
            self.listClass.hide()
            self.initialize()
    def trim(self, l):
        global wordSofar
        self.listener.stop()
        wordSofar = wordSofar[:-l]
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
            if any([self.oskClass.ctrlState, self.oskClass.altState, self.oskClass.winState]):
                kb.tap(key)  
                
            else:
                self.listener.stop()
                kb.type(key)
                if key in englishLatters:    
                    wordSofar += key
                # print(wordSofar)
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start()
            self.oskClass.initState()    
            return   
        if self.oskClass.BanglishCheckBox.isChecked() == True:
            if key in englishLatters:   
                # self.listener.stop()
                # print("I am still here")
                global completorTraegered
                completorTraegered = True
                self.convertTobangla(key) 
                completorTraegered = False

                # self.listClass.showHideFunc("hide")
                # self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                # self.listener.start() 
                # self.listClass.showHideFunc("hide") 
            else:
                self.listener.stop()
                kb.type(key)      
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
                self.listener.start() 
            self.oskClass.initState()   
        # self.on_press(key)
            # self.listClass.showHideFunc("hide")
        pass

    def on_press(self, key):
        # print(f"{key} =====")
        global wordSofar 
        global englishWordSofar
        global previous_word
        global formar_previous_word
        
        if self.AutoCloseBra:
            qote = (str(key)).replace("'", "")
            if qote in self.qoteDic:
                kb.release(Key.shift)
                kb.type(self.qoteDic[qote])
                kb.tap(Key.left)
                self.initialize()
                return
        
        
        if self.current_language == "English":
            return
        try: 
            if str(key) == "Key.shift": # and self.shiftKeyBlocked == False
                for i in self.keysToUnlock:
                    try: 
                        kb2.unblock_key(i)
                    except Exception:
                        pass
                self.shiftKeyBlocked = True
                
            # print(str(key))
            if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"] and self.keysBlocked == True: 
                kb2.unhook_all()
                self.keysBlocked = False
                self.initialize()
                return
            if self.keysBlocked == False:
                return        
            if str(key) == "'.'":
                kb.type("।")
                self.initialize()
                return
            if str(key) == "Key.space" or (str(key)).replace("'", "") in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "`", "~"]:
                self.initialize()
                self.initThread_signal.emit("init")
            if str(key) == "Key.backspace":
                if wordSofar != "":    
                    if len(wordSofar) > 1:   
                        wordSofar = wordSofar[:-1]
                        englishWordSofar = englishWordSofar[:-1]
                        self.word_signal.emit(wordSofar, englishWordSofar, "bangla")
                    else:
                        self.initialize() 
            if self.listClass.isHidden() == False:
                if str(key) == "Key.down":
                    if self.listClass.listWidget.currentRow() == -1 or self.listClass.listWidget.currentRow() == self.listClass.listWidget.count()-1:
                        self.listClass.listWidget.setCurrentRow(1)
                    else:
                        self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.currentRow()+1) 
                    try:
                        kb2.block_key(28)
                    except Exception as e:
                        pass    
                if str(key) == "Key.up":
                    if self.listClass.listWidget.currentRow() == 1:
                        self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.count()-1)
                    else:    
                        self.listClass.listWidget.setCurrentRow(self.listClass.listWidget.currentRow()-1)       
                # if str(key) == "Key.space":
                #     self.listClass.currentRow = 0
                #     self.listClass.populateWords([])
                if str(key) == "Key.enter":
                    if self.listClass.listWidget.currentRow() != -1:    
                        item = self.listClass.listWidget.currentItem()
                        self.WordClicked(item.text())
                        # initGlobal()
                        self.listClass.showHideFunc("hide")
            
            
            if completorTraegered == True:
                return
            
            self.convertTobangla(key)
            # print("I am being called") 
            self.word_signal.emit(wordSofar, englishWordSofar, "bangla")
        except Exception as e:
            # print(e)
            print(traceback.format_exc())
        pass
    def on_click(self, x, y, button, pressed):
        
        # cursor_info = GetCursorInfo()
        # if cursor_info:
        #     hwnd = WindowFromPoint((cursor_info[2][0], cursor_info[2][1]))
        #     print(hwnd)
        # print(self.listClass.context_menu.windowTitle())
        # print(GetWindowText(WindowFromPoint(GetCursorPos())))
        if GetWindowText(WindowFromPoint(GetCursorPos())) not in [self.listClass.windowTitle(), self.oskClass.windowTitle(), self.listClass.context_menu.windowTitle()]:
            self.lastActiveWindow = GetWindowText(WindowFromPoint(GetCursorPos()))
            self.initialize()

            

    def on_release(self, key):
        if self.current_language == "English":
            return
        
        if str(key) == "Key.shift":
            for i in self.keysToUnlock:
                kb2.block_key(i)
            self.shiftKeyBlocked = False    

        if str(key) in ["Key.cmd", "Key.ctrl_l", "Key.alt_l", "Key.ctrl_r", "Key.alt_r"]: # and keysBlocked == False
            for i in self.keysToBlock:    
                kb2.block_key(i)
            self.keysBlocked = True 
            if self.listClass.isHidden() == False:
                for i in [28, 72, 80]:
                    kb2.block_key(i)
    
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
        if stringKey == "a":
            if wordSofar == "":
                bnglaKey = "আ"
            elif previous_word == "a":
                bnglaKey = "্য"
            elif previous_word == formar_previous_word and previous_word != "" and previous_word in ["c", ]:
                self.trim(1)
                bnglaKey = "্যা"
            else:
                if wordSofar[-1] == "ং":
                    self.trim(1)
                    bnglaKey = "ঙা"
                else:
                    bnglaKey = "া"
        if stringKey == "A":
            bnglaKey = "আ"
        if stringKey == "b":
            if previous_word in ["b","r"]:
                bnglaKey= "্ব"
            else:
                bnglaKey= "ব"
        if stringKey == "c":
            if previous_word in ["c","h"]:
                bnglaKey = "্চ"
            elif previous_word in ["n","G"]:
                bnglaKey = "ঞ্চ"
                self.trim(1)
            else:
                bnglaKey= "চ"  
        if stringKey == "d":
            if previous_word in ["n","b", "d", "l", "k"]:
                bnglaKey = "্দ"    
            else:
                bnglaKey = "দ"    
        if stringKey == "D":
            if previous_word in ["n","D", "l"]:
                bnglaKey = "্ড"    
            else:
                bnglaKey = "ড"
        if stringKey == "e":
            if wordSofar == "":
                bnglaKey = "এ"
            elif previous_word == 't' and formar_previous_word == 'n':
                bnglaKey = "তে"
                self.trim(2)
            else:
                bnglaKey = "ে"
        if stringKey == "E":
            if wordSofar == "":
                bnglaKey = "ঈ"
            else:
                bnglaKey = "ী"
        if stringKey == "f" or stringKey == "F":
            bnglaKey = "ফ"
        if stringKey == "g":
            if previous_word == "n" or previous_word == "N":
                if previous_word == "n": 
                    bnglaKey= "ং"
                if previous_word == "N": 
                    bnglaKey= "ঙ"
                self.trim(1)
            elif previous_word == "r": 
                bnglaKey= "্গ"
            elif previous_word == "g":
                bnglaKey= "জ্ঞ" 
                self.trim(1)
            else: 
                bnglaKey= "গ" 
        if stringKey == "G":
            if previous_word == "N":
                bnglaKey= "ঞ" 
                self.trim(1) 
            else:
                bnglaKey= "ঘ" 
        if stringKey == "h":
            if previous_word == "K":
                bnglaKey = "্ষ"
            elif previous_word == "c":
                bnglaKey= "ছ" 
                self.trim(1)
            elif previous_word == "j":
                bnglaKey = "ঝ" 
                self.trim(1) 
            elif previous_word == "k": 
                if formar_previous_word == "k":
                    bnglaKey = "ষ"     
                else:
                    bnglaKey = "খ"
                    self.trim(1)    
            elif previous_word == "p":
                bnglaKey = "ফ"
                self.trim(1)  
            elif previous_word == "g":
                bnglaKey = "ঘ"
                self.trim(1)  
            elif previous_word == "d":
                if formar_previous_word == "g":
                    bnglaKey = "্ধ"
                    self.trim(1)
                else:
                    bnglaKey = "ধ"
                self.trim(1)  
            elif previous_word == "D":
                bnglaKey = "ঢ"
                self.trim(1)
            elif previous_word == "b":
                if formar_previous_word == "d":
                    bnglaKey = "্ভ"
                else:
                    bnglaKey = "ভ"
                self.trim(1)
            elif previous_word == "R":
                bnglaKey = "ঢ়"
                self.trim(1) 
            elif previous_word == "s":
                bnglaKey = "শ"
                self.trim(1)
            elif previous_word == "S":
                self.trim(1)
                bnglaKey = "ষ"
                
            elif previous_word == "t":
                bnglaKey = "থ"
                self.trim(1)  
            elif previous_word == "T":
                bnglaKey = "ঠ"
                self.trim(1)  
            elif previous_word == "v":
                pass
            else:
                bnglaKey = "হ" 
        if stringKey == "H":
            if previous_word == "K":
                bnglaKey = "্ষ"
            elif previous_word == "T":
                bnglaKey = "ৎ"
                self.trim(1)
        if stringKey == "i":
            if wordSofar == "" or wordSofar[-1] in self.karList or wordSofar[-1] in ["এ","ও","ঔ", "অ", "আ","উ","ই","ঊ", "ঋ", "ঐ", "ঔ"]:
                bnglaKey= "ই"
            elif previous_word == "r" and formar_previous_word == "r":
                bnglaKey= "ৃ"
                self.trim(3)
            elif previous_word == "o" or previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey= "ঐ"
                    self.trim(1)
                else:
                    bnglaKey= "ৈ"
            else:
                bnglaKey= "ি"
        if stringKey == "I":
            if previous_word == "o" or previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey= "ঐ"
                    self.trim(1)
                else:
                    bnglaKey= "ৈ"
            elif wordSofar == "" or wordSofar[-1] in self.karList:
                bnglaKey = "ঈ"    
            else:
                bnglaKey = "ী"
        if stringKey == "j":
            if previous_word == "n":
                bnglaKey= "ঞ্জ"
                self.trim(1)
            elif previous_word in ["j", "J"]:
                bnglaKey= "্জ" 
            else:
                bnglaKey= "জ"
        if stringKey == "J":
            bnglaKey= "ঝ"    
        if stringKey == "k":
            if previous_word in ["k", "K", "l", "s", "r"]:
                bnglaKey = "্ক"
            elif previous_word == "h" and formar_previous_word == "s":
                bnglaKey = "ষ্ক"
                self.trim(1)  
            elif previous_word == "n":
                bnglaKey = "ঙ্ক"
                self.trim(1)      
            elif previous_word == "g" and formar_previous_word == "N":
                bnglaKey = "্ক"
            else:
                bnglaKey = "ক"
        if stringKey == "K":
            bnglaKey = "খ"
        if stringKey == "l":
            if previous_word == "l":
                bnglaKey= "্ল"
            else:
                bnglaKey= "ল"         
        if stringKey == "m":
            if previous_word == "h":
                bnglaKey = "হ্ম"
                self.trim(1) 
            elif previous_word in ["d", "l", "n", "r", "s", "t", "g", "m"]:
                bnglaKey = "্ম" 
            else:
                bnglaKey = "ম" 
        if stringKey == "M":
            bnglaKey = "মো" 
        if stringKey == "n":
            # print(previous_word)
            if previous_word in ["n", "p", "t", "g", "h", "m", "s", "r"]:
                bnglaKey= "্ন"
            else:
                bnglaKey= "ন"      
        if stringKey == "N":
            if previous_word == "r":
                bnglaKey = "্ণ" 
            else:
                bnglaKey = "ণ" 
        if stringKey == "o":
            if previous_word == formar_previous_word != "": 
                if previous_word == "g":
                    bnglaKey = "্য"
                else:
                    self.trim(1) 
                    bnglaKey = "য"   
            elif wordSofar == "":
                bnglaKey = "অ"
            elif previous_word == "g" and formar_previous_word == "n":
                bnglaKey = "ঙ্গ"
                self.trim(1)  
            # elif previous_word == "h" and formar_previous_word == "r":   
            # elif previous_word == formar_previous_word and 
            elif previous_word in ["p", "s", "t", "T", "c", "d", "z", "m", "O", "k", "b", "n", "r", "g", "j", "l", "h", "y", "S"]: 
                previous_word = "o"
                pass 
            else:
                if wordSofar[-1] in self.karList:    
                    bnglaKey = "ো"
                else:    
                    bnglaKey = "ও"
        if stringKey == "O":
            if wordSofar == "":
                bnglaKey = "ও"
            else:
                bnglaKey = "ো"
        if stringKey in ["p", "P"] :
            if previous_word == "s":
                bnglaKey = "্প"
            else:
                bnglaKey = "প"
        if stringKey in ["q", "Q"]:
            bnglaKey = "ক"
        if stringKey == "r":
            if previous_word in ["t","b","k","f","g","h","j","c","d","n","p","s","v","T","D","z","F", "m"]:
                bnglaKey = "্র" 
            else:
                bnglaKey = "র"
        if stringKey == "R":
            if wordSofar == "":
                bnglaKey = "ঋ" 
            else:
                bnglaKey = "ড়"  
        if stringKey == "s":
            if previous_word == "r":
                bnglaKey = "্স" 
            elif previous_word == "H":
                bnglaKey = "্"
                self.trim(1)
            else:
                bnglaKey = "স"  
        if stringKey == "S":
            bnglaKey = "শ" 
        if stringKey == "t":
            if previous_word in ["n","t", "p", "r"]:
                bnglaKey = "্ত"
            elif previous_word == "k": 
                bnglaKey = "ক্ত"
                self.trim(1)
            elif previous_word == "s":
                bnglaKey = "স্ত"
                self.trim(1)
            else:
                bnglaKey = "ত"
        if stringKey == "T":
            # print(wordSofar)
            if previous_word in ["h", "k","l","n", "p", "s","T"] and formar_previous_word not in ["g"]:
                bnglaKey = "্ট"
            else:
                bnglaKey = "ট"
        if stringKey == "u":
            if previous_word in ["O", "o"]:
                bnglaKey = "ঔ"
                self.trim(1)  
            elif wordSofar == "":
                bnglaKey = "উ"  
            else:
                bnglaKey = "ু"      
        if stringKey == "U":
            if wordSofar == "":
                bnglaKey = "ঊ"
            elif previous_word == "O":
                if formar_previous_word == "":
                    bnglaKey = "ঔ"
                else:
                    bnglaKey = "ৌ"
                self.trim(1) 
            else:
                bnglaKey = "ূ"
        if stringKey in ["v", "V"] : 
            if previous_word in ["m", "d"]:
                bnglaKey = "্ভ"
            else:
                bnglaKey = "ভ"
        if stringKey in  ["w", "W"]:
            if wordSofar == "":
                bnglaKey = "ও"
            else:
                bnglaKey = "্ব"
        if stringKey in  ["y", "Y"]:
                bnglaKey = "য়"
        if stringKey == "z":
            if previous_word == "r":
                bnglaKey = "্য"
            else:
                bnglaKey = "য"
        if stringKey == "Z":
            bnglaKey== "্য"   
        if bnglaKey != "" or stringKey == "o":
            if self.lastActiveWindow in [self.Doc_pad.windowTitle()]:
                self.Doc_pad.activateWindow()
            kb.type(str(bnglaKey))
            
            wordSofar += str(bnglaKey)
            self.formar_previous_formar_previous_word = self.previous_formar_previous_word
            self.previous_formar_previous_word = formar_previous_word
            formar_previous_word = previous_word
            previous_word = stringKey
            englishWordSofar += stringKey
      
                
    def initialize(self):
        global wordSofar
        global englishWordSofar
        global previous_word
        global formar_previous_word
        global ruledOut 
        global CurrentWord
        CurrentWord = ""
        self.autoCompletedWord = ""
        previous_word = ""
        wordSofar = ""
        englishWordSofar = ""
        formar_previous_word = ""
        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = "" 
        ruledOut = False 
        self.listClass.initSelf()
        self.oskClass.cleanRecomendations()
    def rb1Clicked(self):
        self.WordClicked(str(self.oskClass.RB1.text()))
    def rb2Clicked(self):
        self.WordClicked(str(self.oskClass.RB2.text())) 
    def rb3Clicked(self):
        self.WordClicked(str(self.oskClass.RB3.text()))
    def rb4Clicked(self):
        self.WordClicked(str(self.oskClass.RB4.text()))  
    def rb5Clicked(self):
        self.WordClicked(str(self.oskClass.RB5.text()))    
    def rb6Clicked(self):
        self.WordClicked(str(self.oskClass.RB6.text()))  
    def rb7Clicked(self):
        self.WordClicked(str(self.oskClass.RB7.text())) 
    def rb8Clicked(self):
        self.WordClicked(str(self.oskClass.RB8.text()))    
    def rb9Clicked(self):
        self.WordClicked(str(self.oskClass.RB9.text()))
    def rb10Clicked(self):
        self.WordClicked(str(self.oskClass.RB10.text()))  
    
    def ShowWordManager(self):
        try:
            self.wordManagerClass.show()
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
    def ShowAddWordsClass(self):
        try:
            self.AddNewWordsClass = AddNewWordsClass()
            self.AddNewWordsClass.show()
        except Exception as e:
            self.showError(e)        
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
                
                self.main_settings.setValue("runAtStartUp", True)

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
            try:
                sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Modern UI Sound_01.wav', winsound.SND_FILENAME))
                sound_thread.start()
            except Exception:
                pass 
            
            self.Doc_pad.Show_self()

        except Exception as e: 
            self.showError(e)       
    def showSettings(self):
        self.settingsGUIClass.Show_settings()
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

        self.reactor_thread = ThreadClass(parent=None)
        self.reactor_thread.any_signal.connect(self.update_prograss)  
        self.reactor_thread.start()
        
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
                print('line 620')
                pass
            try:
                self.thread.any_signal.connect()
                self.thread.stop()
                self.reactor_thread.stop()
                self.Listining_label.setVisible(False)   
                self.Stop_btn.setVisible(False)
                self.Mic_btn.setVisible(True)
                self.Lang_Button.setVisible(True)
            except Exception as e:
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
            
            self.listener.stop()

            self.initialize()
            
            self.loadAbbribiations()

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
        
if __name__ == "__main__":
    print("application openning....")
    # multiprocessing.freeze_support()
    # ++++++++============================================================================ Recoarding volium
    # WM_APPCOMMAND = 0x319
    # APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a
    # APPCOMMAND_VOLUME_MIN = 0x09
    # win32api.SendMessage(-1, 0x319, 0x30292, APPCOMMAND_MICROPHONE_VOLUME_UP * 0x10000)

    
    # app = QApplication(sys.argv)
    # ex = Ui()
    # # # ex.show()
    # # ex.showMinimized()
    # ex.showNormal()
    # sys.exit(app.exec_())

    app = QApplication(sys.argv)
    ex = Ui()
    ex2 = Ui_Splash()
    ex.show()
    # ex2.show()
    sys.exit(app.exec_())