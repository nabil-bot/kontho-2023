# -*- coding:utf-8 -*-
# from sub_file import recognizer
# from logging import exception
# from _typeshed import Self
import difflib
import PyQt5
from PyQt5 import uic, QtCore
# from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog,QColorDialog, QMainWindow, QMessageBox, QPushButton, QSlider, QScrollArea,QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem, QTextEdit, QFontDialog 
from PyQt5.QtGui import QIntValidator, QColor, QFont  
from PyQt5.QtCore import QSettings
# from PyQt5.QtWidgets.QTableWidge import QtWidgets
from PyQt5.QtCore import QItemSelectionModel
import sys
import io
import os
from PyQt5 import QtCore
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
from pynput.keyboard import Controller
keyboard = Controller()
import wave
import contextlib
import speech_recognition as sr
# from PyQt5.QtCore import (Qt, pyqtSignal)
import pyperclip as pc
# import concurrent.futures
from PyQt5 import uic
import threading
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import pydub.silence as pys
import time
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5 import QtCore, QtMultimedia
from PyQt5 import QtCore, QtGui, QtWidgets
import winsound
# import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

import sys
import subprocess
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

from PyQt5 import QtCore, QtWidgets

 
def start_sig():
    try:
        # sound = AudioSegment.from_wav('.//SFX//Start.wav')
        # play(sound)
        winsound.PlaySound('.//SFX//Start.wav', winsound.SND_FILENAME)
    except Exception:
        pass
def stop_sig():
    try:
        # sound = AudioSegment.from_wav('.//SFX//Finish.wav')
        # play(sound)
        winsound.PlaySound('.//SFX//Finish.wav', winsound.SND_FILENAME)
    except Exception:
        print('in singnal exception 1')
        pass     
def TimeStamp(total_milisecs):

    seconds = int(total_milisecs/1000)    # this convert miliseconds to seconds

    miliseconds = ((str((total_milisecs/1000) - seconds)).replace('0.', ''))[0:3] # 

    if seconds > 59:
        if seconds < 3600: 
            hrs = '00'
            mins = (seconds//60)
            second = seconds - (mins * 60)  
            if second < 10:
                if second == 0:
                    second = "00"    
                else:
                    second = f'0{second}'
            else:    
                second = str(second)  
            if mins < 10:
                if mins == 0:
                    mins = '00'
                else:
                    mins = f'0{mins}'
            else:
                mins = str(mins)

        else:
            hrs = seconds // 3600
            left_secs = seconds - (hrs * 3600)
            mins = left_secs // 60
            secs = left_secs - (mins * 60)
            if hrs < 10:
                if hrs == 0:
                    hrs = "00"
                else:
                    hrs = f'0{hrs}'
            else:
                hrs = str(hrs)        
            if mins < 10:
                if mins == 0:
                    mins = '00'
                else:
                    mins = f'0{mins}'
            else:
                mins = str(mins)        
            if secs < 10:
                if secs == 0:
                    secs = '00'
                    second = secs
                else:
                    secs = f'0{secs}'  
                    second = secs
                    
            else:
                secs = str(secs)  
                second = secs

            # self.duration = f'{hrs} hrs {mins} mins {secs} secs'
    else:
        hrs = '00'
        mins = '00'
        if seconds < 10:
            if seconds == 0:
                second = "00"    
            else:
                second = f'0{seconds}'
        else:    
            second = str(seconds)

    

    return (str(hrs+':'+mins+':'+second+','+miliseconds))        
def match_target_amplitude(sound, target_dBFS): # normalyzation 
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)
def similarity_ration_btween(first_string, second_string):
    temp = difflib.SequenceMatcher(None,first_string , second_string)
    return temp.ratio()

class ThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(str)
    time_stamp_list = QtCore.pyqtSignal(list, list)
    nonsilent_data_list = QtCore.pyqtSignal(list)
    recognized_para = QtCore.pyqtSignal(str)
    matched_sentence_signal = QtCore.pyqtSignal(list, list, list, list, list)

    def __init__(self, lang, path, delete_chuncks, for_srt_generator, min_silence_len, silence_thresh, sentances, skip_recognation,match_sequence,Minimum_matched_ratio, FileFormat, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
        self.sentances_ = sentances
        self.sentances = []
        for s in self.sentances_:
            self.sentances.append(s.replace("\n", " "))
        self.skip_recog = skip_recognation
        self.lang = lang
        self.path = path
        self.generate_srt_type = for_srt_generator
        self.delete_chanks = delete_chuncks
        self.min_silence_len = min_silence_len
        self.silence_thresh = silence_thresh
        self.match_sequence = match_sequence
        self.Minimum_matched_ratio = Minimum_matched_ratio
        self.FileFormat = FileFormat
    def run(self):
        if self.FileFormat == "wav":    
            song = AudioSegment.from_wav(self.path)
        if self.FileFormat == "mp3":    
            song = AudioSegment.from_mp3(self.path)    
        if self.generate_srt_type == True:    
            nonsilent_data = detect_nonsilent(song, self.min_silence_len, self.silence_thresh, seek_step=1)
            if self.generate_srt_type == True:
                self.nonsilent_data_list.emit(nonsilent_data)
        time_stamps = []
        if self.skip_recog == True and self.generate_srt_type == True:
            print('in if statement 1')
            text = ""
            len_of_non_silent_data = len(nonsilent_data)
            for i in range(len(nonsilent_data)):
                time_range = nonsilent_data[i]
                timeStamp = ''
                for chunk in time_range:
                    if time_range.index(chunk) == 0:
                        timeStamp += TimeStamp(chunk)
                    else:
                        timeStamp += f' --> {TimeStamp(chunk)}'  
                progress = i / len_of_non_silent_data * 100
                progress_sognal = f'progress_: {round(progress)}'
                
                self.any_signal.emit(progress_sognal)
                
                time_stamps.append(timeStamp)
            # self.any_signal.emit(str(f'{time_stamps}|-|{self.sentances}'))  
            self.time_stamp_list.emit(time_stamps , self.sentances)        # just scripted sentence
        
        if self.skip_recog == False and self.generate_srt_type == True and self.match_sequence == False:
            print('in if statement 2')
            chunks = split_on_silence(song, self.min_silence_len, self.silence_thresh)
            try:
                os.mkdir('audio_chunks')
            except(FileExistsError):
                pass
            len_of_chuncks = len(chunks)
            os.chdir('audio_chunks')
            text = ""
            recognized_sentences = []
            c = 0
            for chunk in chunks:
                chunk_silent = AudioSegment.silent(duration = 4)
                audio_chunk = chunk
                audio_chunk.export("./chunk{0}.wav".format(c), bitrate ='192k', format ="wav")
                c += 1   
                progress = c / len_of_chuncks * 100
                progress_sognal = f'progress_: {round(progress)}'
                self.any_signal.emit(progress_sognal)
    
            r = sr.Recognizer()
            for i in range((len_of_chuncks))[:]:
                filename = 'chunk'+str(i)+'.wav'
                try:
                    
                    with sr.AudioFile(filename) as source:  
                        try:
                            audio_listened = r.listen(source)
                            rec = r.recognize_google(audio_listened, language= self.lang) 
                        except Exception as e:
                            rec = 'could not recognized!'
                            print(e)
                    if self.generate_srt_type == False:
                        recognized_sentences.append(rec)
                    else:
                        time_range = nonsilent_data[i]
                        timeStamp = ''
                        for chunk in time_range:
                            if time_range.index(chunk) == 0:    
                                timeStamp += TimeStamp(chunk)
                            else:
                                timeStamp += f' --> {TimeStamp(chunk)}'    
                        
                        # text += f'{i+1}\n{timeStamp}\n{rec}\n\n' 
                        recognized_sentences.append(rec)
                        time_stamps.append(timeStamp)            
                    progress = i / len_of_chuncks * 100
                    progress_sognal = f'progress_: {round(progress)}'
                    self.any_signal.emit(progress_sognal)
                    time.sleep(0.5)
                        
                except Exception as e:
                    print(e)

            self.time_stamp_list.emit(time_stamps , recognized_sentences)
            if self.delete_chanks == True:    
                for i in range(c):
                    filename = 'chunk'+str(i)+'.wav'
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(f'in error :{e}')

        if self.skip_recog == False and self.generate_srt_type == False:

            
            chunks = split_on_silence(song, self.min_silence_len, self.silence_thresh)
            try:
                os.mkdir('audio_chunks')
            except(FileExistsError):
                pass
            len_of_chuncks = len(chunks)
            os.chdir('audio_chunks')
            text = ""
            recognized_sentences = []
            c = 0
            for chunk in chunks:
                chunk_silent = AudioSegment.silent(duration = 4)
                audio_chunk = chunk
                audio_chunk.export("./chunk{0}.wav".format(c), bitrate ='192k', format ="wav")
                c += 1   
                progress = c / len_of_chuncks * 100
                progress_sognal = f'progress_: {round(progress)}'
                self.any_signal.emit(progress_sognal)
    
            r = sr.Recognizer()
            for i in range((len_of_chuncks))[:]:
                filename = 'chunk'+str(i)+'.wav'
                try:
                    
                    with sr.AudioFile(filename) as source:  
                        try:
                            audio_listened = r.listen(source)
                            rec = r.recognize_google(audio_listened, language= self.lang) 
                            
                        except Exception as e:
                            rec = 'could not recognized!'
                            print(e)
                    
                    text += f'{rec}\n'
                               
                    progress = i / len_of_chuncks * 100
                    progress_sognal = f'progress_: {round(progress)}'
                    self.any_signal.emit(progress_sognal)
                    time.sleep(0.5)
                        
                except Exception as e:
                    print(e)

            self.any_signal.emit(text)        
            
            if self.delete_chanks == True:    
                for i in range(c):
                    filename = 'chunk'+str(i)+'.wav'
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(f'in error :{e}')                

        if self.match_sequence == True and self.generate_srt_type == True:
            
            # audio chuncks ==================================================================
            chunks = split_on_silence(song, self.min_silence_len, self.silence_thresh)
            try:
                os.mkdir('audio_chunks')
            except(FileExistsError):
                pass
            len_of_chuncks = len(chunks)
            os.chdir('audio_chunks')
            text = ""
            recognized_sentences = []
            matches = []
            c = 0
            for chunk in chunks:
                chunk_silent = AudioSegment.silent(duration = 4)
                audio_chunk = chunk
                audio_chunk.export("./chunk{0}.wav".format(c), bitrate ='192k', format ="wav")
                c += 1   
                progress = c / len_of_chuncks * 100
                progress_sognal = f'progress_: {round(progress)}'
                self.any_signal.emit(progress_sognal)
            # audio chuncks ==================================================================
            
            r = sr.Recognizer()
            for i in range((len_of_chuncks))[:]:
                filename = 'chunk'+str(i)+'.wav'
                try:
                    
                    with sr.AudioFile(filename) as source:  
                        try:
                            audio_listened = r.listen(source)
                            rec = r.recognize_google(audio_listened, language= self.lang) 
                        except Exception as e:
                            rec = 'could not recognized!'
                            print(e)

                    time_range = nonsilent_data[i]
                    timeStamp = ''
                    for chunk in time_range:
                        if time_range.index(chunk) == 0:    
                            timeStamp += TimeStamp(chunk)
                        else:
                            timeStamp += f' --> {TimeStamp(chunk)}'    
                    
                    # text += f'{i+1}\n{timeStamp}\n{rec}\n\n' 
                    recognized_sentences.append(rec)
                    time_stamps.append(timeStamp)            
                    progress = i / len_of_chuncks * 100
                    progress_sognal = f'progress_: {round(progress)}'
                    self.any_signal.emit(progress_sognal)
                    time.sleep(0.5)
                except Exception as e:
                    print(e)

            matched_caption_and_similrity_list = self.match_finder(recognized_sentences, self.sentances, self.Minimum_matched_ratio)
            matched_captions = matched_caption_and_similrity_list[0]
            similarity_by_caption = matched_caption_and_similrity_list[1]


            self.matched_sentence_signal.emit(time_stamps, recognized_sentences, self.sentances, matched_captions, similarity_by_caption)
            if self.delete_chanks==True:
                for i in range(c):
                    filename = 'chunk'+str(i)+'.wav'
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(f'in error :{e}')
    def stop(self):
        self.is_running = False
        self.terminate()
    def match_finder(self, recognized_sentence_list, scriped_sentence_list, minimum_match_ratio):
        row_count = len(recognized_sentence_list) # this is recognized caption list number
        r = 0
        r_s = 0
        matched_caption_list = []
        similarity_list = []
        for i in range(row_count)[:]:
            matched_caption_list.append(' ')
            similarity_list.append(' ')

        while True:
            recognized_text = recognized_sentence_list[r]
            try:
                script_sentence = scriped_sentence_list[r_s]
                if script_sentence[0] == ' ':
                    script_sentence = script_sentence[1:-1]
            except Exception:
                script_sentence = ' '
            similarity = similarity_ration_btween(recognized_text, script_sentence)
            if similarity > minimum_match_ratio:
                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(script_sentence.format(0, 0))))
                similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')
                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))
                matched_caption_list[r] = script_sentence
                similarity_list[r] = similarity_str

                r += 1
                r_s += 1

                progress = r / row_count * 100
                progress_sognal = f'pg2: {round(progress)}'
                self.any_signal.emit(progress_sognal)
            else:
                words_in_recognized_sentence = recognized_text.split(' ')
                words_in_sentence = script_sentence.split(' ')
                word_num_in_sentence = len(words_in_sentence)

                custom_sentence = ''
                most_matched_sentence = ''

                most_matched_ration = 0.0000000000000000000000
                for w_i in range(word_num_in_sentence):
                    custom_sentence += f'{words_in_sentence[w_i]} '
                    if custom_sentence[0] == ' ':
                        custom_sentence = custom_sentence[1:-1]
                    similarity = similarity_ration_btween(recognized_text, custom_sentence)

                    if similarity > most_matched_ration:
                        most_matched_ration = similarity
                        most_matched_sentence = custom_sentence
                if most_matched_ration > minimum_match_ratio:
                    # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                    similarity_str = (int(most_matched_ration * 100))
                    #
                    # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                    matched_caption_list[r] = most_matched_sentence
                    similarity_list[r] = similarity_str

                    r += 1

                    progress = r / row_count * 100
                    progress_sognal = f'pg2: {round(progress)}'
                    self.any_signal.emit(progress_sognal)

                    rest_of_the_sentence = script_sentence.replace(most_matched_sentence, '')

                    next_recognized_sentence = recognized_sentence_list[r]

                    similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                    if similarity > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                        similarity_str = (int(similarity * 100))

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = rest_of_the_sentence
                        similarity_list[r] = similarity_str

                        r += 1
                        r_s += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)
                else:
                    most_matched_sentence = ''
                    most_matched_ration = 0.0000000000000000000000

                    for sen in range(row_count):
                        try:
                            script_sentence = scriped_sentence_list[sen]
                        except Exception:
                            script_sentence = ''
                        similarity = similarity_ration_btween(recognized_text, script_sentence)
                        if similarity > most_matched_ration:
                            most_matched_ration = similarity
                            most_matched_sentence = script_sentence
                    if most_matched_ration > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                        similarity_str = int(most_matched_ration * 100)

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = most_matched_sentence
                        similarity_list[r] = similarity_str

                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)

                    elif most_matched_ration > 0.4:
                        the_hole_sentence = most_matched_sentence

                        words_in_sentence = most_matched_sentence.split(' ')
                        word_num_in_sentence = len(words_in_sentence)

                        custom_sentence = ''
                        most_matched_sentence = ''

                        most_matched_ration = 0.0000000000000000000000
                        for w_i in range(word_num_in_sentence):
                            custom_sentence += f'{words_in_sentence[w_i]} '
                            if custom_sentence[0] == ' ':
                                custom_sentence = custom_sentence[1:-1]
                            similarity = similarity_ration_btween(recognized_text, custom_sentence)

                            if similarity > most_matched_ration:
                                most_matched_ration = similarity
                                most_matched_sentence = custom_sentence
                        if most_matched_ration > minimum_match_ratio:
                            # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                            similarity_str = int(most_matched_ration * 100)

                            # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                            matched_caption_list[r] = most_matched_sentence
                            similarity_list[r] = similarity_str

                            r += 1

                            rest_of_the_sentence = the_hole_sentence.replace(most_matched_sentence, '')

                            next_recognized_sentence = recognized_sentence_list[r]

                            similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                            if similarity > minimum_match_ratio:

                                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                                similarity_str = int(similarity * 100)

                                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                                matched_caption_list[r] = rest_of_the_sentence
                                similarity_list[r] = similarity_str

                                r += 1
                                r_s += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                self.any_signal.emit(progress_sognal)
                            else:
                                r += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                self.any_signal.emit(progress_sognal)
                        else:
                            r += 1

                            progress = r / row_count * 100
                            progress_sognal = f'pg2: {round(progress)}'
                            self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)

            if r == row_count:
                break
        return matched_caption_list, similarity_list
    def match_finder_reserved(self, recognized_sentence_list, scriped_sentence_list, minimum_match_ratio):
        row_count = len(recognized_sentence_list) # this is recognized caption list number
        r = 0
        r_s = 0
        matched_caption_list = []
        similarity_list = []
        for i in range(row_count)[:]:
            matched_caption_list.append(' ')
            similarity_list.append(' ')

        while True:
            recognized_text = recognized_sentence_list[r]
            try:
                script_sentence = scriped_sentence_list[r_s]
                if script_sentence[0] == ' ':
                    script_sentence = script_sentence[1:-1]
            except Exception:
                script_sentence = ' '
            similarity = similarity_ration_btween(recognized_text, script_sentence)
            if similarity > minimum_match_ratio:
                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(script_sentence.format(0, 0))))
                similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')
                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))
                matched_caption_list[r] = script_sentence
                similarity_list[r] = similarity_str

                r += 1
                r_s += 1

                progress = r / row_count * 100
                progress_sognal = f'pg2: {round(progress)}'
                self.any_signal.emit(progress_sognal)
            else:
                words_in_recognized_sentence = recognized_text.split(' ')
                words_in_sentence = script_sentence.split(' ')
                word_num_in_sentence = len(words_in_sentence)

                custom_sentence = ''
                most_matched_sentence = ''

                most_matched_ration = 0.0000000000000000000000
                for w_i in range(word_num_in_sentence):
                    custom_sentence += f'{words_in_sentence[w_i]} '
                    if custom_sentence[0] == ' ':
                        custom_sentence = custom_sentence[1:-1]
                    similarity = similarity_ration_btween(recognized_text, custom_sentence)

                    if similarity > most_matched_ration:
                        most_matched_ration = similarity
                        most_matched_sentence = custom_sentence
                if most_matched_ration > minimum_match_ratio:
                    # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                    similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')
                    #
                    # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                    matched_caption_list[r] = most_matched_sentence
                    similarity_list[r] = similarity_str

                    r += 1

                    progress = r / row_count * 100
                    progress_sognal = f'pg2: {round(progress)}'
                    self.any_signal.emit(progress_sognal)

                    rest_of_the_sentence = script_sentence.replace(most_matched_sentence, '')

                    next_recognized_sentence = recognized_sentence_list[r]

                    similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                    if similarity > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                        similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = rest_of_the_sentence
                        similarity_list[r] = similarity_str

                        r += 1
                        r_s += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)
                else:
                    most_matched_sentence = ''
                    most_matched_ration = 0.0000000000000000000000

                    for sen in range(row_count):
                        try:
                            script_sentence = scriped_sentence_list[sen]
                        except Exception:
                            script_sentence = ''
                        similarity = similarity_ration_btween(recognized_text, script_sentence)
                        if similarity > most_matched_ration:
                            most_matched_ration = similarity
                            most_matched_sentence = script_sentence
                    if most_matched_ration > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                        similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = most_matched_sentence
                        similarity_list[r] = similarity_str

                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)

                    elif most_matched_ration > 0.4:
                        the_hole_sentence = most_matched_sentence

                        words_in_sentence = most_matched_sentence.split(' ')
                        word_num_in_sentence = len(words_in_sentence)

                        custom_sentence = ''
                        most_matched_sentence = ''

                        most_matched_ration = 0.0000000000000000000000
                        for w_i in range(word_num_in_sentence):
                            custom_sentence += f'{words_in_sentence[w_i]} '
                            if custom_sentence[0] == ' ':
                                custom_sentence = custom_sentence[1:-1]
                            similarity = similarity_ration_btween(recognized_text, custom_sentence)

                            if similarity > most_matched_ration:
                                most_matched_ration = similarity
                                most_matched_sentence = custom_sentence
                        if most_matched_ration > minimum_match_ratio:
                            # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                            similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')

                            # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                            matched_caption_list[r] = most_matched_sentence
                            similarity_list[r] = similarity_str

                            r += 1

                            rest_of_the_sentence = the_hole_sentence.replace(most_matched_sentence, '')

                            next_recognized_sentence = recognized_sentence_list[r]

                            similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                            if similarity > minimum_match_ratio:

                                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                                similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')

                                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                                matched_caption_list[r] = rest_of_the_sentence
                                similarity_list[r] = similarity_str

                                r += 1
                                r_s += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                self.any_signal.emit(progress_sognal)
                            else:
                                r += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                self.any_signal.emit(progress_sognal)
                        else:
                            r += 1

                            progress = r / row_count * 100
                            progress_sognal = f'pg2: {round(progress)}'
                            self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        self.any_signal.emit(progress_sognal)

            if r == row_count:
                break
        return matched_caption_list, similarity_list    
class Ui_Text_genarator(QMainWindow):
    def __init__(self):
        super(Ui_Text_genarator, self).__init__() 
        uic.loadUi('.//Uis//A_to_T.ui', self) 
        self.progressBar.setValue(0)

        # self.deleteLater()

        self.path = ''
        self.error = False
        self.filterTypes = 'SRT files (*.srt) ;; Text Document (*.txt) ;; Rich Text Document (*.rtf)'
        self.srttb_types = 'Srt Table File (*.srttb;;Text Document (*.txt))'
        self.Cancel_pushButton.setVisible(False)
        self.PlayPathButton.clicked.connect(self.play_path_func)
        self.Cancel_pushButton.clicked.connect(self.stopThread)
        self.Copy_file_pathpushButton.clicked.connect(self.copy_path)
        self.Open_Audio_pushButton.clicked.connect(self.Open_file)
        self.Clear_pushButton.clicked.connect(self.clear)
        self.Language_comboBox.currentIndexChanged.connect(self.lang_changed)
        self.Generate_pushButton.setEnabled(False)
        self.Save_pushButton.setEnabled(False)
        self.Generate_pushButton.clicked.connect(self.generate)
        self.Save_pushButton.clicked.connect(self.save_text_as)
        self.Copy_pushButton.clicked.connect(self.copy_text)
        self.groupBox_4.setVisible(False)
        self.dockWidget.setVisible(False)
        self.already_showing_edit_group = False
        self.horizontalSlider.setStyleSheet("background: transparent")
        self.horizontalSlider.setMaximum(101)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setTickInterval(5)
        self.horizontalSlider.setTickPosition(QSlider.TicksAbove)
        with open('.//Res//current_lang_in_g.txt', "r") as CLG:
            CLG_pos = CLG.read()
        self.Language_comboBox.setCurrentText(CLG_pos)
        self.initGUI(True)
        self.JusttextEdit_2.setVisible(False)
        self.horizontalSlider.setTickPosition(QSlider.TicksAbove)
        self.ChunckscheckBox.setChecked(True)
        self.horizontalSlider.valueChanged.connect(self.update_scilence_threshhold)
        self.spinBox.setValue(500)
        self.horizontalSlider.setValue(25)
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setMinimum(15)

        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setValue(70)
        self.horizontalSlider_2.valueChanged.connect(self.update_min_matched_ratio)
        self.horizontalSlider_2.setTickPosition(QSlider.TicksAbove)
        self.actionRemove_Similarity_Column.triggered.connect(self.RemoveColumn)
        self.setGeometry(100, 100, 601, 277)
        self.onlyInt = QIntValidator()
        self.lineEdit.setValidator(self.onlyInt)
        self.lineEdit.textChanged.connect(self.update_threshhold)
        self.lineEdit.setText('-25')
        self.pushButton.clicked.connect(self.reset)
        self.TextFilepushButton.clicked.connect(self.OpenRefarenceFile)
        self.filterTypes = 'Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Rich Text Document (*.rtf);; Html (*.html);; SRT (*.srt)'
        self.Split_pushButton.clicked.connect(self.split_func)
        self.SaveSettingspushButton.clicked.connect(self.SaveFunc)
        self.settings = QSettings('WAV to Text')
        self.HomePagePushButton.clicked.connect(self.home_page)
        self.TextPagePushButton.clicked.connect(self.text_page)
        self.Up_pushbutton.clicked.connect(self.up_button_clicked)
        self.DownPushButton.clicked.connect(self.down_button_clicked)
        self.Make_room_pushbutton.clicked.connect(self.make_room_func)
        
        # self.RemovePushButton.clicked.connect(self.remove_func)
        self.RemovePushButton.clicked.connect(self.remove_func)

        self.actionReset.triggered.connect(self.reset_func)

        self.Edit_pushButton.clicked.connect(self.edit_func)
        self.tableWidget.selectionModel().selectionChanged.connect(self.selection_changed_function)
        self.comit_save_pushButton.clicked.connect(self.commit_save)
        self.Cancel_pushButton_2.clicked.connect(self.cancel_commit)
        self.fontComboBox.currentIndexChanged.connect(self.change_font)
        self.player = QMediaPlayer()
        self.playing_audio = False
        self.player.durationChanged.connect(self.duration_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.media_slider_horizontalSlider.sliderMoved.connect(self.set_position)
        self.Playback_speed_comboBox.currentIndexChanged.connect(self.chage_playback_speed)
        self.play_audio_pushButton.clicked.connect(self.play_func)
        self.current_row_num = 0
        self.Split_pushButton.setEnabled(False)
        self.Skip_checkBox.setEnabled(False)
        self.checkBox.stateChanged.connect(self.enable_text_tab)
        
        self.actionExport_Table.triggered.connect(self.save_as_table)

        self.open_table__pushButton.clicked.connect(self.open_table)
        self.path = 0
        self.match_sequence_checkBox.stateChanged.connect(self.match_sequence_func)
        self.copy_text_file_pushButton.clicked.connect(self.copy_text_file_path)
 #       self.tableWidget.selectionModel().selectionChanged.connect(self.onSelectionCHanged)
        self.actionWave.triggered.connect(self.Open_file)
        self.actionReference_file.triggered.connect(self.OpenRefarenceFile)
        self.actionSrt_Table_file.triggered.connect(self.open_table)
        self.groupBox_9.setEnabled(False)
        try:
            self.spinBox.setValue(self.settings.value('MinSilLen'))
            self.lineEdit.setText(self.settings.value('SilThrDb'))
            self.checkBox.setChecked(bool(self.settings.value('IncludeTimeStamp')))
            self.tabWidget.setTabEnabled(1, bool(self.settings.value('IncludeTimeStamp')))
            self.horizontalSlider_2.setValue((float(self.settings.value('Match_ratio'))*100))
            self.Minimum_matched_ratio_lineEdit.setText(self.settings.value('Match_ratio'))
            
            if bool(self.settings.value('IncludeTimeStamp')) == True: 
                self.tableWidget.setVisible(True)
                self.tableWidget.setVisible(True)
                self.Edit_pushButton.setVisible(True)
                self.Up_pushbutton.setVisible(True)
                self.DownPushButton.setVisible(True)
                self.Make_room_pushbutton.setVisible(True)
                self.RemovePushButton.setVisible(True)
                self.groupBox_5.setVisible(True)
            else:
                self.tableWidget.setVisible(False)
                self.Edit_pushButton.setVisible(False)
                self.Up_pushbutton.setVisible(False)
                self.DownPushButton.setVisible(False)
                self.Make_room_pushbutton.setVisible(False)
                self.RemovePushButton.setVisible(False)
                self.groupBox_5.setVisible(False)   

            self.ChunckscheckBox.setChecked(bool(self.settings.value('Delete_chuncks')))
            self.Sentance_spliter_lineEdit.setText(self.settings.value('Spliter'))
            font = self.settings.value('font')
            self.textEdit.setStyleSheet(f'font: 12pt "{font}";')
            self.tableWidget.setStyleSheet(f'font: 12pt "{font}";\n\nbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(117, 189, 255, 255), stop:1 rgba(132, 198, 255, 255));')
            pass
        except Exception as e:
            print(e)

        self.previous_fontSize = self.fontsizecomboBox.currentText()
        self.SRTfilecheckBox.stateChanged.connect(self.srt_file_checkbox_func)
        self.SimpleTextcheckBox.stateChanged.connect(self.simpletextsrtfunc)
        self.UseCustomFontcheckBox.stateChanged.connect(self.useCustomFontFunc)
        self.ChooseFontCheckBox.stateChanged.connect(self.chooseFontFunc)
        self.fontComboBox_2.currentIndexChanged.connect(self.fontChanged)
        self.fontComboBox_2.setEnabled(False)
        self.previousFont = self.fontComboBox_2.currentText()
        self.ItaliccheckBox.stateChanged.connect(self.sendItalicFunc)
        self.BoldcheckBox.stateChanged.connect(self.sendBoldFunc)
        self.FontSizecheckBox.stateChanged.connect(self.useCustomFontSize)
        self.fontsizecomboBox.setEnabled(False)
        self.IncreaseFontsizePushButton.setEnabled(False)
        self.decricePushbutton.setEnabled(False)
        self.fontsizecomboBox.currentIndexChanged.connect(self.fontChangedFunc)
        self.IncreaseFontsizePushButton.clicked.connect(self.increaseFontSize)
        self.decricePushbutton.clicked.connect(self.dcreaseFontSize)
        self.CustomColorcheckBox.stateChanged.connect(self.CustomColorFunc)
        self.colorCodelineEdit.setText('#FFFFFF')
        self.previousColorCode = self.colorCodelineEdit.text()
        self.colorCodelineEdit.textChanged.connect(self.colorCodeChangedFunc)

        self.colorCodelineEdit.setEnabled(False)
        self.colorPickerpushButton.setEnabled(False)
        self.BlackpushButton.setEnabled(False)
        self.WhitePushButton.setEnabled(False)

        self.WhitePushButton.clicked.connect(self.whitePushButoonClicked)
        self.BlackpushButton.clicked.connect(self.blackPushButoonClicked)
        self.colorPickerpushButton.clicked.connect(self.colorDialog)
        self.SaveSettingsPushButton.clicked.connect(self.saveExportSetting)
        self.SetAsSavedPushButton.clicked.connect(self.setAsSavedFunc)
        self.frame_3.setEnabled(False)
        self.tableWidget.cellDoubleClicked.connect(self.edit_func)
        self.SaveExportPushButton.clicked.connect(self.saveExportFunction)
        self.RColumncheckBox.stateChanged.connect(self.RCChecked)
        self.SColumnCheckBox.stateChanged.connect(self.SColumnCheckBoxFunction)
        self.MColumnCheckBox.stateChanged.connect(self.MColumnCheckBoxFunction)
        self.Save_pushButton.setVisible(False)
        self.OpenTXTButton.clicked.connect(self.open_txt)
        self.paste_pushButton.clicked.connect(self.paste_func)
        self.actionFill_Empty_lines_with_recognized_sentences.triggered.connect(self.fillWithRecognizedSentence)
        self.actionQuick_Export_as_SRT_file.triggered.connect(self.QuickExportAsSrt)
        # self.OpenWith("C:/Users/ui/Desktop/TaxForTits.mp3", "C:/Users/ui/3D Objects/Kontho reboot/ghjj.txt")
    def QuickExportAsSrt(self):
        try:
            colum_count = self.tableWidget.columnCount() 
            if colum_count == 5:    
                if self.RColumncheckBox.isChecked() == True:
                    column = 1
                if  self.SColumnCheckBox.isChecked() == True:
                    column = 2
                if  self.MColumnCheckBox.isChecked() == True:
                    column = 3
            if colum_count == 4:
                column = 3
            if colum_count == 2:
                column = 1      
            
            row_count = self.tableWidget.rowCount() 
            for no in range(row_count):
                try:    
                    timeStamp = self.tableWidget.item(no, 0).text()
                except Exception:
                    timeStamp = ""    
                try:    
                    caption = self.tableWidget.item(no, column).text()
                except Exception:
                    caption = ""    
                caption = caption.replace('  ', ' ')
                if len(caption) > int(self.cherecter_spinBox.value()):
                    words = caption.split(' ')
                    words_num = len(caption.split(' '))
                    one_line_words_num = round(words_num/2)
                    custom_caption = ''
                    for n in range(one_line_words_num-1):
                        custom_caption += f'{words[n]} '
                    rest_of_the_caption =  caption.replace(custom_caption, '')   
                    caption = f'{custom_caption}\n{rest_of_the_caption}'

                if self.UseCustomFontcheckBox.isChecked() == True:
                    textToExport += f'{no}\n{timeStamp}\n{self.StartLineEdit.text()}{caption}{self.EndLineEdit.text()}\n\n'
                else:
                    textToExport += f'{no}\n{timeStamp}\n{caption}\n\n'
            pass
        except Exception:
            pass
    def fillWithRecognizedSentence(self):
        try:    
            row_count = self.tableWidget.rowCount() 
            for no in range(row_count):
                matched_text = self.tableWidget.item(no, 3).text() 
                if matched_text == "" or matched_text == " ":
                    recognized_sentence = self.tableWidget.item(no, 1).text()
                    item = QTableWidgetItem(recognized_sentence.format(0, 0))
                    self.tableWidget.setItem(no,3, item)
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(str(e))
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()             
    def open_txt(self):
        try:    
            os.startfile(self.reffa_path)
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(e)
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()     
    def play_path_func(self):
        try:    
            os.startfile(self.path)
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(str(e))
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()         
    def MColumnCheckBoxFunction(self, state):
        if state == 2:
            self.RColumncheckBox.setChecked(False)  
            self.SColumnCheckBox.setChecked(False)      
    def SColumnCheckBoxFunction(self, state):
        if state == 2:
            self.RColumncheckBox.setChecked(False)
            self.self.MColumnCheckBox.setChecked(False)        
    def RCChecked(self, state):
        if state == 2:
            self.SColumnCheckBox.setChecked(False) 
            self.MColumnCheckBox.setChecked(False)       
    def saveExportFunction(self):
        if self.groupBox_11.isVisible() == True:
            if self.RColumncheckBox.isChecked() == False and self.SColumnCheckBox.isChecked() == False and self.MColumnCheckBox.isChecked() == False:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 10pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Please select a column to export!")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_() 
                return   
        textToExport = ''
        row_count = self.tableWidget.rowCount()  
        colum_count = self.tableWidget.columnCount() 
        if colum_count == 5:    
            if self.RColumncheckBox.isChecked() == True:
                column = 1
            if  self.SColumnCheckBox.isChecked() == True:
                column = 2
            if  self.MColumnCheckBox.isChecked() == True:
                column = 3
        if colum_count == 4:
            column = 3
        if colum_count == 2:
            column = 1      
        if self.SimpleTextcheckBox.isChecked() == True:
            for row in range(row_count)[:]:
                textToExport += f'{self.tableWidget.item(row, column).text()}\n'
        if self.SRTfilecheckBox.isChecked() == True:
            for no in range(row_count):
                try:    
                    timeStamp = self.tableWidget.item(no, 0).text()
                except Exception:
                    timeStamp = ""    
                try:    
                    caption = self.tableWidget.item(no, column).text()
                except Exception:
                    caption = ""    
                caption = caption.replace('  ', ' ')
                if len(caption) > int(self.cherecter_spinBox.value()):
                    words = caption.split(' ')
                    words_num = len(caption.split(' '))
                    one_line_words_num = round(words_num/2)
                    custom_caption = ''
                    for n in range(one_line_words_num-1):
                        custom_caption += f'{words[n]} '
                    rest_of_the_caption =  caption.replace(custom_caption, '')   
                    caption = f'{custom_caption}\n{rest_of_the_caption}'

                if self.UseCustomFontcheckBox.isChecked() == True:
                    textToExport += f'{no}\n{timeStamp}\n{self.StartLineEdit.text()}{caption}{self.EndLineEdit.text()}\n\n'
                else:
                    textToExport += f'{no}\n{timeStamp}\n{caption}\n\n'
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as',
            '',
            filter='SRT (*.srt);;Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Rich Text Document (*.rtf);; Html (*.html)'
        )
        if path:
            try:
                with io.open(path, 'w', encoding="utf-8") as f:
                    f.write(textToExport)

                self.path = path
                self.explore(self.path)
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 10pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong! 3\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()             
    def OpenWith(self, audioFilePath, ScriptFilePath):
        self.show()
        self.Open_file(audioFilePath)
        self.OpenRefarenceFile(ScriptFilePath)
        self.split_func()
        self.match_sequence_checkBox.setChecked(True)
        pass
    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    def setAsSavedFunc(self):
        self.ChooseFontCheckBox.setChecked(bool(self.settings.value('ChossFontCheckBox')))  
        self.FontSizecheckBox.setChecked(bool(self.settings.value('FontSizeCheckBox')))
        self.CustomColorcheckBox.setChecked(bool(self.settings.value('FontColorCheckBox')))
        self.ItaliccheckBox.setChecked(bool(self.settings.value('ItalicCheckBox')))
        self.BoldcheckBox.setChecked(bool(self.settings.value('BoldCheckBox')))

        self.fontComboBox_2.setCurrentText(self.settings.value('fontName'))    
        self.fontsizecomboBox.setCurrentText(self.settings.value('fontSize')) 
        self.colorCodelineEdit.setText(self.settings.value('ColorCode')) 

        self.StartLineEdit.setText(self.settings.value('StartLineEdit'))
        self.EndLineEdit.setText(self.settings.value('EndLineEdit'))

        self.updateTextPreview()    
    def saveExportSetting(self):
        self.settings.setValue('ChossFontCheckBox', self.ChooseFontCheckBox.isChecked())
        self.settings.setValue('FontSizeCheckBox', self.FontSizecheckBox.isChecked())
        self.settings.setValue('FontColorCheckBox', self.CustomColorcheckBox.isChecked())
        self.settings.setValue('ItalicCheckBox', self.ItaliccheckBox.isChecked())
        self.settings.setValue('BoldCheckBox', self.BoldcheckBox.isChecked())
        
        self.settings.setValue('fontName', self.fontComboBox_2.currentText())
        self.settings.setValue('fontSize', self.fontsizecomboBox.currentText())
        self.settings.setValue('ColorCode', self.colorCodelineEdit.text())

        self.settings.setValue('StartLineEdit', self.StartLineEdit.text())
        self.settings.setValue('EndLineEdit', self.EndLineEdit.text())
    def colorDialog(self):
        color = QColorDialog.getColor()
        if color:    
            self.colorCodelineEdit.setText(color.name())
    def blackPushButoonClicked(self):
        self.colorCodelineEdit.setText('#000000')
        self.updateTextPreview()    
    def whitePushButoonClicked(self):
        self.colorCodelineEdit.setText('#FFFFFF')
        self.updateTextPreview()    
    def colorCodeChangedFunc(self):
        current_text = self.StartLineEdit.text()     
        previousColorCodeSignal = f'color="{self.previousColorCode}"'
        currentColorCodeSignal =  f'color="{self.colorCodelineEdit.text()}"'
        signal_toSent = current_text.replace(previousColorCodeSignal, currentColorCodeSignal)   
        self.StartLineEdit.setText(((signal_toSent).replace(' >', '>')).replace('  ', ' '))      
        self.previousColorCode = self.colorCodelineEdit.text()
        try:    
            self.updateTextPreview()    
        except Exception:
            pass
    def CustomColorFunc(self, state):
        if state == 2:
            self.colorCodelineEdit.setEnabled(True)
            self.colorPickerpushButton.setEnabled(True)
            self.BlackpushButton.setEnabled(True)
            self.WhitePushButton.setEnabled(True)

            if self.colorCodelineEdit.text() == "":
                self.colorCodelineEdit.setText('#FFFFFF')
            color_code = self.colorCodelineEdit.text()
            current_text = self.StartLineEdit.text()     
            colorCodeSignal = f'<font color="{color_code}"'
            signal_toSent = current_text.replace('<font', colorCodeSignal)   
            self.StartLineEdit.setText(((signal_toSent).replace(' >', '>')).replace('  ', ' ')) 
            self.updateTextPreview()    

        else:
            self.colorCodelineEdit.setEnabled(False)
            self.colorPickerpushButton.setEnabled(False)
            self.BlackpushButton.setEnabled(False)
            self.WhitePushButton.setEnabled(False)

            color_code = self.colorCodelineEdit.text()
            current_text = self.StartLineEdit.text()     
            colorCodeSignal = f'color="{color_code}"'
            signal_toSent = current_text.replace(colorCodeSignal, '')   
            self.StartLineEdit.setText(((signal_toSent).replace(' >', '>')).replace('  ', ' '))       
    def dcreaseFontSize(self):
        current_size = int(self.fontsizecomboBox.currentText())
        increasedSize= str(current_size - 1)
        self.fontsizecomboBox.setCurrentText(increasedSize)
        self.fontChangedFunc()  
    def increaseFontSize(self):
        current_size = int(self.fontsizecomboBox.currentText())
        increasedSize= str(current_size + 1)
        self.fontsizecomboBox.setCurrentText(increasedSize)
        self.fontChangedFunc()         
    def fontChangedFunc(self):
        current = self.StartLineEdit.text()
        previousFontSizeSignal = f'size="{self.previous_fontSize}"'
        currentFontSizeSignal = f'size="{self.fontsizecomboBox.currentText()}"'
        signal_tosend = current.replace(previousFontSizeSignal, currentFontSizeSignal)
        self.StartLineEdit.setText(signal_tosend)
        self.previous_fontSize = self.fontsizecomboBox.currentText()
        self.updateTextPreview()    
    def useCustomFontSize(self, state):
        if state == 2:
            self.fontsizecomboBox.setEnabled(True)
            self.IncreaseFontsizePushButton.setEnabled(True)
            self.decricePushbutton.setEnabled(True)  

            current = self.StartLineEdit.text()  
            signal_to_send = f'<font size="{self.fontsizecomboBox.currentText()}"'
            custom_signal = ((current.replace('<font', signal_to_send)).replace(' >', '>')).replace('  ', ' ') 
            self.StartLineEdit.setText(custom_signal)
            self.updateTextPreview()    

        else:
            self.fontsizecomboBox.setEnabled(False)
            self.IncreaseFontsizePushButton.setEnabled(False)
            self.decricePushbutton.setEnabled(False)

            current = self.StartLineEdit.text()  
            signal_to_send = f'size="{self.fontsizecomboBox.currentText()}"'
            custom_signal = ((current.replace(signal_to_send, '')).replace(' >', '>')).replace('  ', ' ') 
            self.StartLineEdit.setText(custom_signal)     
    def sendBoldFunc(self, state):
        if state == 2:
            current = self.StartLineEdit.text()  
            customSigStart = f"<b>{current}"
            self.StartLineEdit.setText((customSigStart.replace(' >', '>')).replace('  ', ' ')) 

            current = self.EndLineEdit.text()  
            
            customSig2 = f'{current}</b>'
            self.EndLineEdit.setText(customSig2.replace(' >', '>'))
            self.updateTextPreview()    
        else:
            current = self.StartLineEdit.text()  
            customSigStart = current.replace('<b>', '') 
            self.StartLineEdit.setText((customSigStart.replace(' >', '>')).replace('  ', ' ')) 

            current = self.EndLineEdit.text()  
            
            customSig2 = current.replace('</b>', '')
            self.EndLineEdit.setText(customSig2) 
            self.updateTextPreview()    
    def sendItalicFunc(self, state):
        if state == 2:
            current = self.StartLineEdit.text()  
            customSigStart = f"<i>{current}"
            self.StartLineEdit.setText((customSigStart.replace(' >', '>')).replace('  ', ' ')) 
            current = self.EndLineEdit.text()    
            customSig2 = f'{current}</i>'
            self.EndLineEdit.setText(customSig2.replace(' >', '>'))
            self.updateTextPreview()    
        else:
            current = self.StartLineEdit.text()  
            customSigStart = current.replace('<i>', '') 
            self.StartLineEdit.setText((customSigStart.replace(' >', '>')).replace('  ', ' ')) 

            current = self.EndLineEdit.text()  
            
            customSig2 = current.replace('</i>', '')
            self.EndLineEdit.setText(customSig2)
            self.updateTextPreview()    
    def fontChanged(self):
        current = self.StartLineEdit.text()
        font = self.fontComboBox_2.currentText()
        fontSignal = f'{font}'
        sendSignal = current.replace(self.previousFont, fontSignal)   
        self.StartLineEdit.setText((sendSignal.replace('  ', ' ')).replace(' >', '>'))   
        self.previousFont = self.fontComboBox_2.currentText()
        self.updateTextPreview()    
    def chooseFontFunc(self, state):
        if state == 2:
            current = self.StartLineEdit.text()
            font = self.fontComboBox_2.currentText()
            fontSignal = f'<font face="{font}"'
            sendSignal = current.replace('<font', fontSignal)   
            self.StartLineEdit.setText((sendSignal.replace('  ', ' ')).replace(' >', '>'))
            self.fontComboBox_2.setEnabled(True) 

            self.updateTextPreview()    
        else:
            current = self.StartLineEdit.text()
            font = self.fontComboBox_2.currentText()
            fontSignal = f'face="{font}"'
            sendSignal = current.replace(fontSignal, '')   
            self.StartLineEdit.setText((sendSignal.replace('  ', ' ')).replace(' >', '>')) 
            self.fontComboBox_2.setEnabled(False)
            
            current_font = 'MS Shell Dig 2'
            font_size = self.fontsizecomboBox.currentText()
            font = QtGui.QFont(current_font, int(font_size))
            font.setBold(self.BoldcheckBox.isChecked())
            font.setItalic(self.ItaliccheckBox.isChecked())
    def useCustomFontFunc(self, state):
        if state == 2:
            self.groupBox_9.setEnabled(True) 
            self.frame_3.setEnabled(True) 
            self.StartLineEdit.setText('<font>')
            self.EndLineEdit.setText('</font>') 
            self.updateTextPreview()    
        else:
            self.groupBox_9.setEnabled(False)
            self.plainTextEdit.setEnabled(False)  
            self.frame_3.setEnabled(False) 
    def updateTextPreview(self):
        current_font = self.fontComboBox_2.currentText()
        font_size = self.fontsizecomboBox.currentText()
        colorCode = self.colorCodelineEdit.text()
        font = QFont(current_font, int(font_size))
        if self.BoldcheckBox.isChecked() == True:
            bold_status = 75
        else:
            bold_status = ' '
        if self.ItaliccheckBox.isChecked() == True:
            italic_status = 'italic'
        else:
            italic_status = ' '       
        # styleSheet = f'font: {bold_status} {italic_status} {font_size}pt "{current_font}";color:{colorCode}"'
        self.plainTextEdit.setStyleSheet(f'font: {bold_status} {italic_status} {font_size}pt {current_font};color:{colorCode};background:transparent')
    def srt_file_checkbox_func(self, state):
        if state == 2:    
            self.groupBox_8.setEnabled(True)
            self.SimpleTextcheckBox.setChecked(False)
        else:
            self.groupBox_8.setEnabled(False)
    def simpletextsrtfunc(self, state):
        if state == 2:
            self.SRTfilecheckBox.setChecked(False)   
            self.groupBox_8.setEnabled(False)         
    def update_min_matched_ratio(self):
        value_int = (self.horizontalSlider_2.value())/100
        self.Minimum_matched_ratio_lineEdit.setText(f'{value_int}')
    def call_function(self):
        self.tableWidget.setColumnCount(5)
        recognized_sentence_list = []
        scriped_sentence_list = []
        row_count = self.tableWidget.rowCount()
        for i in range(row_count)[:]:
            recognized_text = self.tableWidget.item(i, 1).text()
            try:
                script_sentence = self.tableWidget.item(i, 2).text()
                if script_sentence[0] == ' ':
                    script_sentence = script_sentence[1:-1]
            except Exception:
                script_sentence = ' '
            recognized_sentence_list.append(recognized_text)
            scriped_sentence_list.append(script_sentence)

        returned_list = self.match_finder(recognized_sentence_list, scriped_sentence_list, 0.70) # call the function ++++++++
        matched_captions = returned_list[0]
        similarity_list = returned_list[1]
        for i in range(row_count)[:]:
            self.tableWidget.setItem(i,3, (QTableWidgetItem(matched_captions[i].format(0, 0))))
            self.tableWidget.setItem(i,4, (QTableWidgetItem(similarity_list[i].format(0, 0))))
        return
    def match_finder(self, recognized_sentence_list, scriped_sentence_list, minimum_match_ratio):
        row_count = len(recognized_sentence_list) # this is recognized caption list number
        r = 0
        r_s = 0
        matched_caption_list = []
        similarity_list = []
        for i in range(row_count)[:]:
            matched_caption_list.append(' ')
            similarity_list.append(' ')

        while True:
            recognized_text = recognized_sentence_list[r]
            try:
                script_sentence = scriped_sentence_list[r_s]
                if script_sentence[0] == ' ':
                    script_sentence = script_sentence[1:-1]
            except Exception:
                script_sentence = ' '
            similarity = similarity_ration_btween(recognized_text, script_sentence)
            if similarity > minimum_match_ratio:
                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(script_sentence.format(0, 0))))
                similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')
                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))
                matched_caption_list[r] = script_sentence
                similarity_list[r] = similarity_str

                r += 1
                r_s += 1

                progress = r / row_count * 100
                progress_sognal = f'pg2: {round(progress)}'
                # self.any_signal.emit(progress_sognal)
            else:
                words_in_recognized_sentence = recognized_text.split(' ')
                words_in_sentence = script_sentence.split(' ')
                word_num_in_sentence = len(words_in_sentence)

                custom_sentence = ''
                most_matched_sentence = ''

                most_matched_ration = 0.0000000000000000000000
                for w_i in range(word_num_in_sentence):
                    custom_sentence += f'{words_in_sentence[w_i]} '
                    if custom_sentence[0] == ' ':
                        custom_sentence = custom_sentence[1:-1]
                    similarity = similarity_ration_btween(recognized_text, custom_sentence)

                    if similarity > most_matched_ration:
                        most_matched_ration = similarity
                        most_matched_sentence = custom_sentence
                if most_matched_ration > minimum_match_ratio:
                    # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                    similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')
                    #
                    # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                    matched_caption_list[r] = most_matched_sentence
                    similarity_list[r] = similarity_str

                    r += 1

                    progress = r / row_count * 100
                    progress_sognal = f'pg2: {round(progress)}'
                    # self.any_signal.emit(progress_sognal)

                    rest_of_the_sentence = script_sentence.replace(most_matched_sentence, '')
                    if rest_of_the_sentence[0] == ' ':
                        rest_of_the_sentence = rest_of_the_sentence[1:-1]

                    next_recognized_sentence = recognized_sentence_list[r]

                    similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                    if similarity > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                        similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = rest_of_the_sentence
                        similarity_list[r] = similarity_str

                        r += 1
                        r_s += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        # self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        # self.any_signal.emit(progress_sognal)
                else:
                    most_matched_sentence = ''
                    most_matched_ration = 0.0000000000000000000000
                    for sen in range(row_count):
                        try:
                            script_sentence = scriped_sentence_list[sen]
                        except Exception:
                            script_sentence = ''
                        similarity = similarity_ration_btween(recognized_text, script_sentence)
                        if similarity > most_matched_ration:
                            most_matched_ration = similarity
                            most_matched_sentence = script_sentence
                    if most_matched_ration > minimum_match_ratio:
                        # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                        similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')

                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        matched_caption_list[r] = most_matched_sentence
                        similarity_list[r] = similarity_str

                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        # self.any_signal.emit(progress_sognal)

                    elif most_matched_ration > 0.4:
                        the_hole_sentence = most_matched_sentence

                        words_in_sentence = most_matched_sentence.split(' ')
                        word_num_in_sentence = len(words_in_sentence)

                        custom_sentence = ''
                        most_matched_sentence = ''

                        most_matched_ration = 0.0000000000000000000000
                        for w_i in range(word_num_in_sentence):     # starting from the start
                            custom_sentence += f'{words_in_sentence[w_i]} '
                            if custom_sentence[0] == ' ':
                                custom_sentence = custom_sentence[1:-1]
                            similarity = similarity_ration_btween(recognized_text, custom_sentence)

                            if similarity > most_matched_ration:
                                most_matched_ration = similarity
                                most_matched_sentence = custom_sentence
                        if most_matched_ration > minimum_match_ratio:
                            # self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                            similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')

                            # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                            matched_caption_list[r] = most_matched_sentence
                            similarity_list[r] = similarity_str

                            r += 1

                            rest_of_the_sentence = the_hole_sentence.replace(most_matched_sentence, '')

                            next_recognized_sentence = recognized_sentence_list[r]

                            similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                            if similarity > minimum_match_ratio:

                                # self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                                similarity_str = ((str(similarity * 100))[0:3]).replace('.', '')

                                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                                matched_caption_list[r] = rest_of_the_sentence
                                similarity_list[r] = similarity_str

                                r += 1
                                r_s += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                # self.any_signal.emit(progress_sognal)
                            else:
                                r += 1

                                progress = r / row_count * 100
                                progress_sognal = f'pg2: {round(progress)}'
                                # self.any_signal.emit(progress_sognal)
                        else:
                            
                            # most_matched_sentence = ''

                            # most_matched_ration = 0.0000000000000000000000

                            # # my letest experiment (reverst list match)====================================
                            # reversed_words = script_sentence.split(' ')
                            # reversed_words.reverse()
                            # for r in range(len(words_in_sentence)):
                            #     word = words_in_sentence[r]
                            #     R_word = reversed_words[r]
                            #     try:    
                            #         r_word_index = words_in_sentence.index(R_word)
                            #     except Exception:
                            #         try:
                            #             r_word_index = words_in_sentence.index(R_word+1)
                            #         except Exception:
                            #             continue               
                            #     custom_sentence_word_list = words_in_sentence[r_word_index:]
                            #     custom_sentence = ''
                            #     for w in custom_sentence_word_list:
                            #         custom_sentence += f'{w} '
                            #         similarity = similarity_ration_btween(recognized_text, custom_sentence)
                            #         if similarity > most_matched_ration:
                            #             most_matched_ration = similarity
                            #             most_matched_sentence = custom_sentence
                            # if most_matched_ration > minimum_match_ratio:
                            #     similarity_str = ((str(most_matched_ration * 100))[0:3]).replace('.', '')
                            #     matched_caption_list[r] = most_matched_sentence
                            #     similarity_list[r] = similarity_str
                                
                                # rest_of_the_sentence = the_hole_sentence.replace(most_matched_sentence, '')
                            # my letest experiment ====================================
                            r += 1
                            progress = r / row_count * 100
                            progress_sognal = f'pg2: {round(progress)}'
                            # self.any_signal.emit(progress_sognal)
                    else:
                        r += 1

                        progress = r / row_count * 100
                        progress_sognal = f'pg2: {round(progress)}'
                        # self.any_signal.emit(progress_sognal)

            if r == row_count:
                break
        return matched_caption_list, similarity_list
    def find_correcet_caption(self):
        self.minimum_match_ratio = 0.70
        self.tableWidget.setColumnCount(5)
        row_count = self.tableWidget.rowCount()
        r = 0
        r_s = 0
        while True:
            recognized_text = self.tableWidget.item(r, 1).text()
            try:
                script_sentence =  self.tableWidget.item(r_s, 2).text()
                if script_sentence[0] == ' ':
                    script_sentence = script_sentence[1:-1]
            except Exception:
                script_sentence = ''
            similarity = similarity_ration_btween(recognized_text, script_sentence)
            if similarity > self.minimum_match_ratio:
                self.tableWidget.setItem(r, 3, (QTableWidgetItem(script_sentence.format(0, 0))))
                similarity_str = (str(similarity*100))[0:2]
                self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                r += 1
                r_s += 1
            else:
                words_in_recognized_sentence = recognized_text.split(' ')
                words_in_sentence = script_sentence.split(' ')
                word_num_in_sentence = len(words_in_sentence)

                custom_sentence = ''
                most_matched_sentence = ''

                most_matched_ration = 0.0000000000000000000000
                for w_i in range(word_num_in_sentence):
                    custom_sentence += f'{words_in_sentence[w_i]} '
                    if custom_sentence[0] == ' ':
                        custom_sentence = custom_sentence[1:-1]
                    similarity = similarity_ration_btween(recognized_text, custom_sentence)

                    if similarity > most_matched_ration:
                        most_matched_ration = similarity
                        most_matched_sentence = custom_sentence
                if most_matched_ration > self.minimum_match_ratio:
                    # self.tableWidget.setItem(r, 4, (QTableWidgetItem(most_matched_sentence.format(0, 0))))

                    self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                    similarity_str = (str(most_matched_ration * 100))[0:2]

                    self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                    r += 1

                    rest_of_the_sentence = script_sentence.replace(most_matched_sentence, '')

                    next_recognized_sentence = self.tableWidget.item(r, 1).text()

                    similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                    if similarity > self.minimum_match_ratio:
                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))

                        self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                        similarity_str = (str(similarity * 100))[0:2]

                        self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        r += 1
                        r_s += 1
                    else:
                        r += 1
                        print('in else 2')
                else:
                    most_matched_sentence = ''
                    most_matched_ration = 0.0000000000000000000000

                    for sen in range(row_count):
                        try:
                            script_sentence = self.tableWidget.item(sen, 2).text()
                        except Exception:
                            script_sentence = ''
                        similarity = similarity_ration_btween(recognized_text, script_sentence)
                        if similarity > most_matched_ration:
                            most_matched_ration = similarity
                            most_matched_sentence = script_sentence
                    if most_matched_ration > self.minimum_match_ratio:
                        # self.tableWidget.setItem(r, 4, (QTableWidgetItem(most_matched_sentence.format(0, 0))))

                        self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                        similarity_str = (str(most_matched_ration * 100))[0:2]

                        self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                        r += 1

                    elif most_matched_ration > 0.4:
                        the_hole_sentence = most_matched_sentence

                        words_in_sentence = most_matched_sentence.split(' ')
                        word_num_in_sentence = len(words_in_sentence)

                        custom_sentence = ''
                        most_matched_sentence = ''

                        most_matched_ration = 0.0000000000000000000000
                        for w_i in range(word_num_in_sentence):
                            custom_sentence += f'{words_in_sentence[w_i]} '
                            if custom_sentence[0] == ' ':
                                custom_sentence = custom_sentence[1:-1]
                            similarity = similarity_ration_btween(recognized_text, custom_sentence)

                            if similarity > most_matched_ration:
                                most_matched_ration = similarity
                                most_matched_sentence = custom_sentence
                        if most_matched_ration > self.minimum_match_ratio:
                            # self.tableWidget.setItem(r, 4, (QTableWidgetItem(most_matched_sentence.format(0, 0))))

                            self.tableWidget.setItem(r, 3, (QTableWidgetItem(most_matched_sentence.format(0, 0))))
                            similarity_str = (str(most_matched_ration * 100))[0:2]

                            self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                            r += 1

                            rest_of_the_sentence = the_hole_sentence.replace(most_matched_sentence, '')

                            next_recognized_sentence = self.tableWidget.item(r, 1).text()

                            similarity = similarity_ration_btween(next_recognized_sentence, rest_of_the_sentence)

                            if similarity > self.minimum_match_ratio:
                                # self.tableWidget.setItem(r, 4, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))

                                self.tableWidget.setItem(r, 3, (QTableWidgetItem(rest_of_the_sentence.format(0, 0))))
                                similarity_str = (str(similarity * 100))[0:2]

                                self.tableWidget.setItem(r, 4, (QTableWidgetItem(similarity_str.format(0, 0))))

                                r += 1
                                r_s += 1
                            else:
                                r += 1
                                print('in else 3')
                                print(f'rest of the sentence:{rest_of_the_sentence}')
                        else:
                            r += 1
                    else:
                        r += 1


            if r == row_count:
                break
    def copy_text_file_path(self):
        file_path = self.file_path.text()
        pc.copy(file_path)
    def match_sequence_func(self):
        if self.match_sequence_checkBox.isChecked() == True:
            self.Skip_checkBox.setChecked(False)
            self.Minimum_matched_ratio_lineEdit.setEnabled(True)
            self.horizontalSlider_2.setEnabled(True)
        else:
            self.Skip_checkBox.setChecked(True)

            self.Minimum_matched_ratio_lineEdit.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
    def open_table(self):
        path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory='Desktop',
                filter=self.filterTypes
            )
        if path:
            try:    
                with io.open(path, 'r', encoding="utf-8") as f:
                    file_text = f.read()
                self.tableWidget.clear()
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)

                lists_in_file = (file_text.split('\n'))

                self.tableWidget.setColumnCount(len(lists_in_file))
                colums_header_labels = []
                header = self.tableWidget.horizontalHeader()                                  # uncomment this
                header.setSectionResizeMode(1, PyQt5.QtWidgets.QHeaderView.Interactive)
                c = 0
                r  = 0
                for l in lists_in_file[:]:
                    index_of_label_finisher = l.index(':')
                    horizontal_Header_label = l[0:index_of_label_finisher]
                    colums_header_labels.append(horizontal_Header_label)
                self.tableWidget.setHorizontalHeaderLabels(colums_header_labels)    
                for l in lists_in_file[:]:
                    index_of_label_finisher = l.index(':')
                    horizontal_Header_label = l[0:index_of_label_finisher]
                    # just_list = ((l.replace(f"{horizontal_Header_label}:['", "")).replace("']", "")).split("', '")
                    just_list = ((l.replace(f"{horizontal_Header_label}:", ""))).split("|-|")

                    r  = 0
                    for e in just_list[:]:
                        if c == 0:
                            rowPosition = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(rowPosition)

                        if e[0] == ' ':
                            e = e[1:-1]
                        item = QTableWidgetItem(e.format(0, 0))
                        self.tableWidget.setItem(r , c, item)
                        r+=1
                    print(f'Row item number of {horizontal_Header_label} is: {len(just_list)}')

                    c += 1   
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 10pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong!\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()
                pass   
    def save_table(self):
        if self.path == 0:
            self.save_as_table()
        else:
            row_count = self.tableWidget.rowCount()
            colum_count = self.tableWidget.columnCount()
            text_ = ''
            for c in range(colum_count)[:]:
                column_lable = self.tableWidget.horizontalHeaderItem(c).text()    
                row_item_list = []
                for r in range(row_count)[:]:
                    try:    
                        row_item = (self.tableWidget.item(r, c).text())
                        row_item_list.append(row_item)
                    except Exception:
                        row_item = '' 
                        row_item_list.append(row_item)   
                text_ += f'{column_lable}:{row_item_list}\n'       
            try:
                with io.open(self.path, 'w', encoding="utf-8") as f:
                    f.write(text_) 
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 10pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong!\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()              
    def save_as_table(self):
        row_count = self.tableWidget.rowCount()  
        colum_count = self.tableWidget.columnCount() 
        text_ = ''
        for c in range(colum_count)[:]:
            column_lable = self.tableWidget.horizontalHeaderItem(c).text()    
            row_item_list = []
            for r in range(row_count)[:]:
                try:    
                    row_item = (self.tableWidget.item(r, c).text())
                    row_item_list.append(row_item)
                except Exception:
                    row_item = ''
            row_list = (((str(row_item_list)).replace("['", "")).replace("', '", "|-|")).replace("']", "")
            if c == colum_count - 1:

                text_ += f'{column_lable}:{row_list}'
            else:
                text_ += f'{column_lable}:{row_list}\n'
            print(f'Row item number of {column_lable} is: {len(row_item_list)}')
            print(f'{column_lable}:{len(row_list.split("|-|"))}')
        
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as',
            '',
            filter=self.filterTypes
        )
        if path:
            try:
                with io.open(path, 'w', encoding="utf-8") as f:
                    f.write(text_)

                self.path = path
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 10pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong! 3\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()        
    def UndoFunc(self):
        print('in undo function')
        self.strate_undo_clicked_count -=1
        try:    
            list_str = self.backUp_list[self.strate_undo_clicked_count]
            lists = (list_str.split('\n'))
            timeStamp = (((str(lists[0])).replace("['", "")).replace("']", "")).split("', '")
            caption_list = (((str(lists[1])).replace("['", "")).replace("']", "")).split("', '")
            print(len(timeStamp))
            while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
            r = 0
            for t in timeStamp[:]:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                item = QTableWidgetItem(t.format(0, 0))
                self.tableWidget.setItem(r,0, item)

                try:
                    item = QTableWidgetItem(caption_list[r].format(0, 0))
                    self.tableWidget.setItem(r,1, item)
                except Exception as e:
                    pass
                    pass    
                r+=1
        except Exception as e:
            print(e)
            pass    
    def saveForBackup(self):
        time_stamp_list = []
        caption_list = []
        row_count = self.tableWidget.rowCount()
        for r in range(row_count)[:]:
            time_stamp = (self.tableWidget.item(r , 0).text())     
            try:    
                caption = (self.tableWidget.item(r , 1).text()) 
            except Exception:
                caption = ''        
            time_stamp_list.append(time_stamp)
            caption_list.append(caption)
        BC_ = f'{time_stamp_list}\n{caption_list}'
        if len(self.backUp_list) < self.back_up_limit:
            if BC_ not in self.backUp_list:
                self.backUp_list.append(BC_)
                self.strate_undo_clicked_count = 0
                print('back up saved1')
        else:
            for i in range(len(self.backUp_list))[:]:
                try:    
                    self.backUp_list[i] = self.backUp_list[i+1]
                except Exception:
                    self.backUp_list.remove(self.backUp_list[-1])
                    self.backUp_list.append(BC_)
                    self.strate_undo_clicked_count = 0
                    print('back up saved1')

                    pass
    def enable_text_tab(self):
        if self.checkBox.isChecked() == True:
            # self.JusttextEdit_2.setVisible(False)
            
            self.tabWidget.setTabEnabled(1, True) 
            self.tableWidget.setVisible(True)

            self.Edit_pushButton.setVisible(True)
            self.Up_pushbutton.setVisible(True)
            self.DownPushButton.setVisible(True)
            self.Make_room_pushbutton.setVisible(True)
            self.RemovePushButton.setVisible(True)
            self.groupBox_5.setVisible(True)
        else:
            # self.JusttextEdit_2.setVisible(True) 
            
            self.tabWidget.setTabEnabled(1, False)   
            self.tableWidget.setVisible(False)
            self.Edit_pushButton.setVisible(False)
            self.Up_pushbutton.setVisible(False)
            self.DownPushButton.setVisible(False)
            self.Make_room_pushbutton.setVisible(False)
            self.RemovePushButton.setVisible(False)
            self.groupBox_5.setVisible(False)
    def TimeStamp(self, total_milisecs):

        seconds = int(total_milisecs/1000)    # this convert miliseconds to seconds

        miliseconds = ((str((total_milisecs/1000) - seconds)).replace('0.', ''))[0:3] # 

        if seconds > 59:
            if seconds < 3600: 
                hrs = '00'
                mins = (seconds//60)
                second = seconds - (mins * 60)  
                if second < 10:
                    if second == 0:
                        second = "00"    
                    else:
                        second = f'0{second}'
                else:    
                    second = str(second)  
                if mins < 10:
                    if mins == 0:
                        mins = '00'
                    else:
                        mins = f'0{mins}'
                else:
                    mins = str(mins)

            else:
                hrs = seconds // 3600
                left_secs = seconds - (hrs * 3600)
                mins = left_secs // 60
                secs = left_secs - (mins * 60)
                if hrs < 10:
                    if hrs == 0:
                        hrs = "00"
                    else:
                        hrs = f'0{hrs}'
                else:
                    hrs = str(hrs)        
                if mins < 10:
                    if mins == 0:
                        mins = '00'
                    else:
                        mins = f'0{mins}'
                else:
                    mins = str(mins)        
                if secs < 10:
                    if secs == 0:
                        secs = '00'
                        second = secs
                    else:
                        secs = f'0{secs}'  
                        second = secs
                        
                else:
                    secs = str(secs)  
                    second = secs

                # self.duration = f'{hrs} hrs {mins} mins {secs} secs'
        else:
            hrs = '00'
            mins = '00'
            if seconds < 10:
                if seconds == 0:
                    second = "00"    
                else:
                    second = f'0{seconds}'
            else:    
                second = str(seconds)

        

        return (str(hrs+':'+mins+':'+second+':'+miliseconds))  
    def chage_playback_speed(self):
        self.player.setPlaybackRate(float((self.Playback_speed_comboBox.currentText()).replace('x', '')))
    def set_position(self, position):
        self.player.setPosition(position)
        self.duration_label.setText(TimeStamp(position)) # position in miliseconds
    def position_changed(self, position):
        self.media_slider_horizontalSlider.setValue(position)
        self.duration_label.setText(TimeStamp(position))  # position in miliseconds
        colum_count = self.tableWidget.columnCount() 
        try:
            for r in self.nonsilent_range_list:
                start_point = r[0]
                end_point = r[1]
                row_index = self.nonsilent_range_list.index(r)
                if position >= start_point and position <= end_point:
                    if colum_count == 2:    
                        self.tableWidget.setCurrentCell(row_index, 1)
                    if colum_count == 5:
                        if (self.tableWidget.item(row_index, 3)).text() != ' ':
                            self.tableWidget.setCurrentCell(row_index, self.tableWidget.currentColumn())
                        else:    
                            self.tableWidget.setCurrentCell(row_index, self.tableWidget.currentColumn())
                    self.current_row_num = self.tableWidget.currentRow()

        except Exception as e:
            print(e)            
    def duration_changed(self, duration):
        self.media_slider_horizontalSlider.setRange(0, duration) # this just changes the duration
    def play_func(self):
        try:
            if self.playing_audio != True:
                self.player.play()
                self.play_audio_pushButton.setText("Pause")
                self.playing_audio = True
                pass
            else:
                self.player.pause()
                self.play_audio_pushButton.setText("Play")
                self.playing_audio = False
        except Exception as e:
            print(e)        
    def change_font(self):
        current_font = self.fontComboBox.currentText()
        self.textEdit.setStyleSheet(f'font: 12pt "{current_font}";')
        self.tableWidget.setStyleSheet(f'font: 12pt "{current_font}";\n\nbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(117, 189, 255, 255), stop:1 rgba(132, 198, 255, 255));')
        self.settings.setValue('font', current_font)
    def edit_func(self):
        if self.already_showing_edit_group == False:
            self.groupBox_4.setVisible(True)
            self.dockWidget.setVisible(True)
            self.already_showing_edit_group = True
            try:
                current_item = (self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text())
                self.textEdit.setText(current_item)
            except Exception:
                pass    
        else:
            self.groupBox_4.setVisible(False)
            self.dockWidget.setVisible(False)
            self.already_showing_edit_group = False 
    def selection_changed_function(self):
        try:
            try:    
                current_item = (self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text())
            except Exception:
                current_item =''    
            self.textEdit.setText(current_item)
            time_range = self.nonsilent_range_list[self.tableWidget.currentRow()]
            start_point = time_range[0]
            if self.playing_audio != True:   
                self.media_slider_horizontalSlider.setValue(start_point)
                self.player.setPosition(start_point)
            if self.tableWidget.currentRow() != self.current_row_num+1:
                if self.playing_audio == True: 
                    self.player.pause()
                    self.player.setPosition(start_point)
                    self.player.play()
            pass  
        except Exception:
            pass    
    def commit_save(self):
        custom_text = self.textEdit.toPlainText() 
        c_item = QTableWidgetItem(custom_text.format(0, 0))
            
        self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), c_item)
    def cancel_commit(self):
        self.groupBox_4.setVisible(False)
        self.dockWidget.setVisible(False)
        self.already_showing_edit_group = False    
    def reset_func(self):
        try:
            with io.open('.//Res//lists.txt', 'r', encoding="utf-8") as f:
                list_str = f.read()
            lists = (list_str.split('\n'))
            timeStamp = (((str(lists[0])).replace("['", "")).replace("']", "")).split("', '")
            caption_list = (((str(lists[1])).replace("['", "")).replace("']", "")).split("', '")
            while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
            r = 0
            for t in timeStamp[:]:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                item = QTableWidgetItem(t.format(0, 0))
                self.tableWidget.setItem(r,0, item)

                try:
                    item = QTableWidgetItem(caption_list[r].format(0, 0))
                    self.tableWidget.setItem(r,1, item)
                except Exception as e:
                    pass
                    pass    
                r+=1
        except Exception as e:
            print(e)
    def remove_func(self):
        if self.tableWidget.currentColumn() != 0:
            if len(self.tableWidget.selectedItems()) == 1:
                previous_item = ''
                p_item = QTableWidgetItem(previous_item.format(0, 0))
                self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), p_item)
            else:
                selected_items = self.tableWidget.selectedItems()

                self.selected_items = []

                for i in selected_items[:]:
                    row_column = [i.row(), i.column()]
                    self.selected_items.append(row_column)
                self.selected_items.reverse()

                for cell in self.selected_items:
                    previous_item = ''
                    p_item = QTableWidgetItem(previous_item.format(0, 0))
                    self.tableWidget.setItem(cell[0], cell[1], p_item)

        else:
            if len(self.tableWidget.selectedItems()) != 1:
                selected_items = self.tableWidget.selectedItems()

                self.selected_items = []

                for i in selected_items[:]:
                    row_column = [i.row(), i.column()]
                    self.selected_items.append(row_column)
                self.selected_items.reverse()

                for cell in self.selected_items:
                    self.tableWidget.removeRow(cell[0])
            else:
                try:
                    self.tableWidget.removeRow(self.tableWidget.currentRow())
                    self.nonsilent_range_list.remove(self.nonsilent_range_list[self.tableWidget.currentRow()])
                except Exception:
                    pass
        pass
    def make_room_func(self):
            caption_list = []
            row_count = self.tableWidget.rowCount()
            current_row = self.tableWidget.currentRow()
            the_row_to_create_a_room = self.tableWidget.currentRow() +1

            if current_row == self.tableWidget.rowCount():
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
            for i in range(row_count-current_row):
                try:
                    caption = (self.tableWidget.item(current_row , self.tableWidget.currentColumn()).text())   
                    caption_list.append(caption) 
                    current_row +=1
                except Exception:
                    pass
            previous_item = ''
            p_item = QTableWidgetItem(previous_item.format(0, 0))
            self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), p_item)        
            for c in  caption_list:
                item = QTableWidgetItem(c.format(0, 0))
                self.tableWidget.setItem(the_row_to_create_a_room , self.tableWidget.currentColumn(), item)
                the_row_to_create_a_room +=1
                if the_row_to_create_a_room == self.tableWidget.rowCount():
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)
    def down_button_clicked(self):
        if len(self.tableWidget.selectedItems()) == 1:
            try:
                previous_item = (self.tableWidget.item(self.tableWidget.currentRow()+1 , self.tableWidget.currentColumn()).text())
            except Exception:
                previous_item = ''
            current_item = (self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text())

            p_item = QTableWidgetItem(previous_item.format(0, 0))
            c_item = QTableWidgetItem(current_item.format(0, 0))

            self.tableWidget.setItem(self.tableWidget.currentRow()+1 , self.tableWidget.currentColumn(), c_item)
            self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), p_item)

            self.tableWidget.setCurrentItem(c_item)
        else:
            selected_items = self.tableWidget.selectedItems()
            self.selected_items = []

            for i in selected_items[:]:
                row_column = [i.row(), i.column()]
                self.selected_items.append(row_column)
            self.selected_items.reverse()
            for cell in self.selected_items:
                try:
                    try:
                        next_item = self.tableWidget.item(cell[0] + 1, cell[1]).text()
                    except Exception:
                        previous_item = ''
                    current_item = self.tableWidget.item(cell[0], cell[1]).text()

                    n_item = QTableWidgetItem(next_item.format(0, 0))
                    c_item = QTableWidgetItem(current_item.format(0, 0))

                    self.tableWidget.setItem(cell[0] + 1, cell[1], c_item)
                    self.tableWidget.setItem(cell[0], cell[1], n_item)

                    self.tableWidget.setCurrentItem(c_item)

                except Exception as e:
                    print(e)
            for cell in self.selected_items:
                try:
                    self.tableWidget.item(cell[0]+1, cell[1]).setSelected(True)
                except Exception:
                    pass
    def up_button_clicked(self):
        if len(self.tableWidget.selectedItems()) == 1:
            try:    
                previous_item = (self.tableWidget.item(self.tableWidget.currentRow()-1 , self.tableWidget.currentColumn()).text())
                current_item = (self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text())
                
                p_item = QTableWidgetItem(previous_item.format(0, 0))
                c_item = QTableWidgetItem(current_item.format(0, 0))
                
                self.tableWidget.setItem(self.tableWidget.currentRow()-1 , self.tableWidget.currentColumn(), c_item)
                self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), p_item)
                
                self.tableWidget.setCurrentItem(c_item)
            except Exception:
                pass
        else:
            selected_items = self.tableWidget.selectedItems() 
            self.selected_items = []

            for i in selected_items[:]:
                row_column = [i.row(), i.column()]
                self.selected_items.append(row_column)
            for cell in self.selected_items:
                try:
                    try:    
                        previous_item = self.tableWidget.item(cell[0]-1, cell[1]).text()
                    except Exception:
                        previous_item = ''    
                    current_item = self.tableWidget.item(cell[0], cell[1]).text()

                    p_item = QTableWidgetItem(previous_item.format(0, 0))
                    c_item = QTableWidgetItem(current_item.format(0, 0))

                    self.tableWidget.setItem(cell[0]-1, cell[1], c_item)
                    self.tableWidget.setItem(cell[0], cell[1], p_item)

                    # self.tableWidget.setCurrentItem(c_item)

                except Exception as e:
                    print(e)
            for cell in self.selected_items:
                try:
                    self.tableWidget.item(cell[0]-1, cell[1]).setSelected(True)
                except Exception:
                    pass
    def home_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.HomePagePushButton.setDisabled(True)
        self.TextPagePushButton.setDisabled(False)
        self.Save_pushButton.setDisabled(False)
        self.HomePagePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(117, 189, 255, 255), stop:1 rgba(255, 255, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-left-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"}')
        self.TextPagePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-right-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"}')
        self.Save_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"}')
    def text_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.HomePagePushButton.setDisabled(False)
        self.Save_pushButton.setDisabled(False)
        self.TextPagePushButton.setDisabled(True)
        self.HomePagePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-left-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.TextPagePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(117, 189, 255, 255), stop:1 rgba(255, 255, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-right-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.Save_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
    def SaveFunc(self):
        self.settings.setValue('MinSilLen', self.spinBox.value())
        self.settings.setValue('SilThrDb', self.lineEdit.text())
        self.settings.setValue('IncludeTimeStamp', self.checkBox.isChecked())
        self.settings.setValue('Delete_chuncks', self.ChunckscheckBox.isChecked())
        self.settings.setValue('Spliter', self.Sentance_spliter_lineEdit.text())
        self.settings.setValue('Match_ratio', self.Minimum_matched_ratio_lineEdit.text())
        self.settings.setValue('Match_Sequence_with_recognized_text', self.match_sequence_checkBox.isChecked())
        pass    
    def split_func(self):
        
        try:
            self.Refarence_text = self.Refarence_text.replace("\n", " ")
            self.Refarence_text = self.Refarence_text.replace("  ", " ")

            self.Num_of_sentance_lineEdit_2.setText("")
            spliters = self.Sentance_spliter_lineEdit.text()
            spliters_list = []
            for i in range(len(spliters))[:]:
                spliters_list.append(spliters[i])

            for s in spliters_list[:]:
                self.Refarence_text = self.Refarence_text.replace(s, f"{s}`")
        
            sentences_host = self.Refarence_text.split("`")  # basically sentences with punctions
            self.sentences = []
            sort_sentence = ""
            for s in sentences_host[:]:
                pure_sentence = ((s.replace("\n", " ").replace("  "," "))).strip()
                wordsInSentence = len(pure_sentence.split(" "))
                if pure_sentence != "" and wordsInSentence > 3:  
                    self.sentences.append(((sort_sentence+pure_sentence).replace("  ", " ").strip()))
                    sort_sentence = ""
                if pure_sentence != "" and wordsInSentence < 3:  
                    if sort_sentence != "":     
                        sort_sentence = f"{sort_sentence} {pure_sentence} "
                    else:
                        sort_sentence = f"{pure_sentence} "
                    wordsInShortSent = len(sort_sentence.split(" "))    
                    if wordsInShortSent > 3:
                        self.sentences.append(sort_sentence.strip())
                        sort_sentence = ""

            if sort_sentence != "":     
                self.sentences.append(sort_sentence.strip())
            # for sents in sentences_host[:]:
            #     print(sents)
            # self.sentences = sentences_host
            self.Num_of_sentance_lineEdit_2.setText(str(len(self.sentences)))
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                              "color: white;\n"
                              "background-color: rgb(108, 177, 223);\n"
                              "font: 10pt \"MS Shell Dlg 2\";\n"
                              "gridline-color: #EAEDED;\n"
                              "}")
            msg.setWindowTitle("Opps!")
            msg.setText(f"{e}\nPlease add a sentence spliter!")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()
            return
    def OpenRefarenceFile(self, path): # refferarence file open 
        if path:
            pass
        else:
            path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= "",
                filter='Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Rich Text Document (*.rtf);; Html (*.html);; SRT (*.srt)'
            )
            if path:
                pass
            else:
                return    
        if path:
            self.settings.setValue('Last_Ref_File_path', path)
            self.reffa_path = path
            try:    
                with io.open(path, 'r', encoding="utf-8") as f:
                    self.Refarence_text = f.read()

                    text_parts = self.Refarence_text.split('\n')
                    if 'Nms Script Pad document[' in text_parts[0]:
                        self.Refarence_text = ""
                        for l in text_parts[9:][:]:
                            self.Refarence_text +=f"{l} "
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"Fixedsys\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![1]\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_() 
                return
            self.settings.setValue('LastDilogPathforWavTotext', self.path)
            words = (self.Refarence_text.replace('  ', ' ')).split(' ')
            self.Num_of_words_lineEdit.setText(str(len(words)))
            self.Skip_checkBox.setChecked(False)
            self.Skip_checkBox.setEnabled(True)

            self.match_sequence_checkBox.setEnabled(True)
            self.match_sequence_checkBox.setChecked(True)

            self.remove_spaces_checkBox.setEnabled(True)
            self.Split_pushButton.setEnabled(True)
            self.file_path.setText(path)
            Size = round((int(os.path.getsize(path))/1000000), 2)
            self.SizelineEdit.setText(f'{Size} MB')
            parts = path.split('/')
            file_name = parts[-1]
            Dot_index = file_name.find('.')
            type_ = file_name[Dot_index:]
            just_name= file_name.replace(type_, '')
            just_type = type_.replace('.', '')
            self.File_lineEdit.setText(just_name)
            upper_type = just_type.upper()
            self.File_type_lineEdit.setText(upper_type)
        # print(self.Refarence_text)    
    def reset(self):
        self.horizontalSlider.setValue(25)
        self.spinBox.setValue(500) 
    def update_scilence_threshhold(self):
        self.lineEdit.setText(f'-{self.horizontalSlider.value()}')
    def update_threshhold(self):    
        if int((self.lineEdit.text()).replace('-', '')) < 15:
            self.lineEdit.setText(str(-15))  
            self.horizontalSlider.setValue(15)  
        elif int((self.lineEdit.text()).replace('-', '')) > 50: 
            self.lineEdit.setText(str(-50))  
            self.horizontalSlider.setValue(50)  
        else:
            self.horizontalSlider.setValue(int((self.lineEdit.text()).replace('-', ''))) 
            pass        
    def initGUI(self, status):
        if status == True:
            self.label_10.setText('Creating audio chunks.')
            self.Generate_pushButton.setVisible(False)
            self.groupBox_2.setVisible(False)
            # self.Copy_pushButton.setVisible(False)
            #
            # self.Clear_pushButton.setVisible(False)
            # self.Save_pushButton.setVisible(False)
            # self.textEdit.setVisible(False)
            self.progressBar.setVisible(False)
            self.label_10.setVisible(False)
            # self.TextFilepushButton.setVisible(False)
            self.resize(506, 300)
            
        elif status == False:
            self.Generate_pushButton.setVisible(True)
            self.groupBox_2.setVisible(True)
            self.Copy_pushButton.setVisible(True)
            
            self.Clear_pushButton.setVisible(True)
            self.Save_pushButton.setVisible(True)
            # self.textEdit.setVisible(True)
            
              
        else:  # when file is opened 
            self.Generate_pushButton.setVisible(True)
            self.groupBox_2.setVisible(True)         
    def save_text_as(self):
        text = ''
        if self.JusttextEdit_2.isVisible() == True:    
            text = self.JusttextEdit_2.toPlainText()
            path, _ = QFileDialog.getSaveFileName(
                self,
                'Save file as',
                '',
                self.filterTypes
            )
            if not path:
                return
            else:
                try:
                    with io.open(path, 'w', encoding="utf-8") as f:
                        f.write(text)
                        f.close()
                except Exception as e:
                    msg = QMessageBox()
                    msg.setStyleSheet("QMessageBox{\n"
                                      "color: white;\n"
                                      "background-color: rgb(108, 177, 223);\n"

                                      "font: 10pt \"MS Shell Dlg 2\";\n"
                                      "gridline-color: #EAEDED;\n"
                                      "}")
                    msg.setWindowTitle("Opps!")
                    msg.setText(f"Something went wrong!\nerror: {e}")
                    msg.setIcon(QMessageBox.Warning)
                    msg_exec = msg.exec_()
        else:
            self.stackedWidget.setCurrentIndex(2)
            self.HomePagePushButton.setDisabled(False)
            self.Save_pushButton.setDisabled(True)
            self.TextPagePushButton.setDisabled(False)

            self.HomePagePushButton.setStyleSheet(
                'QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-left-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
            self.Save_pushButton.setStyleSheet(
                'QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(117, 189, 255, 255), stop:1 rgba(255, 255, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
            self.TextPagePushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 11pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-bottom-right-radius : 22;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"}')
    def stopThread(self):
        self.thread.stop()
        self.groupBox.setEnabled(True)
        self.Generate_pushButton.setVisible(True)
        self.Cancel_pushButton.setVisible(False)
        self.Open_Audio_pushButton.setEnabled(True)
        # self.textEdit.setPlaceholderText('')
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.label_10.setVisible(False)
    def generate(self):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)
        self.label_10.setText('Creating audio chunks.')
        self.label_10.setVisible(True)
        self.start_thread = threading.Thread(target=start_sig)
        self.start_thread.start()
        lang_com = self.Language_comboBox.currentText()
        lang_parts = lang_com.split(') ')
        lang = str(lang_parts[1]) 
        path = self.path
        delete_chuncks = self.ChunckscheckBox.isChecked()
        for_srt_generator = self.checkBox.isChecked()
        self.mini_silen_len = self.spinBox.value()
        self.min_silen_thr = int(self.lineEdit.text())
        Minimum_matched_ratio = float(self.Minimum_matched_ratio_lineEdit.text())
        self.split_func()
        try:
            self.thread = ThreadClass(lang, path, delete_chuncks, for_srt_generator,self.mini_silen_len,self.min_silen_thr, self.sentences, self.Skip_checkBox.isChecked(),self.match_sequence_checkBox.isChecked(),Minimum_matched_ratio,self.FileFormat, parent=None)
        except Exception:
            self.sentences = []   
            self.thread = ThreadClass(lang, path, delete_chuncks, for_srt_generator,self.mini_silen_len,self.min_silen_thr, self.sentences, self.Skip_checkBox.isChecked(),self.match_sequence_checkBox.isChecked(),Minimum_matched_ratio,self.FileFormat, parent=None)
        self.thread.start()
        self.groupBox.setEnabled(False)
        self.Generate_pushButton.setVisible(False)
        self.Open_Audio_pushButton.setEnabled(False)
        self.Copy_pushButton.setEnabled(False)
        self.Clear_pushButton.setEnabled(False)
        self.Save_pushButton.setEnabled(False) 
        self.Cancel_pushButton.setVisible(True)
        # self.textEdit.setPlaceholderText("Generating text from the audio file. Please wait until it's finished.\nWe will let you know if something goes wrong.\nAnd make sure that your internet connection is working properly.")
        self.thread.any_signal.connect(self.my_function)  
        self.thread.time_stamp_list.connect(self.Add_time_stamp_list_func) 
        self.thread.nonsilent_data_list.connect(self.nonsilent_data_list) 
        self.thread.matched_sentence_signal.connect(self.match_signal_func)
    def match_signal_func(self, timeStamp, recognized, caption, Matched_caption, similarity_ratio):
        self.groupBox_11.setVisible(True)
        self.JusttextEdit_2.setVisible(False)
        self.tableWidget.clear()
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        self.tableWidget.setColumnCount(5)
        colums_header_labels = ['TimeStamp', 'Recognized Caption', 'Inputed Sentences','Matched Caption', 'Similarity']
        self.tableWidget.setHorizontalHeaderLabels(colums_header_labels)

        header = self.tableWidget.horizontalHeader() # uncomment this
        header.setSectionResizeMode(1, PyQt5.QtWidgets.QHeaderView.Interactive)

        header.setSectionResizeMode(3, PyQt5.QtWidgets.QHeaderView.Stretch)

        # header = self.tableWidget.horizontalHeader()  # uncomment this
        header.setSectionResizeMode(4, PyQt5.QtWidgets.QHeaderView.ResizeToContents)
        r = 0
        for t in timeStamp[:]:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            item = QTableWidgetItem(t.format(0, 0))
            self.tableWidget.setItem(r,0, item)

            item = QTableWidgetItem(recognized[r].format(0, 0))
            self.tableWidget.setItem(r,1, item)

            try:
                item = QTableWidgetItem(caption[r].format(0, 0))
                self.tableWidget.setItem(r,2, item)
            except Exception as e:
                pass

            item = QTableWidgetItem(Matched_caption[r].format(0, 0))
            self.tableWidget.setItem(r, 3, item)
            self.tableWidget.item(r, 3).setBackground(QColor(170, 255, 0, 155))

            item = QTableWidgetItem(str(similarity_ratio[r]).format(0, 0))
            self.tableWidget.setItem(r, 4, item)
            try:
                if int(similarity_ratio[r]) >89:
                    self.tableWidget.item(r, 4).setBackground(QColor(0, 255, 0, 255))
                if int(similarity_ratio[r]) >79 and int(similarity_ratio[r]) <90:
                    self.tableWidget.item(r, 4).setBackground(QColor(128, 255, 0, 255))    
                if int(similarity_ratio[r]) >69 and int(similarity_ratio[r]) <80:
                    self.tableWidget.item(r, 4).setBackground(QColor(255, 255, 0, 255))      
                if int(similarity_ratio[r]) >59 and int(similarity_ratio[r]) <70:
                    self.tableWidget.item(r, 4).setBackground(QColor(255, 153, 51, 255)) 
                if int(similarity_ratio[r]) >49 and int(similarity_ratio[r]) <60:
                    self.tableWidget.item(r, 4).setBackground(QColor(255, 102,102, 255))   
                if int(similarity_ratio[r]) >39 and int(similarity_ratio[r]) <50:
                    self.tableWidget.item(r, 4).setBackground(QColor(255, 51, 51, 255))       
            except Exception:
                pass         
            # item = QTableWidgetItem(similarity[r].format(0, 0))
            # self.tableWidget.setItem(r,3, item)
            r+=1

        if len(caption) > len(timeStamp):
            extra_row_num = len(caption) - len(timeStamp) 
            for u in range(extra_row_num):
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                try:
                    item = QTableWidgetItem(caption[r].format(0, 0))
                    self.tableWidget.setItem(r,2, item)
                except Exception as e:
                    pass
                r+=1
        

        self.tableWidget.setCurrentCell(0, 4)
        stop_sig()
        self.text_page()

        self.initGUI(False)
        self.progressBar.setValue(100)
        self.Save_pushButton.setVisible(True)
        self.groupBox.setEnabled(True)
        self.Generate_pushButton.setVisible(True)
        self.Save_pushButton.setEnabled(True)
        self.Open_Audio_pushButton.setEnabled(True)
        self.Copy_pushButton.setEnabled(True)

        self.Clear_pushButton.setEnabled(True)
        self.Cancel_pushButton.setVisible(False)
    def Add_time_stamp_list_func(self, timeStamp, caption_list):
        self.groupBox_11.setVisible(False)
        self.JusttextEdit_2.setVisible(False)
        try:
            with io.open('.//Res//lists.txt', 'w', encoding="utf-8") as f:
                f.write(f'{timeStamp}\n{caption_list}')
        except Exception:
            pass        
        r = 0
        header = self.tableWidget.horizontalHeader()                                  # uncomment this
        header.setSectionResizeMode(1, PyQt5.QtWidgets.QHeaderView.Stretch)
        for t in timeStamp[:]:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            item = QTableWidgetItem(t.format(0, 0))
            self.tableWidget.setItem(r,0, item)

            try:
                item = QTableWidgetItem(caption_list[r].format(0, 0))
                self.tableWidget.setItem(r,1, item)
            except Exception as e:
                pass
                pass    
            r+=1
        
        self.text_page()
        
        self.initGUI(False)
        self.progressBar.setValue(100)
        # self.textEdit.setText(text_)
        self.groupBox.setEnabled(True)
        self.Generate_pushButton.setVisible(True)
        self.Save_pushButton.setEnabled(True)
        self.Save_pushButton.setVisible(True)
        self.Open_Audio_pushButton.setEnabled(True)
        self.Copy_pushButton.setEnabled(True)
        self.Clear_pushButton.setEnabled(True)
        self.Cancel_pushButton.setVisible(False)
        # self.textEdit.setPlaceholderText('') 
        if self.error != True:
            try:
                self.start_thread = threading.Thread(target=stop_sig)
                self.start_thread.start()
            except Exception:
                print('could not play stop thread')
                pass 
        stop_sig()        
        pass
    def nonsilent_data_list(self, nonsilent_list):
        self.nonsilent_range_list = nonsilent_list
        self.JusttextEdit_2.setVisible(False)
        pass    
    def my_function(self, text):
        text_ = text 
        self.JusttextEdit_2.setVisible(False)
        if 'progress_:' in text_:
            
            splited_progress_signal = text_.split(' ')
            actual_progress = int((splited_progress_signal[1]))

            self.progressBar.setValue(actual_progress)
            if actual_progress == 100:
                self.label_10.setText('Recognizing audio chunks.')
            return
        if 'pg2:' in text_:

            splited_progress_signal = text_.split(' ')
            actual_progress = int((splited_progress_signal[1]))

            self.progressBar.setValue(actual_progress)
            if actual_progress <= 3:
                self.label_10.setText('Finding Matched Caption')
            return

        self.error = False
        if text_ == "recognition connection failed: [Errno 11001] getaddrinfo failed":
            print('recognition connection failed: [Errno 11001] getaddrinfo failed')
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"
                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(f"Something went wrong.\nMaybe it was an internet connection problem or you haven't selected the correct language for this audio.\nPlease try again!")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()
            text_ = ''
            self.error = True
        if text_ == "Something went wrong. Could not open the audio file 2":

            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(f"Something went wrong. Could not open the audio file")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()
            text_ = ''
            self.error = True    
        
        self.initGUI(False)
        self.progressBar.setValue(100)
        self.JusttextEdit_2.setText(text_)
        self.groupBox.setEnabled(True)
        self.Generate_pushButton.setVisible(True)
        self.Save_pushButton.setEnabled(True)
        self.Open_Audio_pushButton.setEnabled(True)
        self.Copy_pushButton.setEnabled(True)
        self.Clear_pushButton.setEnabled(True)
        self.Cancel_pushButton.setVisible(False)
        # self.textEdit.setPlaceholderText('') 
        if self.error != True:
            try:
                self.start_thread = threading.Thread(target=stop_sig)
                self.start_thread.start()
            except Exception:
                print('could not play stop thread')
                pass
    def lang_changed(self):
        curent_lang = self.Language_comboBox.currentText()
        with open('.//Res//current_lang_in_g.txt', "w") as CLG:
            CLG.write(curent_lang)
    def copy_path(self):
        try:
            text = self.File_path_lineEdit.text()
            pc.copy(text) 
        except Exception:
            pass      
    def clear(self):
        try:    
            self.error = False
            self.file_name_lineEdit.clear()
            self.TypeOf_filelineEdit.clear()
            self.Size_lineEdit.clear()
            self.Duration_lineEdit.clear()
            self.File_path_lineEdit.clear()
            while (self.tableWidget.rowCount() > 0):
                self.tableWidget.removeRow(0)
                
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps!")
            msg.setText(f"{e}")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_()
    def Open_file(self, path):   # audio file
        self.error = False
        if path:
            pass
        else:
            path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory=self.settings.value('Last_WAVE_File_path'),
                filter= 'All file (*.*);; WAV file (*.wav);; mp3 (*.mp3)'
            )
            if path:
                pass
            else:
                return
        if path:
            self.PlayPathButton.setEnabled(True)
            self.settings.setValue('Last_WAVE_File_path', path)
            # self.Split_pushButton.setEnabled(True)
            # self.Skip_checkBox.setEnabled(True)
            self.match_sequence_checkBox.setEnabled(True)
            self.remove_spaces_checkBox.setEnabled(True)


            url = QtCore.QUrl.fromLocalFile(path)
            self.player.setMedia(QtMultimedia.QMediaContent(url))

            self.path = path
            self.Generate_pushButton.setEnabled(True)
            self.File_path_lineEdit.setText(path)
            Size = round((int(os.path.getsize(path))/1000000), 2)
            self.Size_lineEdit.setText(f'{Size} MB')
            parts = path.split('/')
            file_name = parts[-1]
            Dot_index = file_name.find('.')
            type_ = file_name[Dot_index:]
            just_name= file_name.replace(type_, '')
            just_type = type_.replace('.', '')
            self.file_name_lineEdit.setText(just_name)
            upper_type = just_type.upper()
            self.TypeOf_filelineEdit.setText(upper_type)

            fname = path
            if just_type.upper() == 'WAV':    
                try:
                    with contextlib.closing(wave.open(fname,'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                        seconds = round(duration)
                        self.initGUI("sami")
                        self.FileFormat = "wav"
                except Exception as e:
                    msg = QMessageBox()
                    msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
                    msg.setWindowTitle("Opps!")
                    msg.setText(f"Something went wrong. Could not open the audio file.\nError: {e}")
                    msg.setIcon(QMessageBox.Warning)
                    msg_exec = msg.exec_()
                    return    	
                if seconds > 59:
                    if seconds < 3600: 
                        mins = (seconds//60)
                        second = seconds - (mins * 60) 
                        self.duration = f'{mins} mins {second} secs'
                        
                    else:
                        hrs = seconds // 3600
                        left_secs = seconds - (hrs * 3600)
                        mins = left_secs // 60
                        secs = left_secs - (mins * 60)
                        self.duration = f'{hrs} hrs {mins} mins {secs} secs'
                        
                else:
                    self.duration = f'{seconds} secs'
                self.Duration_lineEdit.setText(self.duration)
            if just_type.lower() == 'mp3': 
                self.FileFormat = "mp3"
                self.initGUI("sami")      
    def copy_text(self):
        text = (self.tableWidget.item(self.tableWidget.currentRow() , self.tableWidget.currentColumn()).text())
        pc.copy(text) 
    def paste_func(self):
        copied_text = pc.paste()
        custom_text = copied_text
        c_item = QTableWidgetItem(custom_text.format(0, 0))
        self.tableWidget.setItem(self.tableWidget.currentRow() , self.tableWidget.currentColumn(), c_item)
    def cut_text(self):
        text = 'self.textEdit.toPlainText()'
        pc.copy(text) 
    def Show_self(self):
        self.show()
    def init_Open_file(self, path):
            self.settings.setValue('Last_WAVE_File_path', path)
            self.Split_pushButton.setEnabled(True)
            # self.Skip_checkBox.setEnabled(True)
            self.match_sequence_checkBox.setEnabled(True)
            self.remove_spaces_checkBox.setEnabled(True)


            url = QtCore.QUrl.fromLocalFile(path)
            self.player.setMedia(QtMultimedia.QMediaContent(url))

            self.path = path
            self.Generate_pushButton.setEnabled(True)
            self.File_path_lineEdit.setText(path)
            Size = round((int(os.path.getsize(path))/1000000), 2)
            self.Size_lineEdit.setText(f'{Size} MB')
            parts = path.split('/')
            file_name = parts[-1]
            Dot_index = file_name.find('.')
            type_ = file_name[Dot_index:]
            just_name= file_name.replace(type_, '')
            just_type = type_.replace('.', '')
            self.file_name_lineEdit.setText(just_name)
            upper_type = just_type.upper()
            self.TypeOf_filelineEdit.setText(upper_type)

            fname = path
            if just_type.upper() == 'WAV':    
                try:
                    with contextlib.closing(wave.open(fname,'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                        seconds = round(duration)
                        self.initGUI("sami")
                except Exception as e:
                    msg = QMessageBox()
                    msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 10pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
                    msg.setWindowTitle("Opps!")
                    msg.setText(f"Something went wrong. Could not open the audio file.\nError: {e}")
                    msg.setIcon(QMessageBox.Warning)
                    msg_exec = msg.exec_()
                    return    	
                	
            if seconds > 59:
                if seconds < 3600: 
                    mins = (seconds//60)
                    second = seconds - (mins * 60) 
                    self.duration = f'{mins} mins {second} secs'
                    
                else:
                    hrs = seconds // 3600
                    left_secs = seconds - (hrs * 3600)
                    mins = left_secs // 60
                    secs = left_secs - (mins * 60)
                    self.duration = f'{hrs} hrs {mins} mins {secs} secs'
                    
            else:
                self.duration = f'{seconds} secs'
                

            self.Duration_lineEdit.setText(self.duration)
    def init_OpenRefarenceFile(self, path):
        if path:
            try:    
                with io.open(path, 'r', encoding="utf-8") as f:
                    self.Refarence_text = f.read()
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"Fixedsys\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![1]\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_() 
                return
    
            words = (self.Refarence_text.replace('  ', ' ')).split(' ')
            self.Num_of_words_lineEdit.setText(str(len(words)))
            self.Skip_checkBox.setChecked(True)
            self.Skip_checkBox.setEnabled(True)

            self.match_sequence_checkBox.setEnabled(True)
            self.match_sequence_checkBox.setChecked(False)

            self.remove_spaces_checkBox.setEnabled(True)

            self.file_path.setText(path)
            Size = round((int(os.path.getsize(path))/1000000), 2)
            self.SizelineEdit.setText(f'{Size} MB')
            parts = path.split('/')
            file_name = parts[-1]
            Dot_index = file_name.find('.')
            type_ = file_name[Dot_index:]
            just_name= file_name.replace(type_, '')
            just_type = type_.replace('.', '')
            self.File_lineEdit.setText(just_name)
            upper_type = just_type.upper()
            self.File_type_lineEdit.setText(upper_type)        
    def RemoveColumn(self):
        try:
            header = self.tableWidget.horizontalHeader() # uncomment this
            header.setSectionResizeMode(1, PyQt5.QtWidgets.QHeaderView.Interactive)

            header.setSectionResizeMode(3, PyQt5.QtWidgets.QHeaderView.Stretch)

            header = self.tableWidget.horizontalHeader()  # uncomment this
            header.setSectionResizeMode(4, PyQt5.QtWidgets.QHeaderView.Interactive)
            
            self.tableWidget.removeColumn(4)
        except Exception as e:
            print(e)
            pass    
        pass
    def closeEvent(self, event):
        try:
            self.player.pause()
            self.playing_audio = False
            pause_icon = QtGui.QIcon()
            pause_icon.addPixmap(QtGui.QPixmap(".//Imgs//playPng.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.play_audio_pushButton.setIcon(pause_icon)
        except Exception:
            pass    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Text_genarator() 
    ex.show()
    sys.exit(app.exec_())  
    
    
