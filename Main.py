# -*- coding:utf-8 -*-

from glob import glob
import time
import keyboard as kb2
import speech_recognition as sr
from pynput.keyboard import Controller, Key
kb = Controller()
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QTimer, QSettings, QEasingCurve
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QApplication, QMessageBox, QGraphicsDropShadowEffect
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
import OSK
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
from win32gui import GetWindowText, GetCursorPos, WindowFromPoint, GetForegroundWindow, GetWindowRect, GetCaretPos
from AddNewWord import AddNewWordsClass
from WordManager import wordManagerClass
from LoadWords import wordsList,englaList,EnglishwordsList


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
ruledOut = False



def initGlobal():
    global previous_word 
    global formar_previous_word 
    global previous_formar_previous_word 
    global formar_previous_formar_previous_word 
    global wordSofar 
    global englishWordSofar 
    global shiftKeyBlocked 
    global keysBlocked
    global ruledOut
    
    previous_word = ""
    formar_previous_word = ""
    previous_formar_previous_word = ""
    formar_previous_formar_previous_word = ""
    wordSofar = ""
    englishWordSofar = ""
    shiftKeyBlocked = False
    keysBlocked = True
    ruledOut = False 


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

from pynput import keyboard

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
            # with open('.//Res//Recoard_settings.txt', "r") as RS:
            #     RS_pos = RS.read()
            # settings = (RS_pos.split('\n'))
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
                minimumSimi = 0.7
            else:
                minimumSimi = 0.7   
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
            if self.preWord != wordSofar and wordSofar not in ["", " "]:   
                self.newCherecterIspressed.emit(True)
                # self.newCharecterState = False
                
                self.matchedWords = []

                if self.ruledOut == False or len(englishWordSofar) < len(self.preWord):
                    self.loopThroughList(wordsList,wordSofar,englishWordSofar)
                    if len(self.matchedWords) == 0:
                        self.ruledOut = True

                if self.ruledOut == True and self.ruledOutEngla == False:
                    self.loopThroughList(englaList,wordSofar,englishWordSofar)
                    if len(self.matchedWords) == 0:
                        self.ruledOutEngla = True
                    else:    
                        self.themeSignal.emit("blue")


                if len(self.matchedWords) == 0 and self.ruledOutSimi == False:
                    self.startSimilarityThread(englishWordSofar, 'bangla')   

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
            if len(wordArray) == 1:
                continue
            banglaWord = wordArray[0]
            index = 0
            for wrd in wordArray[:]:
                if banglaWord in self.matchedWords:
                    break
                if index == 0 and wrd[:len(wordSofar)] == wordSofar : # and wrd not in self.matchedWords
                    self.matchedWords.append(banglaWord)
                    break
                elif (wrd[:len(englishWordSofar_local)]).lower() == (englishWordSofar_local).lower() and banglaWord not in self.matchedWords: # and wrd not in self.matchedWords
                    self.matchedWords.append(banglaWord)
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

    newCherecterIspressed = QtCore.pyqtSignal(bool)
    initSignal = QtCore.pyqtSignal(str)
    ruledOutSig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(wordThread, self).__init__()

        self.whileLoopThread = WhileloopThroughListThread()
        self.whileLoopThread.matchedWordsSignal.connect(self.addSimiWordsFunc)
        self.whileLoopThread.finished.connect(self.whileLoopThread.deleteLater)
        self.whileLoopThread.themeSignal.connect(self.emitTheme)
        self.initSignal.connect(self.whileLoopThread.initFunc)
        self.newCherecterIspressed.connect(self.whileLoopThread.newCharecterIsPressedStateChange)
        self.ruledOutSig.connect(self.whileLoopThread.initFunc)
        self.whileLoopThread.start()

    def run(self):
        if wordSofar in ["", " "]:
            return
        self.hideSignal.emit("show")    

    def dicThreadReturnFunc(self, matchedWords):
        self.matched_Word_signal.emit(matchedWords) 
        self.dicThreadIsRunning = False

    def addSimiWordsFunc(self, simiWords):
        self.matchedWords = []
        self.matchedWords.append(englishWordSofar)
        # self.matchedWords.append(wordSofar)
        for w in simiWords:
            self.matchedWords.append(w)
        self.matched_Word_signal.emit(self.matchedWords)     


    def emitTheme(self, theme):
        self.themeSignal.emit(theme)

    def initFunc(self, sig):
        self.initSignal.emit("hjh")
        self.themeSignal.emit("green")
 
       

class listViewClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(listViewClass, self).__init__()
        uic.loadUi('.//Uis//Completor.ui', self)
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        User32.SetWindowLongW(int(self.winId()), -20, 134217728)

        self.pined = False
        self.PinPushButton.clicked.connect(self.pinStateChanged)
        self.listWidget.itemClicked.connect(self.WordClicked)
        self.listWidget.setUniformItemSizes(True)
        self.matchedWords = []
        self.currentWords = []
        self.clicked = False
        self.comButtonsBlocked = False
        self.Doc_pad = Script_pad.Ui_nms_pad()

        self.SpellCheckPushButton.setToolTip("Spell Check")

        self.SpellCheckPushButton.clicked.connect(self.spellCheckFunc)
        self.threadRunning = False


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
        global wordSofar

        if wordSofar not in ["", " "]:
            self.showHideFunc("show")
            self.listWidget.clear()
            self.listWidget.addItems(words)
            self.currentRow = 0
            self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 10 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth())   
        else:
            self.showHideFunc("hide")

    @QtCore.pyqtSlot(list)
    def populateSimilarWords(self, simiWords):
        self.listWidget.addItems(simiWords)
        self.currentRow = 0
        self.listWidget.setFixedSize(self.listWidget.sizeHintForColumn(0) + 10 * self.listWidget.frameWidth(), self.listWidget.sizeHintForRow(0) * self.listWidget.count() + 2 * self.listWidget.frameWidth())   
    def initSelf(self):
        if self.isHidden() == False:    
            self.listWidget.clear()
            self.showHideFunc("hide")
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
    def on_press(self, key):
        if self.isHidden() == False:
            
            if str(key) == "Key.down":
                if self.listWidget.currentRow() == -1 or self.listWidget.currentRow() == self.listWidget.count()-1:
                    self.listWidget.setCurrentRow(1)
                else:
                    self.listWidget.setCurrentRow(self.listWidget.currentRow()+1) 
                try:
                    kb2.block_key(28)
                except Exception as e:
                    pass    
            if str(key) == "Key.up":
                if self.listWidget.currentRow() == 1:
                    self.listWidget.setCurrentRow(self.listWidget.count()-1)
                else:    
                    self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)       
            if str(key) == "Key.space":
                self.currentRow = 0
                self.populateWords([])
            if str(key) == "Key.enter":
                if self.listWidget.currentRow() != -1:    
                    self.WordClicked(self.listWidget.currentItem())
                    # initGlobal()
                    self.showHideFunc("hide")
                
    def WordClicked(self, item):
        global completorTraegered
        global wordSofar
        try:
            wordSelected = item.text()
            if wordSelected[:len(wordSofar)] == wordSofar:
                kb.type(wordSelected[len(wordSofar):])              
            elif len(wordSofar) == 1:
                keyList = [Key.shift, Key.left]
                for key in keyList:
                    kb.press(key)
                for key in keyList:
                    kb.release(key)
                kb.type(wordSelected)
            else:
                keyList = [Key.ctrl, Key.shift, Key.left]
                for key in keyList:
                    kb.press(key)
                for key in keyList:
                    kb.release(key)     
                completorTraegered = True
                kb.type(wordSelected)
                completorTraegered = False 
            initGlobal()
            self.showHideFunc("hide")  
        except Exception:
            pass
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
    # word_signal = pyqtSignal(str, str, str)
    # initThread_signal = pyqtSignal(str)

    # newCherecterIspressed = QtCore.pyqtSignal(bool)
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
        self.Conveter = self.Settings_menu.addAction('Unicode to Bijoy text conveter')
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
        self.Run_at_startUp = QAction('Run automatically at startup', self, checkable=True, checked=False)
        self.Run_at_startUp.triggered.connect(self.Run_startup_fun)
        self.Settings_menu.addAction(self.Run_at_startUp)
        if RKS_pos == "True":
            self.Run_at_startUp.setChecked(True) 
        if RKS_pos == "False":
            self.Run_at_startUp.setChecked(False)
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
        self.settingsGUIClass = Options_UI()     
        self.current_language = "English"
        self.Lang_Button.clicked.connect(self.update_lang) 

        self.previous_formar_previous_word = ""
        self.formar_previous_formar_previous_word = ""
        self.shiftKeyBlocked = False
        self.keysBlocked = True
        
        self.converter_gui = Converter_for_main.Ui_converter()

        self.numDic = {'1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯','0':'০'}
        self.karList = ["া","ি","ী","ু","ূ","ৃ","ে","ৈ","ো","ৌ"]
        self.keysToBlock = [2,3,4,5,6,7,8,9,10,11,  16,17,18,19,20,21,22,23,24,25,   30,31,32,33,34,35,36,37,38,   44,45,46,47,48,49,50,  52]    
        self.keysToUnlock = [2,3,4,5,6,7,8,9,10,11,52]
        
        self.listClass = listViewClass()
        self.listClass.hide()

        self.Doc_pad = Script_pad.Ui_nms_pad()
        self.lastActiveWindow = ""

        
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
        self.listener.start()

        print(self.listener.running)

        self.MouseListener = mouse.Listener(on_click = self.on_click)
        self.MouseListener.start()

        self.wordThread_ = wordThread()
        self.wordThread_.matched_Word_signal.connect(self.listClass.populateWords)
        self.wordThread_.hideSignal.connect(self.listClass.showHideFunc)
        self.wordThread_.themeSignal.connect(self.listClass.changeTheme)
        # self.word_signal.connect(self.wordThread_.run)
        # self.initThread_signal.connect(self.wordThread_.initFunc)

        ahk.run_script(ahkScript, blocking=False)
        self.wordManagerClass = wordManagerClass()
        self.wordManagerClass.save_signal.connect(self.loadAbbribiations)

        self.loadAbbribiations()


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
        # print(self.listener.running)

        wordSofar = wordSofar[:-l]
        for i in range(l):  
            kb.tap(Key.backspace)
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)    
        self.listener.start()
        # print(self.listener.running)

    def on_press(self, key):
        # print(f"{key} =====")
        global englishWordSofar
        global wordSofar
        global previous_word
        global formar_previous_word
        global previous_formar_previous_word
        try: 
            if str(key) == "Key.shift":
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
                # self.initThread_signal.emit("init")
            if str(key) == "Key.backspace":
                if wordSofar != "":    
                    if len(wordSofar) > 1:   
                        wordSofar = wordSofar[:-1]
                        englishWordSofar = englishWordSofar[:-1]
                    else:
                        self.initialize() 
            if str(key) in ["Key.down", "Key.up", "Key.enter"]:
                self.listClass.on_press(key)
  
            bnglaKey = ""
            stringKey = (str(key)).replace("'", "")

            if completorTraegered == True:
                return
            
            if stringKey in self.numDic:
                kb.type(self.numDic[stringKey])
                self.initialize()
                return
            if stringKey == "a":
                if wordSofar == "":
                    bnglaKey = "আ"
                elif previous_word == "a":
                    bnglaKey = "্য"
                elif previous_word == formar_previous_word and previous_word != "":
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
                # if self.lastActiveWindow in [self.Doc_pad.windowTitle()]:
                #     self.Doc_pad.activateWindow()
                kb.type(str(bnglaKey))
                
                wordSofar += str(bnglaKey)
                
                formar_previous_word = previous_word
                previous_word = stringKey
                englishWordSofar += stringKey

                # self.word_signal.emit('')
                
                 
        except Exception as e:
            # print(e)
            print(traceback.format_exc())
        pass
    def on_click(self, x, y, button, pressed):
        if GetWindowText(WindowFromPoint(GetCursorPos())) != "Nms_completer":
            self.lastActiveWindow = GetWindowText(WindowFromPoint(GetCursorPos()))
            self.initialize()
            pass
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
    def initialize(self):
        initGlobal()
        self.listClass.initSelf()
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
                oskClass = OSK.OSK_UI()
                oskClass.show()
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
    def Run_startup_fun(self):
        try:
            if self.Run_at_startUp.isChecked() == True:
                
                creat_shortcut()
                with open('.//Res//Run_at_startup.txt', "w") as RKS:
                    RKS.write("True")
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
        except Exception:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"
                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Kontho")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.setText("Something went wrong!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
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

            oskClass = OSK.OSK_UI()
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
    # ex.show()
    ex2.show()
    sys.exit(app.exec_())