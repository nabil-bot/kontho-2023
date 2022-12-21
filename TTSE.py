from ast import Lambda
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication, QSlider, QMainWindow, QFileDialog, QMessageBox
import speech_recognition as sr
from PyQt5.QtCore import QSettings
from PyQt5 import *
from PyQt5 import QtCore, QtMultimedia
import NumberToWord
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
import winsound
import threading
import Script_pad
import os
import Mic
from datetime import datetime, date
from pathlib import Path
from PyQt5.QtMultimedia import QMediaPlayer
import traceback

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


class ThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(str)
    prograss_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)
    
    def __init__(self, v1, v2, rate, pitch, fullText, file_path, USDVFES, min_silence_len, silence_thresh, keep_silence, Truncate_checked, parent=None):
        
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
        
        self.min_silence_len = min_silence_len
        self.silence_thresh = silence_thresh
        self.keep_silence = keep_silence
        self.Truncate_checked = Truncate_checked
        
        self.USDVFES = USDVFES
        self.v1 = v1
        self.v2 = v2
        self.rate = rate
        self.pitch = pitch
        self.fullText = fullText
        self.file_path = file_path

    def run(self):
        try:

            if self.USDVFES == False:
                self.prograss_signal.emit("Converting text to speech")
                command = f'edge-tts --voice {self.v1} --rate={self.rate} --pitch={self.pitch} --text "{self.fullText}" --write-media {self.file_path}'
                os.system(command)
            if self.USDVFES == True:
                self.prograss_signal.emit("Cleaning Previous Chunks")
                
                try:
                    dir_list = os.listdir(".//audio_chunks")
                    for file in dir_list:
                        os.remove(f".//audio_chunks//{file}")
                except Exception as e:
                    print(e)        

                sentenceList = self.sepaBangEng(self.fullText)
                self.prograss_signal.emit(f"Divided  into {len(sentenceList)} parts")
                sentCount = 0

                for sent in sentenceList[:]:
                    self.prograss_signal.emit(f"Generating: {sentCount}/{len(sentenceList)}")
                    if self.langList[sentCount] == "bng":
                        comd = f'edge-tts --voice {self.v1} --rate={self.rate} --pitch={self.pitch} --text "{sent}" --write-media .//audio_chunks//sentChunck{str(sentCount)}.mp3'
                    if self.langList[sentCount] == "eng":    
                        comd = f'edge-tts --voice {self.v2} --rate={self.rate} --pitch={self.pitch} --text "{sent}" --write-media .//audio_chunks//sentChunck{str(sentCount)}.mp3'

                    os.system(comd)
                    sentCount += 1       
                
                audioSegmentList = []
                self.prograss_signal.emit(f"Merging Together")

                for i in range(sentCount):
                    audioSegment = AudioSegment.from_mp3(f".//audio_chunks//sentChunck{str(i)}.mp3")
                    audioSegmentList.append(audioSegment)

                combined = AudioSegment.empty()
                
                c = 0
                for chunk in audioSegmentList:
                    self.prograss_signal.emit(f"Merging Together: {c}")
                    louder_song = chunk + 5
                    if (self.list_[c])[-2] not in [".", ",", "?", "|", ";", ":", "।", '"', "'"]:
                        louder_song = louder_song[:(len(louder_song)-525)]
                    combined += louder_song
                    c += 1
                combined.export(self.file_path, format ="mp3")   

            if self.Truncate_checked == True:    
                self.prograss_signal.emit("Truncate silence")
                file_name = self.file_path.split('/')[-1]
                audio_format = "mp3"
                # sound = AudioSegment.from_file(self.file_path, format = audio_format)
                
                sound = AudioSegment.from_mp3(self.file_path)

                audio_chunks = split_on_silence(sound,(self.min_silence_len) ,int(self.silence_thresh), (self.keep_silence))

                combined = AudioSegment.empty()
                for chunk in audio_chunks:
                    combined += chunk
                combined.export(self.file_path, format = audio_format)
            self.prograss_signal.emit("Converting mp3 to wav")
            self.any_signal.emit("finished!")
        except Exception as e:
            self.error_signal.emit(str(e))  
            print("in exception!")
            print(traceback.format_exc())  
        pass  
    
    def stop(self):
        self.is_running = False
        self.terminate() 

    def sepaBangEng(self, text):

        englishAlphabetes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
                        ]
        text = text.replace("  ", " ")
        self.langList = []
        self.list_ = []

        words = text.split(" ")

        banglaSent = ""
        englishSent = ""
        state = None
        for wrd in words:
            for un in ["(", ")", "{", "}", "[", "]", "!"]:
                wrd = wrd.replace(un, "")
            if wrd != "":
                try:
                    if wrd[0] in englishAlphabetes:
                        englishSent += f"{wrd} "
                        if state == 0:
                            self.langList.append("bng")
                            self.list_.append(banglaSent)
                            banglaSent = ""
                        state = 1

                    if wrd[0] not in englishAlphabetes:
                        banglaSent += f"{wrd} "
                        if state == 1:    
                            self.list_.append(englishSent)
                            self.langList.append("eng")
                            englishSent = ""
                        state = 0
                except Exception as e:
                    print(e)
                    print(wrd)        
        if state == 0:    
            self.list_.append(banglaSent)
            self.langList.append("bng")
        if state == 1:    
            self.list_.append(englishSent)  
            self.langList.append("Eng")  

        return self.list_

class TextToSpeech_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(TextToSpeech_UI, self).__init__()
        uic.loadUi('.//Uis//TextToSpeechUI.ui', self)
        
        self.recommendated_settings()
        self.horizontalSlider_2.setTickPosition(QSlider.TicksAbove)
        self.horizontalSlider_2.valueChanged.connect(self.Update_Threshold)
        self.Pitch_horizontalSlider.valueChanged.connect(lambda: self.Pitch_lineEdit.setText(f"{self.Pitch_horizontalSlider.value()}Hz"))
        self.ReSepushButton.clicked.connect(self.recommendated_settings)
        self.Export_Button.clicked.connect(self.export)
        self.checkBox.clicked.connect(self.enableTruncate)
        self.cancel_pushButton.clicked.connect(self.cancelFunction)
        self.cancel_pushButton.setVisible(False)
        self.Signal_label.setVisible(False)
        self.CreateSubtitleFilePushButton.setVisible(False)
        self.CreateSubtitleFilePushButton.clicked.connect(self.OpenWithWaveToText)
        self.settings = QSettings('TTSE')
        self.PreviewPushButton.clicked.connect(self.previewFunc)
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.stateChanged)
        self.playing_audio = False
        self.settingChanged = True
        self.comboBox.currentTextChanged.connect(self.settingChangerBool) 
        self.doubleSpinBox.valueChanged.connect(self.settingChangerBool)
        self.Pitch_horizontalSlider.valueChanged.connect(self.settingChangerBool) 
        self.UDVFES_Checkbox.stateChanged.connect(lambda:self.comboBox_2.setEnabled(self.UDVFES_Checkbox.isChecked()))
    
    def stateChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.stop()
            self.playing_audio = False 
            self.PreviewPushButton.setText("▶️ Preview")
            return
    def settingChangerBool(self):
        self.settingChanged = True
        if self.playing_audio == True:
            self.player.stop()
            self.playing_audio = False 
            self.PreviewPushButton.setText("▶️ Preview")
    def OpenWithWaveToText(self):
        self.pad = Script_pad.Ui_nms_pad()
        ScriptFilePath = self.SFP # got the text
        self.wav_to_text = Mic.Ui_Text_genarator()
        self.wav_to_text.Show_self()
        self.wav_to_text.OpenWith(self.path, ScriptFilePath)
        pass
    def enableTruncate(self):
        self.groupBox_11.setEnabled(self.checkBox.isChecked())    
    def Update_Threshold(self):
        self.Threshold_lineEdit.setText(str(self.horizontalSlider_2.value()))   
    def recommendated_settings(self):
        self.doubleSpinBox.setValue(1.0)
        self.horizontalSlider_2.setValue(-30)  
        self.doubleSpinBox_2.setValue(1000)  
        self.doubleSpinBox_3.setValue(800) 
        self.Pitch_horizontalSlider.setValue(0)
    def Show_settings(self, txt, txt_file_path):
        self.show()  
        self.SFP = txt_file_path
        self.txt = self.modify_artical(txt)
    def previewFunc(self):
        if self.playing_audio == False and self.settingChanged == True:
            self.PreviewPushButton.setText("Genareting Preview File")
            self.PreviewPushButton.setEnabled(False)
            wordsToPreviewWith = (self.txt.split(" "))
            txtToPreviewWith = ""
            words_limite = self.spinBox.value()
            word_count = 0
            for w in wordsToPreviewWith:
                if w != " " and w != "" and w not in [".", ",", "|", "/", "!", "%", ";", ";"]: 
                    txtToPreviewWith += f"{w} "
                    word_count +=1 
                if word_count >= words_limite:
                    break
            txtToPreviewWith = txtToPreviewWith[0:250]
            now = datetime.now().time()
            today = date.today()
            d2 = today.strftime("%B_%d_%Y")
            current_time = now.strftime("%H_%M_%S")

            self.PreviewFilePath = Path.home() / f"AppData/Local/Temp/speechToTextPreview_{d2}_{current_time}.mp3"
            # print(self.PreviewFilePath)
            # command = f'edge-tts --voice {self.comboBox.currentText()} --rate={self.doubleSpinBox.value()} --pitch={self.Pitch_lineEdit.text()} --text "{txtToPreviewWith}" --write-media {self.PreviewFilePath}'
            
            self.thread = ThreadClass(self.comboBox.currentText()," ", self.doubleSpinBox.value(),self.Pitch_lineEdit.text() ,txtToPreviewWith, self.PreviewFilePath, False,"","","","", parent=None)
            self.thread.any_signal.connect(self.finishedFunctionPreview)
            self.thread.error_signal.connect(self.ShowError)
            self.thread.start()
            self.settingChanged = False

            pass
        if self.playing_audio == True:
            self.player.stop()
            self.playing_audio = False 
            self.PreviewPushButton.setText("▶️ Preview")
            return
        if self.playing_audio == False and self.settingChanged == False:
            self.player.play()
            self.playing_audio = True 
            self.PreviewPushButton.setText("⏹ Stop")
            return
  
    def finishedFunctionPreview(self):
        # print(self.PreviewFilePath)
        self.PreviewPushButton.setText("⏹ Stop")
        self.PreviewPushButton.setEnabled(True)
        # self.player.setMedia(QtMultimedia.QMediaContent(self.PreviewFilePath))
        url = QtCore.QUrl.fromLocalFile(str(self.PreviewFilePath))
        self.player.setMedia(QtMultimedia.QMediaContent(url))

        self.player.play()
        self.playing_audio = True
        pass
    def export(self):
        # print(self.txt)
        try:
            self.path, _ = QFileDialog.getSaveFileName(
                self,
                'Save file as',
                directory= self.settings.value('LastDilogPath'),
                filter= "*.mp3" 
            )                               
            if not self.path:
                return
            else:
                pass
            self.settings.setValue('LastDilogPath', (self.path).replace(" ", "_"))
            self.path = (self.path).replace(" ","_")
                
            # command = f'edge-tts --voice {self.comboBox.currentText()} --rate={self.doubleSpinBox.value()} --pitch={self.Pitch_lineEdit.text()} --text "{str(self.txt)}" --write-media {(self.path).replace(" ","_")}'
            # print(self.UDVFES_Checkbox.isChecked())
            # self.thread = ThreadClass(command, self.path,int(self.doubleSpinBox_2.value()),int(self.Threshold_lineEdit.text()),int(self.doubleSpinBox_3.value()),self.checkBox.isChecked(),self.UDVFES_Checkbox.isChecked(),self.comboBox_2.currentText(),self.doubleSpinBox.value(),self.Pitch_lineEdit.text(),str(self.txt), parent=None)
            
            self.thread = ThreadClass(self.comboBox.currentText(),self.comboBox_2.currentText(),self.doubleSpinBox.value(), self.Pitch_lineEdit.text(),str(self.txt), self.path, self.UDVFES_Checkbox.isChecked(),int(self.doubleSpinBox_2.value()),int(self.Threshold_lineEdit.text()),int(self.doubleSpinBox_3.value()),self.checkBox.isChecked(), parent=None)

            self.thread.any_signal.connect(self.finishedFunction)
            self.thread.prograss_signal.connect(self.ProgFunc)
            self.thread.error_signal.connect(self.ShowError)
            self.thread.start()
            self.groupBox_7.setEnabled(False)
            self.Export_Button.setVisible(False)
            self.cancel_pushButton.setVisible(True)
            self.Signal_label.setVisible(True)
            self.ReSepushButton.setVisible(False)
            sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Start.wav', winsound.SND_FILENAME))
            sound_thread.start()
            return 
        except Exception as e:
            self.ShowError(e)    
    def ShowError(self, e):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{\n"
                        "color: white;\n"
                        "background-color: rgb(108, 177, 223);\n"
                        "font: 12pt \"MS Shell Dlg 2\";\n"
                        "gridline-color: #EAEDED;\n"
                        "}")
        msg.setWindowTitle("Opps!")
        msg.setText(str(e))
        msg.setIcon(QMessageBox.Warning)
        msg_exec = msg.exec_()
        self.PreviewPushButton.setText("Preview")
    def cancelFunction(self):
        self.thread.stop()
        self.CreateSubtitleFilePushButton.setVisible(False)
        self.groupBox_7.setEnabled(True)
        self.cancel_pushButton.setVisible(False)
        self.Export_Button.setVisible(True)
        self.Signal_label.setVisible(False)
        self.ReSepushButton.setVisible(True)
        sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Finish.wav', winsound.SND_FILENAME))
        sound_thread.start()
        pass
    def close_self(self):
        self.close()   
    def finishedFunction(self):
        self.CreateSubtitleFilePushButton.setVisible(True)
        self.groupBox_7.setEnabled(True)
        self.cancel_pushButton.setVisible(False)
        self.Export_Button.setVisible(True)
        self.Signal_label.setVisible(False)
        self.ReSepushButton.setVisible(True)
        sound_thread = threading.Thread(target=lambda:winsound.PlaySound('.//SFX//Finish.wav', winsound.SND_FILENAME))
        sound_thread.start()
        self.explore(self.path)
    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    def ProgFunc(self, signal):
        # print(signal)
        self.Signal_label.setText(signal)
    def modify_artical(self, artical):
        
        modiDic = {" |": "|", " ।": "।", " .": ".", " ,": "," ," ?": "?"," ;": ";" ,"' ": "'"," '": "'",
                    "সো": "শো", 'স্বয়ংক্রিয়ভাবে': 'স্বয়য়ংক্রিয়ভাবে', ' মো.': ' মোহাম্মদ', ' মো:': ' মোহাম্মদ', "য়": "য়", "হ্য": "য্য",
                    '্যাস': '্যাশ', ' শ ': ' শো ', '–': ' ', ',': ', ', ' তম ': ' তমো ', '৷': '। ', '।': '। ', '-': ' ',
                    '’': '', '‘': ',', '.': '। ', 'বাক্সে': 'বাক্শে', 'প্রবাহ':'প্রবাহো', "তম ":"তমো ", "সা":"শা", "বাক্স":"বাক্সো", "আপাতত": "আপাতোতো" 
        }
        for x, y in modiDic.items():
            artical = artical.replace(x, y)     

        artical = artical.replace('\n', ' ')

        artical = artical.replace('ছাড়াল', 'ছাড়ালো')
        artical = artical.replace('নিয়মতি', 'নিয়োমতি')
        artical = artical.replace('পেরোল', 'পেরোলো')
        artical = artical.replace('শ্রেয়', 'শ্রেয়ো')
        artical = artical.replace(" লাগল "," লাগলো ")
        artical = artical.replace(" হত "," হোতো ")
        artical = artical.replace(" হত "," হোতো ")
        artical = artical.replace(" ব্যতীত "," ব্যতীতো ")
        artical = artical.replace(" আমলে "," আমোলে ")

        artical = artical.replace('ব্যবসাসফল', 'ব্যবসা সফল')

        artical = artical.replace('\n', '')

        artical = artical.replace('  ', ' ')

        word_list = artical.split(' ')
        custom_artical= ''
        # this replaces all numbers into words ======================================
        bangla_numbers = ['০','১','২','৩','৪','৫','৬','৭','৮','৯']
        for w in word_list[:]:

            for n in bangla_numbers[:]:
                if n in w:

                    unwanted_part= ''
                    for i in range(len(w))[:]:
                        if w[i] not in bangla_numbers and w[i] !='.':
                            unwanted_part+= w[i]
                            pass
                    for i in range(len(unwanted_part))[:]:
                        w = w.replace(unwanted_part[i], '')
                    just_number = w
                       
                    number_to_replace = just_number
                    bangla_num_word = NumberToWord.convert_num_to_word(just_number)

                    try:    
                        w = f"{w.replace(just_number, bangla_num_word)} {unwanted_part}"
                        # w = f"{just_number} {unwanted_part}"

                    except Exception:
                        print(f"just_number:{just_number}, bangla_num_word:{bangla_num_word}")
                        pass
            custom_artical += f'{w} '
        # this replaces all numbers into words ======================================    

        return custom_artical            
    

    def sepaBangEng(self, text):

        englishAlphabetes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
        ]
        text = text.replace("  ", " ")
        list_ = []

        words = text.split(" ")

        banglaSent = ""
        englishSent = ""
        state = None
        for wrd in words:
            
            if wrd[0] in englishAlphabetes or wrd[-1] in englishAlphabetes:
                englishSent += f"{wrd} "
                if state == 0:    
                    list_.append(banglaSent)
                    banglaSent = ""
                state = 1

            if wrd[0] not in englishAlphabetes or wrd[-1] not in englishAlphabetes:
                banglaSent += f"{wrd} "
                if state == 1:    
                    list_.append(englishSent)
                    englishSent = ""
                state = 0
        if state == 0:    
            list_.append(banglaSent)
        if state == 1:    
            list_.append(englishSent)    

        return list_
    
    def closeEvent(self, event):
        if self.playing_audio == True:
            self.player.stop()
            self.playing_audio = False 
            self.PreviewPushButton.setText("▶️ Preview")
            try:    
                os.remove(self.PreviewFilePath)
            except Exception as e:
                print(e)    
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    ex = TextToSpeech_UI() 
    ex.show()
    sys.exit(app.exec_())    