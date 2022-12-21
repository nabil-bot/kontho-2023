# -*- coding:utf-8 -*-
#!/usr/bin/python3
# from typing import Text
# import PyQt5
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QColorDialog, QFontDialog, QMessageBox
from PyQt5.QtGui import QColor, QFont, QTextBlockFormat, QTextCursor  
import sys
import io
import os
from PyQt5.QtWidgets import QAction
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import QSettings
# from PyQt5.sip import T
import traceback
from pynput.keyboard import Controller

keyboard = Controller()

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QKeySequence

from multiprocessing import Process
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat
import TTSE
# import WebScraper


from bs4 import BeautifulSoup
import requests
import pyperclip as pc
keyboard = Controller()

class ScrapeThread(QtCore.QThread):	
    return_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self, url, Title_header, Title_class, Title_ID, paragraphs_tag, parent=None):
        super(ScrapeThread, self).__init__(parent)
        self.is_running = True
        self.url = url
        self.Title_header = Title_header
        self.Title_class = Title_class
        self.Title_ID = Title_ID
        self.paragraphs_tag = paragraphs_tag
        
    def run(self):
        # print("in run")
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find(self.Title_header, class_=self.Title_class).text
            paragraphs = soup.find_all(self.paragraphs_tag)
            artical = ''
            artical += f'{title}।\n'
            for p in paragraphs:
                artical += p.text

            if 'wikipedia' in self.url:
                custom_artical = ''
                for i in range(artical.count('['))[:]:
                    start_index = (artical.index('[')) -1
                    end_index =  artical.index(']') + 1
                    custom_artical = f'{artical[0:start_index]}{artical[start_index]} {artical[end_index:]}'
                    artical = custom_artical
                    artical = artical.replace('।।', '।')
                    artical = artical.replace('\n', ' ')
                    artical = artical.replace('অনিবন্ধিত সম্পাদকের জন্য পাতা আরও জানুন', '')
                    artical = artical.replace('পরিভ্রমণ', '')
                    artical = artical.replace('সরঞ্জাম', '')
                    artical = artical.replace('মুদ্রণ/রপ্তানি', '')
                    artical = artical.replace('অন্যান্য প্রকল্পে', '')
                    artical = artical.replace('  ', ' ')      

            self.return_signal.emit(artical)
            pass
        except Exception as e:
            self.error_signal.emit(str(e))
    def stop(self):
        self.terminate()

class ReplaceThreadClass(QtCore.QThread):	
    any_signal = QtCore.pyqtSignal(str)
    def __init__(self, text , this, toThis, parent=None):
        super(ReplaceThreadClass, self).__init__(parent)
        self.is_running = True
        self.text = text
        self.this = this
        self.toThis = toThis
    def run(self):
        print("In thread")
        custom_text = self.text.replace(self.this, self.toThis)
        self.any_signal.emit(custom_text)
        print("In thread2")
    def stop(self):
        self.is_running = False
        self.terminate()

class Ui_nms_pad(QMainWindow):
    def __init__(self):
        super(Ui_nms_pad, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('.//Uis//Nms_pad.ui', self) 
        Line_space_icon = QtGui.QIcon()
        Line_space_icon.addPixmap(QtGui.QPixmap("Imgs/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    # some extra shitty features ==================================================================================
        self.TTSE_class = TTSE.TextToSpeech_UI()
        self.dockWidget_2.setVisible(False)
    # some extra shitty features ==================================================================================
        self.raw_is_pressed = False
        self.hoshonto_is_presed = False
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.CancelScrapePushButton.setVisible(False)
        self.CancelScrapePushButton.clicked.connect(self.cancelScrape)

        self.Replace_groupBox.setVisible(False)
        self.Find_groupBox.setVisible(False)
        self.showing_count = False
        self.textEdit.setTextColor(QColor('black'))
        self.textEdit.setFont(QtGui.QFont('MS Shell Dlg 2', int(12)))
        self.textEdit.setFocus()
        self.filterTypes = 'Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Html (*.html);; SRT (*.srt)'
        self.path = None
        self.pre_path = False
        self.textEdit.setAcceptRichText(False)
        self.Close_count_pushButton.clicked.connect(self.Count_words_clicked_again)
        self.Close_font_pushButton.clicked.connect(self.Font_Para_again)
        self.actionReplace.triggered.connect(self.Replace_click)
        self.close_replace_Button.clicked.connect(self.close_replace)
        self.actionOpen_2.triggered.connect(self.file_open_new)
        self.actionSave_as.triggered.connect(self.file_saveAs)
        self.actionSave.triggered.connect(self.file_save)
        self.actionZoom_In.triggered.connect(self.increase_font_size)
        self.actionOpen_with_last_saved.triggered.connect(self.Oen_with)
        self.actionZoom_out.triggered.connect(self.decrese_font_size)
        self.actionNew.triggered.connect(self.New)
        self.actionExit_2.triggered.connect(self.closeEvent)
        self.actionFont.triggered.connect(self.Font_Para)
        self.actionCount.triggered.connect(self.Count_words)
        self.actionText_to_Speech_BETA.triggered.connect(self.show_Text_to_speech_window)
        self.actionWeb_Scraper.triggered.connect(self.show_Scraper_window)
        self.Font_groupBox.setVisible(False)
        self.Count_groupBox.setVisible(False)
        self.Replace_Button.clicked.connect(self.replace)
        self.Replace_cross_Button.clicked.connect(self.Replace_lineEdit_clear)
        self.Replace_cross_pushButton.clicked.connect(self.replace_to_this_lineEdit_clear)
        self.Replace_lineEdit.textChanged.connect(self.count)
        self.word_c_lineEdit.textChanged.connect(self.countWord)
        self.write_sp_word_cross_button.clicked.connect(self.word_c_lineEdit.clear)
        self.fontComboBox.currentIndexChanged.connect(self.change_font)
        self.font_size_comboBox.currentIndexChanged.connect(self.change_font_size)
        self.increase_font_size_pushButton.clicked.connect(self.increase_font_size)
        self.decrese_font_sizr_pushButton.clicked.connect(self.decrese_font_size)
        self.font_size_comboBox.setCurrentText(str(12))
        self.Bold_pushButton.clicked.connect(self.make_bold)
        self.RGB_pushButton.clicked.connect(self.colorDialog)
        self.Italic_pushButton.clicked.connect(self.make_italic)
        self.UnderLine_pushButton.clicked.connect(self.make_under_line)
        self.Black_pushButton.clicked.connect(self.black)
        self.White_pushButton.clicked.connect(self.white)
        self.Left_align_pushButton.clicked.connect(self.Left_align)
        self.center_align_pushButton.clicked.connect(self.center_align)
        self.Right_align_pushButton.clicked.connect(self.Right_align)
        self.Line_spaces_comboBox.currentIndexChanged.connect(self.change_linespace)
        self.Close_font_pushButton.clicked.connect(self.close_font_group)
        self.actionCut_2.triggered.connect(self.Cut)
        self.actionCopy_2.triggered.connect(self.copy)
        self.actionPaste_2.triggered.connect(self.textEdit.paste)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRemove_extra_spaces.triggered.connect(self.remove_extra_spaces) # ==========>
        self.actionFont_dialog.triggered.connect(self.Font_dialog)
        self.actionFind_2.triggered.connect(self.Show_find_dialog)
        self.subScriptButton.clicked.connect(self.subScript)
        self.superScriptButton.clicked.connect(self.superScript)
        self.latter_space_spinBox.valueChanged.connect(self.latterSpace)
        self.Show_find_pushButton.clicked.connect(self.Show_find_dialog)
        self.close_find_dialog_pushButton.clicked.connect(self.close_find)
        self.Show_replace_pushButton.clicked.connect(self.show_replace_dialog)
        self.Find_next_pushButton.clicked.connect(self.searchText)
        self.Highlight_all_pushbutton.clicked.connect(self.Highlight_all)
        self.clear_find_lineEdit_pushButton.clicked.connect(self.ClearFindLineEdit)
        self.Find_dedecated_lineEdit.textChanged.connect(self.find_lineedit_text_changed)
        self.copy_pushButton.clicked.connect(self.copy)
        self.Cut_pushButton.clicked.connect(self.Cut)
        self.Paste_pushButton.clicked.connect(self.textEdit.paste)
        self.firstFindAttempt = True
        self.current_search_index = 0
        self.Clear_button.clicked.connect(self.textEdit.clear)
        self.textEdit.textChanged.connect(self.textchanged)
        self.actionSafe_write.triggered.connect(self.safe_Write)
        self.PasteFindButton.clicked.connect(self.Find_dedecated_lineEdit.paste)
        self.preserved_text = ''
        
        # self.taking_commend = QAction('Take single Cdm.', self)
        # self.taking_commend.triggered.connect(lambda:path_ = 2)
        # self.taking_commend.triggered.connect(self.file_open)
        # self.menuOpen_Recent.addAction(self.taking_commend)

        self.settings = QSettings('ScriptPad')
        try:    
            self.fontComboBox.setCurrentText(self.settings.value('LastFont')) 
            self.change_font() 
        except Exception:
            pass          
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        with open('.//Res//Theme.txt', "r") as Theme:
            Theme_pos = Theme.read()
        if Theme_pos == "Light":
            self.actionLight_theme.setChecked(True)  
            self.textEdit.setStyleSheet("QTextEdit{\n\n	\n	background-color: rgb(250, 250, 250);\n}")
            self.black()
        if Theme_pos == "Dark":
            self.Dark_theme()
            self.white()
        if Theme_pos == "Blue":
            self.Blue_theme()
            self.textEdit.setTextColor(QColor('white'))
            self.textEdit.setFocus()  
            self.white()  
        with open('.//Res//open_with.txt', "r") as OWT:
            OWT_pos = OWT.read()
        with open('.//Res//safe_write.txt', "r") as SFW:
            SFW_pos = SFW.read() 
        if SFW_pos == "True":
            self.actionSafe_write.setChecked(True)          
        if OWT_pos == "True":
            self.actionOpen_with_last_saved.setChecked(True)
            try:
                with io.open('.//Res//last_file_path.txt', "r") as LFP:
                    LFP_pos = LFP.read()
                    print(LFP_pos) 
                self.path = LFP_pos
                self.pre_path = True
                self.file_open()
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"Fixedsys\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![0]\nCouldn't find the file in the path\n {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()    
            self.pre_path = False
        with open('.//Res//Stay_on_top.txt', "r") as SOT:
            SOT_pos = SOT.read()
        if SOT_pos == "ON":
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.actionStay_on_top.setChecked(True)
        with open('.//Res//LineHighlighter.txt', "r") as LHR:
            LHR_pos = LHR.read()
        if LHR_pos == "ON":
            self.textEdit.cursorPositionChanged.connect(self.highlightCurrentLine)   
            self.actionLine_Highlighter.setChecked(True)      
        self.actionLight_theme.triggered.connect(self.Light_theme)
        self.actionDark_Theme.triggered.connect(self.Dark_theme)
        self.actionBlue_Theme.triggered.connect(self.Blue_theme)
        self.actionLine_Highlighter.triggered.connect(self.lineHighlighter)
        self.actionStay_on_top.triggered.connect(self.stay_on_top)
        # delete me latter _________________________________________________________________=========$%^&*($%^&*#$%^&*)
        self.actionAdd_New_Words_to_list.triggered.connect(self.addWords)

        self.recentFiles = self.settings.value('recentFileList')
        # print(self.recentFiles)
        self.loadRecentFilePaths()
        self.menuOpen_Recent.triggered.connect(self.handle_triggered_recentfile)
    # ======================== Keyboard Functions slot =====================================

        with open('.//Res//Make_italic.txt', "w") as MIF:
            MIF.write("False")
        with open('.//Res//Make_Bold.txt', "w") as MBF:
            MBF.write("False")
        with open('.//Res//Make_Underline.txt', "w") as MUF:
            MUF.write("False")   

        self.ClearButton.clicked.connect(self.clear_line_edit)
        self.PastePushButton.clicked.connect(self.paste_func)
        self.ScrapePushButton.clicked.connect(self.scrape_article)
        self.SaveButton.clicked.connect(self.save_profile_function)
        self.websiteList = QSettings('websiteList')
        self.ProfileComboBox.currentIndexChanged.connect(self.UpdateProfile)
        self.DeletePushButton.clicked.connect(self.deleteProfile)
        
        try:
            self.websites = list(self.websiteList.value('List'))
            for web in self.websites:
                if web != "":
                    self.ProfileComboBox.addItem(web)    
        except Exception:
            self.websites = []
            pass           
    #delete me later =-=======================097851234567890!@#$%^&*()
    def loadRecentFilePaths(self):
        self.menuOpen_Recent.clear()
        filePaths = self.settings.value('recentFileList')
        if len(filePaths) > 12:
            flipedList = filePaths[::-1]
            
            limitedList = flipedList[:12]
            self.settings.setValue('recentFileList', limitedList[::-1])
            filePaths = self.settings.value('recentFileList')
        for filename in filePaths:
           self.add_recent_filename(filename) 
    def add_recent_filename(self, filename):
        action = QAction(filename, self)
        actions = self.menuOpen_Recent.actions()
        before_action = actions[0] if actions else None
        self.menuOpen_Recent.insertAction(before_action, action)   
    @QtCore.pyqtSlot(QAction)
    def handle_triggered_recentfile(self, action):
        # print(action.text())
        self.pre_path = True
        self.path = action.text()
        self.file_open()

    def addWords(self):
        # words_str = self.textEdit.toPlainText()
        # import WordMeneger
        # add_new_words(words_str)
        pass
    def stay_on_top(self):
        if self.actionStay_on_top.isChecked() == True:
            with open('.//Res//Stay_on_top.txt', "w") as SOT:
                SOT.write("ON")
        else:
            with open('.//Res//Stay_on_top.txt', "w") as SOT:
                SOT.write("OFF")  
        pass
    def highlightCurrentLine(self):
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        if self.actionBlue_Theme.isChecked() == True or self.actionDark_Theme.isChecked() == True:
            lineColor = QColor(0, 0, 205, 255) 
        else:    
            lineColor = QColor(0, 244, 255, 255)# .lighter(170)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textEdit.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.textEdit.setExtraSelections(extraSelections)

# Keyboard keys function ====================
    def scrape_article(self):
        try:
            url = self.URLlineEdit.text()
            
            Title_header = (self.TitleTaglineEdit.text()).replace(' ', '')
            Title_class = (self.Title_classlineEdit.text()).replace(' ', '')
            Title_ID = (self.IDlineEdit.text()).replace(' ', '')
            
            
            paragraphs_tag = str(self.ParagraphTaglineEdit.text())
            
            # self.Scrape_thread = ScrapeThread(url, Title_header, Title_class, Title_ID, paragraphs_tag, parent=None)
            # self.Scrape_thread.start()
            # self.Scrape_thread.return_signal.connect(self.setReturnText)
            # self.Scrape_thread.error_signal.connect(self.showError)
            # self.ScrapePushButton.setVisible(False)
            # self.CancelScrapePushButton.setVisible(True)

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find(Title_header, class_=Title_class).text
            paragraphs = soup.find_all(paragraphs_tag)
            artical = ''
            artical += f'{title}।\n'
            for p in paragraphs:
                artical += p.text

            if 'wikipedia' in url:
                custom_artical = ''
                for i in range(artical.count('['))[:]:
                    start_index = (artical.index('[')) -1
                    end_index =  artical.index(']') + 1
                    custom_artical = f'{artical[0:start_index]}{artical[start_index]} {artical[end_index:]}'
                    artical = custom_artical
                    artical = artical.replace('।।', '।')
                    artical = artical.replace('\n', ' ')
                    artical = artical.replace('অনিবন্ধিত সম্পাদকের জন্য পাতা আরও জানুন', '')
                    artical = artical.replace('পরিভ্রমণ', '')
                    artical = artical.replace('সরঞ্জাম', '')
                    artical = artical.replace('মুদ্রণ/রপ্তানি', '')
                    artical = artical.replace('অন্যান্য প্রকল্পে', '')
                    artical = artical.replace('  ', ' ') 

            self.setReturnText(artical)         
        except Exception as e:
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
    def cancelScrape(self):
        self.Scrape_thread.stop() 
        self.CancelScrapePushButton.setVisible(False)
        self.ScrapePushButton.setVisible(True)                
    def showError(self, e):
        self.CancelScrapePushButton.setVisible(False)
        self.ScrapePushButton.setVisible(True)
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
        msg.exec_()
        return
    def setReturnText(self, txt):
        self.CancelScrapePushButton.setVisible(False)
        self.ScrapePushButton.setVisible(True)
        self.textEdit.setText(txt)
        pass
    def Scrape(self):
        pass
    def save_profile_function(self):
        websiteURL = (self.WebURLlineEdit.text()).replace('.', '')
        if websiteURL not in self.websites:
            self.ProfileComboBox.addItem(websiteURL) #adding webprofile to combo box
            self.websites.append(websiteURL)
        self.websiteList.setValue('List', self.websites)
        QSettings(websiteURL).setValue("TitleTag", str(self.TitleTaglineEdit.text()))
        QSettings(websiteURL).setValue("TitleClass", str(self.Title_classlineEdit.text()))
        QSettings(websiteURL).setValue("ParagraphTag", str(self.ParagraphTaglineEdit.text()))
        # QSettings(websiteURL).setValue("ImageClass", str(self.mainImageClasslineEdit.text()))
        pass
    def deleteProfile(self):
        websiteURL = (self.WebURLlineEdit.text()).replace('.', '')
        QSettings(websiteURL).clear()
        self.websites.remove(websiteURL)
        self.ProfileComboBox.clear()
        self.websiteList.setValue('List', self.websites)
        for web in self.websites:
            if web != "":
                self.ProfileComboBox.addItem(web)   
        pass
    def UpdateProfile(self):
        self.ProfileComboBox.currentIndexChanged.connect(self.Scrape)
        
        current_profile = self.ProfileComboBox.currentText()
        self.WebURLlineEdit.setText(current_profile)
        self.TitleTaglineEdit.setText(QSettings(current_profile).value('TitleTag'))
        self.Title_classlineEdit.setText(QSettings(current_profile).value('TitleClass'))
        self.ParagraphTaglineEdit.setText(QSettings(current_profile).value('ParagraphTag'))
        # self.mainImageClasslineEdit.setText(QSettings(current_profile).value('ImageClass'))
        self.ProfileComboBox.currentIndexChanged.connect(self.UpdateProfile)
    def clear_line_edit(self):
        self.URLlineEdit.clear()
    def Show_self(self):
        self.show()  
    def paste_func(self):
        copied_text = pc.paste() 
        self.URLlineEdit.setText(copied_text)       
    def show_Text_to_speech_window(self):
        self.file_save()
        self.TTSE_class.Show_settings(self.textEdit.toPlainText(), self.path)
    def show_Scraper_window(self):
        self.dockWidget_2.setVisible(True)

    def lineHighlighter(self):
        if self.actionLine_Highlighter.isChecked() == True:
            self.textEdit.cursorPositionChanged.connect(self.highlightCurrentLine)
            with open('.//Res//LineHighlighter.txt', "w") as LHR:
                LHR.write("ON") 
        else:
            self.textEdit.cursorPositionChanged.connect(self.passfun) 
            with open('.//Res//LineHighlighter.txt', "w") as LHR:
                LHR.write("OFF")   
    def passfun(self):
        extraSelections = []
        # if not self.isReadOnly():
        selection = QTextEdit.ExtraSelection()
        if self.actionLight_theme.isChecked() == True:   
            lineColor = QColor(250, 250, 250)
        elif self.actionDark_Theme.isChecked() == True:
            lineColor = QColor(30, 30, 30)  
        elif self.actionBlue_Theme.isChecked() == True:
            lineColor = QColor(1, 22, 39)     
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textEdit.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.textEdit.setExtraSelections(extraSelections)
    def Light_theme(self):
        with open('.//Res//Theme.txt', "w") as MIF:
            MIF.write("Light")
        self.textEdit.setStyleSheet("QTextEdit{\n\n	\n	background-color: rgb(250, 250, 250);\n\n	color: rgb(0, 0, 0);\n\n}")    
        self.actionLight_theme.setChecked(True)
        self.actionDark_Theme.setChecked(False) 
        self.actionBlue_Theme.setChecked(False)           
    def Dark_theme(self):
        with open('.//Res//Theme.txt', "w") as MIF:
            MIF.write("Dark")  
        self.actionDark_Theme.setChecked(True)
        self.actionBlue_Theme.setChecked(False) 
        self.actionLight_theme.setChecked(False) 
        self.textEdit.setStyleSheet("QTextEdit{\n\n	\n	background-color: rgb(30, 30, 30); \n    color:rgb(255, 255, 255);}")       
    def Blue_theme(self):
        with open('.//Res//Theme.txt', "w") as MIF:
            MIF.write("Blue")  
        self.actionBlue_Theme.setChecked(True)
        self.actionLight_theme.setChecked(False)  
        self.actionDark_Theme.setChecked(False)  
        self.textEdit.setStyleSheet("QTextEdit{\n\n	\n	background-color: rgb(1, 22, 39); \n    color:rgb(255, 255, 255);}")      
    def safe_Write(self):
        status = self.actionSafe_write.isChecked()
        with open('.//Res//safe_write.txt', "w") as SFW:
            SFW.write(str(status))
    def textchanged(self):
        if self.actionSafe_write.isChecked() == True:
            if self.textEdit.toPlainText() != "":
                self.file_save()
            else:
                return 
        if self.showing_count == True:
            if self.word_c_lineEdit.text() == "":
                text = str(self.textEdit.toPlainText())
                lins = text.split('\n')
                text = text.replace('\n', '')
                words = []
                words_split = text.split(" ")
                for w in words_split:
                    if w !='':
                        words.append(w)
                    else:
                        pass    
                remove_items = ['', ' ', '|', '.', ' | ', '?', '!', '/', '[', ']' , '(', ')', '{', '}', '_', ';', ':'] 
                for i in remove_items:    
                    while(i in words) :
                        words.remove(i)
                
                spaces = text.count(" ")
                self.Count_info_lineEdit.setText(f'{len(words)} words; {spaces} spaces; {len(text)} lens') 
        self.TTSE_class.close_self()             
    def Oen_with(self):
        status = self.actionOpen_with_last_saved.isChecked()
        with open('.//Res//open_with.txt', "w") as OWT:
            OWT.write(str(status))     
        content_text = self.textEdit.toPlainText()    
        if self.preserved_text == content_text and self.preserved_text =="" and content_text =="" and status == True:
            self.pre_path = True
            with io.open('.//Res//last_file_path.txt', "r") as LFP:
                LFP_pos = LFP.read()
                # print(LFP_pos) 
            self.path = LFP_pos
            self.file_open()
    def replace_to_this_lineEdit_clear(self):
        self.replace_to_this_lineEdit.clear()
        conternt = str(self.textEdit.toPlainText())
        self.textEdit.clear()
        cursor = self.textEdit.textCursor() 
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor(250, 250, 250)))
        cursor.mergeCharFormat(format)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.setText(conternt)
        self.change_linespace()
        self.latterSpace()
        
        with open('.//Res//Alignment.txt', "r") as ALT:
            ALT_pos = ALT.read()
        if ALT_pos == 'Center':
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignCenter)
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor) 
        if ALT_pos == 'Left': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignLeft)  
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
        if ALT_pos == 'Right': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignRight) 
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
    def Replace_lineEdit_clear(self):
        self.Replace_lineEdit.clear()
    def ClearFindLineEdit(self):
        self.Find_dedecated_lineEdit.clear()
    def find_lineedit_text_changed(self):
        if self.Find_dedecated_lineEdit.text() == "":
            self.firstFindAttempt = True
            self.current_search_index = 0
            conternt = self.textEdit.toPlainText()
            cursor = self.textEdit.textCursor() 
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QBrush(QtGui.QColor(250, 250, 250)))
            self.textEdit.setText(conternt) 
            self.find_info_lineedit.setText('')
        else:
            return
        self.change_linespace()
        self.latterSpace()
        
        with open('.//Res//Alignment.txt', "r") as ALT:
            ALT_pos = ALT.read()
        if ALT_pos == 'Center':
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignCenter)
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor) 
        if ALT_pos == 'Left': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignLeft)  
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
        if ALT_pos == 'Right': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignRight) 
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)           
    def show_replace_dialog(self):
        self.Replace_groupBox.setVisible(True)  
        self.Find_groupBox.setVisible(False)
        self.Replace_lineEdit.setFocus()     
        self.actionReplace.triggered.connect(self.Replace_click_again)
    def Show_find_dialog(self):
        self.Find_groupBox.setVisible(True)
    def close_find(self):
        self.Find_dedecated_lineEdit.clear()
        self.Find_groupBox.setVisible(False)
        self.firstFindAttempt = True
        self.current_search_index = 0
    def searchText(self):
        if self.Find_dedecated_lineEdit.text() == "":
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"
                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Input missing")
            msg.setText("There is nothing to hilight!")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_() 
            return  
        # +++++++++++++++++++++++++++++++++++++++++++++++++info out++++++++
        content = self.textEdit.toPlainText()
        entered_text = self.Find_dedecated_lineEdit.text()
        number_of_element = content.count(entered_text)
        if self.current_search_index  < number_of_element: 
            self.current_search_index += 1
        self.find_info_lineedit.setText(f'{self.current_search_index} of {number_of_element}')
        cursor = self.textEdit.textCursor()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        cursor = self.textEdit.textCursor() 
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor(0, 244, 255)))
        pattern = "word"
        regex = QtCore.QRegExp(pattern)
        pos = 0
        
        if self.firstFindAttempt == True:
            self.index = str(self.textEdit.toPlainText()).find(self.Find_dedecated_lineEdit.text())
        if (self.index != -1):
            cursor.setPosition(self.index)
            # cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            length = len(entered_text)
            start = self.index
            cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, length)
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            cursor.mergeCharFormat(format)
            pos = self.index + regex.matchedLength()
            self.findIndexStart = int(self.index+1)
            self.index = str(self.textEdit.toPlainText()).find(self.Find_dedecated_lineEdit.text(), self.findIndexStart)
            self.firstFindAttempt = False
            self.textEdit.setTextCursor(cursor)  
            self.textEdit.ensureCursorVisible()
            self.textEdit.setFocus()
        else:
            self.textEdit.setFocus()    
    def Highlight_all(self):
        if self.Find_dedecated_lineEdit.text() == "":
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"
                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Input missing")
            msg.setText("There is nothing to hilight!")
            msg.setIcon(QMessageBox.Warning)
            msg_exec = msg.exec_() 
            return   
        content = self.textEdit.toPlainText()
        entered_text = self.Find_dedecated_lineEdit.text()
        number_of_element = content.count(entered_text)
        self.find_info_lineedit.setText(f'{number_of_element} of {number_of_element}')
        cursor = self.textEdit.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor(108, 177, 223)))
        pattern = "word"
        regex = QtCore.QRegExp(pattern)
        pos = 0
        index = str(self.textEdit.toPlainText()).find(self.Find_dedecated_lineEdit.text())
        while (index != -1):
            cursor.setPosition(index)
            # cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            length = len(entered_text)
            start = index
            cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, length)
            cursor.mergeCharFormat(format)
            pos = index + regex.matchedLength()
            self.findIndexStart = int(index+1)
            index = str(self.textEdit.toPlainText()).find(self.Find_dedecated_lineEdit.text(), self.findIndexStart)  
    def latterSpace(self):
        current_font = self.fontComboBox.currentText()
        font_size = int(self.font_size_comboBox.currentText())
        font = QtGui.QFont(current_font, int(font_size))
        with open('.//Res//Make_Underline.txt', "r") as MUF:
            MUF_pos = MUF.read()
        if MUF_pos == 'True':
            font.setUnderline(True) 
        with open('.//Res//Make_italic.txt', "r") as MIF:
            MIF_pos = MIF.read()
        if MIF_pos == "True":
            font.setItalic(True)
        with open('.//Res//Make_Bold.txt', "r") as MBF:
            MBF_pos = MBF.read()
        if MBF_pos == "True":
            font.setBold(True)   
        letter_space_current_value = int(self.latter_space_spinBox.value())
        font.setLetterSpacing(QFont.PercentageSpacing, int(100 + letter_space_current_value))
        self.textEdit.setFont(font)
    def superScript(self):
        cursor = self.textEdit.textCursor()
        format = cursor.charFormat()
        if format.verticalAlignment() == QTextCharFormat.AlignSuperScript:
            vert = QTextCharFormat.AlignNormal
        else:
            vert = QTextCharFormat.AlignSuperScript
        format.setVerticalAlignment(vert)
        cursor.setCharFormat(format)
        self.textEdit.setFocus() 
    def subScript(self):
        cursor = self.textEdit.textCursor()
        format = cursor.charFormat()
        if format.verticalAlignment() == QTextCharFormat.AlignSubScript:
            vert = QTextCharFormat.AlignNormal
        else:
            vert = QTextCharFormat.AlignSubScript
        format.setVerticalAlignment(vert)
        cursor.setCharFormat(format)
        self.textEdit.setFocus() 
    def Font_dialog(self):
        font, ok = QFontDialog.getFont()
        # font.setWordSpacing(20)  
        if ok:
            font.setLetterSpacing(QFont.PercentageSpacing, 200)
            font_details = (font.toString()).split(',')
            font_name = font_details[0]
            font_size = font_details[1]
            self.fontComboBox.setCurrentText(font_name)
            self.font_size_comboBox.setCurrentText(font_size)
            self.change_font()
            self.textEdit.setFont(font)
        else:
            pass
        self.textEdit.setFocus()    

    def copy(self):
       cursor = self.textEdit.textCursor()
       textSelected = cursor.selectedText()
       self.copiedText = textSelected
       self.textEdit.setFocus()
    def Cut(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedText = textSelected
        self.textEdit.cut()
        self.textEdit.setFocus()
    def paste(self):
        self.textEdit.append(self.copiedText) 
        self.textEdit.setFocus()  
    def close_font_group(self):
        self.Font_groupBox.setVisible(False)
        self.actionFont.triggered.connect(self.Font_Para)
        self.textEdit.setFocus()
    def change_linespace(self):
        blockFmt = QTextBlockFormat()
        number = self.Line_spaces_comboBox.currentText()
        if number == '1.5':    
            blockFmt.setLineHeight(150, QTextBlockFormat.ProportionalHeight)
        if number == '1':    
            blockFmt.setLineHeight(100, QTextBlockFormat.ProportionalHeight)
        if number == '1.15':    
            blockFmt.setLineHeight(115, QTextBlockFormat.ProportionalHeight)
        if number == '1.1':    
            blockFmt.setLineHeight(110, QTextBlockFormat.ProportionalHeight) 
        if number == '1.2':    
            blockFmt.setLineHeight(120, QTextBlockFormat.ProportionalHeight)   
        if number == '1.3':    
            blockFmt.setLineHeight(130, QTextBlockFormat.ProportionalHeight) 
        if number == '1.4':    
            blockFmt.setLineHeight(140, QTextBlockFormat.ProportionalHeight)  
        if number == '1.8':    
            blockFmt.setLineHeight(180, QTextBlockFormat.ProportionalHeight) 
        if number == '2':    
            blockFmt.setLineHeight(200, QTextBlockFormat.ProportionalHeight)                                    
        theCursor = self.textEdit.textCursor()
        theCursor.clearSelection()
        theCursor.select(QTextCursor.Document)
        theCursor.mergeBlockFormat(blockFmt)
        self.textEdit.setFocus()
    def Right_align(self):
        self.textEdit.selectAll()
        self.textEdit.setAlignment(Qt.AlignRight)
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)
        with open('.//Res//Alignment.txt', "w") as ALT:
            ALT.write('Right')
        self.textEdit.setFocus()
    def center_align(self):
        self.textEdit.selectAll()
        self.textEdit.setAlignment(Qt.AlignCenter)
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)
        with open('.//Res//Alignment.txt', "w") as ALT:
            ALT.write('Center')
        self.textEdit.setFocus()
    def Left_align(self):
        self.textEdit.selectAll()
        self.textEdit.setAlignment(Qt.AlignLeft)
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)
        with open('.//Res//Alignment.txt', "w") as ALT:
            ALT.write('Left')
        self.textEdit.setFocus()
    def white(self):
        self.textEdit.setTextColor(QColor('white'))
        self.textEdit.setFocus()
    def black(self):
        self.textEdit.setTextColor(QColor('black'))
        self.textEdit.setFocus()
    def make_under_line(self):
        self.textEdit.setFontUnderline(True)
        self.UnderLine_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0.591, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(160, 186, 186, 255));\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.UnderLine_pushButton.clicked.connect(self.make_under_line_again)
        self.textEdit.setFocus()
    def make_under_line_again(self):
        self.textEdit.setFontUnderline(False)
        self.UnderLine_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.UnderLine_pushButton.clicked.connect(self.make_under_line)
        self.textEdit.setFocus()
    def make_italic(self):
        self.textEdit.setFontItalic(True)
        self.Italic_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0.591, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(160, 186, 186, 255));\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.textEdit.setFocus()
        self.Italic_pushButton.clicked.connect(self.make_italic_again)
    def make_italic_again(self):
        self.textEdit.setFontItalic(False)
        self.Italic_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.textEdit.setFocus()
        self.Italic_pushButton.clicked.connect(self.make_italic)
    def make_bold(self): 
        self.textEdit.setFontWeight(QFont.Bold)
        self.textEdit.setFocus()
        self.Bold_pushButton.clicked.connect(self.make_bold_again)
        self.Bold_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\n	background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0.591, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(160, 186, 186, 255));\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
    def make_bold_again(self): 
        self.textEdit.setFontWeight(0)

        self.Bold_pushButton.setStyleSheet('QPushButton{\n padding-top:2px;\n	font: 10pt "MS Shell Dlg 2l";\n color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(33, 33, 33, 255), stop:1 rgba(75, 75, 75, 255));\nbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\n\nborder:1px solid rgb(253, 254, 254);\n\nborder-radius:5px;\n}\nQPushButton:hover{\ncolor: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(63, 63, 63, 255), stop:1 rgba(33, 33, 33, 255));\n background-color: qlineargradient(spread:pad, x1:0.505636, y1:0.221, x2:0.431818, y2:1, stop:0 rgba(89, 255, 255, 255), stop:1 rgba(60, 138, 255, 255));\n\n}\n\nQPushButton:pressed{\nbackground-color: qlineargradient(spread:pad, x1:0.767, y1:1, x2:1, y2:0, stop:0 rgba(0, 244, 255, 255), stop:1 rgba(3, 115, 255, 255));\\n"\n\n}')
        self.textEdit.setFocus()
        self.Bold_pushButton.clicked.connect(self.make_bold)
    def increase_font_size(self):
        incresed_font_size = str(int(self.font_size_comboBox.currentText())+1)
        self.font_size_comboBox.setCurrentText(incresed_font_size)
        self.change_font_size()
    def decrese_font_size(self):
        incresed_font_size = str(int(self.font_size_comboBox.currentText())-1)
        self.font_size_comboBox.setCurrentText(incresed_font_size)
        self.change_font_size()
    def change_font_size(self):
        current_font = self.fontComboBox.currentText()
        font_size = self.font_size_comboBox.currentText()
        try:    
            font = QtGui.QFont(current_font, int(font_size))
        except Exception:
            font = QtGui.QFont(current_font, 12)
            self.font_size_comboBox.setCurrentText(str(12))
        
        with open('.//Res//Make_italic.txt', "r") as MIF:
            MIF_pos = MIF.read()
        if MIF_pos == "True":
            font.setItalic(True)
        with open('.//Res//Make_Bold.txt', "r") as MBF:
            MBF_pos = MBF.read()
        if MBF_pos == "True":
            font.setBold(True)
        with open('.//Res//Make_Underline.txt', "r") as MUF:
            MUF_pos = MUF.read()
        if MUF_pos == 'True':
            font.setUnderline(True)      
        
        letter_space_current_value = int(self.latter_space_spinBox.value())
        font.setLetterSpacing(QFont.PercentageSpacing, int(100 + letter_space_current_value))
        self.textEdit.setFont(font)
        self.textEdit.setFocus()
    def change_font(self):
        current_font = self.fontComboBox.currentText()
        self.settings.setValue('LastFont', self.fontComboBox.currentText())
        try:    
            font_size = int(self.font_size_comboBox.currentText())
        except Exception:
            self.font_size_comboBox.setCurrentText(str(12))
        font = QtGui.QFont(current_font, int(font_size))
        with open('.//Res//Make_Underline.txt', "r") as MUF:
            MUF_pos = MUF.read()
        if MUF_pos == 'True':
            font.setUnderline(True) 
        with open('.//Res//Make_italic.txt', "r") as MIF:
            MIF_pos = MIF.read()
        if MIF_pos == "True":
            font.setItalic(True)
        with open('.//Res//Make_Bold.txt', "r") as MBF:
            MBF_pos = MBF.read()
        if MBF_pos == "True":
            font.setBold(True)     
        
       
        letter_space_current_value = int(self.latter_space_spinBox.value())
        font.setLetterSpacing(QFont.PercentageSpacing, int(100 + letter_space_current_value))
        

        self.textEdit.setFont(font)
        self.textEdit.setFocus()
    def colorDialog(self):
        color = QColorDialog.getColor()
        if color:
            self.textEdit.setTextColor(color)
            self.textEdit.setFocus()
    def countWord(self): 
        text = str(self.textEdit.toPlainText())
        if self.word_c_lineEdit.text() == "":
            text = str(self.textEdit.toPlainText())
            text = text.replace('\n', '')
            words = []
            words_split = text.split(" ")
            for w in words_split:
                if w !='':
                    words.append(w)
                else:
                    pass
            remove_items = ['', ' ', '|', '.', ' | ', '?', '!', '/', '[', ']' , '(', ')', '{', '}', '_', ';', ':'] 
            for i in remove_items:    
                while(i in words) :
                    words.remove(i)
            
            spaces = text.count(" ")
            self.Count_info_lineEdit.setText(f'{len(words)} words and {spaces} spaces; {len(text)} lnes')        

        else:
            word = str(self.word_c_lineEdit.text())
            word_count = text.count(word)
            self.Count_info_lineEdit.setText(f"{word_count}")
    def Count_words(self):  
        self.Count_groupBox.setVisible(True)
        self.showing_count = True
        self.word_c_lineEdit.setFocus()
        if self.word_c_lineEdit.text() == "":
            text = str(self.textEdit.toPlainText())
            lins = text.split('\n')
            text = text.replace('\n', '')
            words = []
            words_split = text.split(" ")
            for w in words_split:
                if w !='':
                    words.append(w)
                else:
                    pass    
            remove_items = ['', ' ', '|', '.', ' | ', '?', '!', '/', '[', ']' , '(', ')', '{', '}', '_', ';', ':'] 
            for i in remove_items:    
                while(i in words) :
                    words.remove(i)
            
            spaces = text.count(" ")
            self.Count_info_lineEdit.setText(f'{len(words)} words; {spaces} spaces; {len(text)} lnes')        

        
        self.actionCount.triggered.connect(self.Count_words_clicked_again)    
    def Count_words_clicked_again(self):
        self.actionCount.triggered.connect(self.Count_words)
        self.showing_count = False
        self.Count_groupBox.setVisible(False)
        self.textEdit.setFocus()
    def Font_Para(self):
        self.Replace_groupBox.setVisible(False)
        self.Count_groupBox.setVisible(False)
        self.Font_groupBox.setVisible(True)
        self.actionFont.triggered.connect(self.Font_Para_again)
    def Font_Para_again(self):
        self.Font_groupBox.setVisible(False)
        self.actionFont.triggered.connect(self.Font_Para)
    def count(self):
        if self.Replace_lineEdit.text() != '':
            word = self.Replace_lineEdit.text()
            text = str(self.textEdit.toPlainText())
            Number = text.count(word)
            self.replace_of_lineEdit_count.setText(str(Number))
        else:
            self.replace_of_lineEdit_count.setText("")    
    def remove_extra_spaces(self):
        text = str(self.textEdit.toPlainText())
        
        modiDir = {"  ": " ", " |": "|", " ।": "।", " .": ".", " ,": ",", " ?": "?", " ;": ";", "' ": "'", " '": "'", " :": ":",
        "( ": "(", " )": ")", "{ ": "{", " }": "}", "[ ": "[", " ]": "]"
        
        }

        for x, y in modiDir.items():
            text = text.replace(x, y)

        self.textEdit.setText(text)
        pass
    def replace(self):
        if self.Replace_lineEdit.text() != "":
            text = str(self.textEdit.toPlainText())
            this = self.Replace_lineEdit.text()
            to_this = self.replace_to_this_lineEdit.text()
            
            print(len(text))

            if len(text) < 800:    
                custom_text = text.replace(this, to_this)
            else:
                self.replace_thread = ReplaceThreadClass(text, this, to_this, parent=None)    
                self.replace_thread.start()
                self.replace_thread.any_signal.connect(self.Replace_in_thread_func)
                return
            self.textEdit.setText(custom_text)
            self.change_linespace()
            # ============================================================+++++
            # cursor = self.textEdit.textCursor()
            # format = QtGui.QTextCharFormat()
            # format.setBackground(QtGui.QBrush(QtGui.QColor(108, 177, 223)))
            # pattern = "word"
            # regex = QtCore.QRegExp(pattern)
            # pos = 0
            # index = str(self.textEdit.toPlainText()).find(to_this)
            # while (index != -1):
            #     cursor.setPosition(index)
            #     # cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)

            #     length = len(to_this)
            #     start = index
            #     cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            #     cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, start + length)
            #     cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, length)

            #     cursor.mergeCharFormat(format)
            #     pos = index + regex.matchedLength()
            #     self.findIndexStart = int(index+1)
            #     index = str(self.textEdit.toPlainText()).find(to_this, self.findIndexStart) 
            # ============================================================+++++

        else:
            return
        with open('.//Res//Alignment.txt', "r") as ALT:
            ALT_pos = ALT.read()
        # if ALT_pos == 'Center':
        #     self.textEdit.selectAll()
        #     self.textEdit.setAlignment(Qt.AlignCenter)
        #     cursor.movePosition(QTextCursor.End)
        #     self.textEdit.setTextCursor(cursor) 
        # if ALT_pos == 'Left': 
        #     self.textEdit.selectAll()
        #     self.textEdit.setAlignment(Qt.AlignLeft)  
        #     cursor.movePosition(QTextCursor.End)
        #     self.textEdit.setTextCursor(cursor)
        # if ALT_pos == 'Right': 
        #     self.textEdit.selectAll()
        #     self.textEdit.setAlignment(Qt.AlignRight) 
        #     cursor.movePosition(QTextCursor.End)
        #     self.textEdit.setTextCursor(cursor)
    def Replace_in_thread_func(self, text_):
        print('inReplace thread func')
        text = text_
        self.textEdit.setText(text)
        self.change_linespace()
        # ============================================================+++++
        cursor = self.textEdit.textCursor()
        # format = QtGui.QTextCharFormat()
        # format.setBackground(QtGui.QBrush(QtGui.QColor(108, 177, 223)))
        # pattern = "word"
        # regex = QtCore.QRegExp(pattern)
        # pos = 0
        # to_this = self.replace_to_this_lineEdit.text()
        # index = str(self.textEdit.toPlainText()).find(to_this)
        # while (index != -1):
        #     cursor.setPosition(index)
        #     # cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)

        #     length = len(to_this)
        #     start = index
        #     cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
        #     cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, start + length)
        #     cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, length)

        #     cursor.mergeCharFormat(format)
        #     pos = index + regex.matchedLength()
        #     self.findIndexStart = int(index+1)
        #     index = str(self.textEdit.toPlainText()).find(to_this, self.findIndexStart) 
        # ============================================================+++++
        with open('.//Res//Alignment.txt', "r") as ALT:
            ALT_pos = ALT.read()
        if ALT_pos == 'Center':
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignCenter)
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor) 
        if ALT_pos == 'Left': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignLeft)  
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
        if ALT_pos == 'Right': 
            self.textEdit.selectAll()
            self.textEdit.setAlignment(Qt.AlignRight) 
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
    def Replace_click(self):      
        self.Replace_groupBox.setVisible(True)  
        self.Replace_lineEdit.setFocus()     
        self.actionReplace.triggered.connect(self.Replace_click_again)
    def Replace_click_again(self):
        self.textEdit.setFocus()
        self.Replace_groupBox.setVisible(False)       
        self.actionReplace.triggered.connect(self.Replace_click)
    def close_replace(self):    
        self.Replace_groupBox.setVisible(False)       
    def file_open_new(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory= self.settings.value('LastDilogPathforScript'),
            filter='All (*.*);; Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Rich Text Document (*.rtf);; Html (*.html);; SRT (*.srt)'
        )
        if path:
            try:    
                with io.open(path, 'r', encoding="utf-8") as f:
                    text = f.read()
 
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
                if path in self.recentFiles:
                    self.recentFiles.remove(path)
                self.settings.setValue('recentFileList', self.recentFiles)
                self.loadRecentFilePaths()     
                return
            try:
                file_name, file_extension = os.path.splitext(str(path))
                if file_extension == ".docp" or file_extension == ".html":
                    self.textEdit.setHtml(text)
                    # return
                else:
                    self.textEdit.setText(text)
            except Exception as e:
                print(path)
                print(traceback.format_exc()) 
                self.textEdit.setText(text)
                pass        
            
            else:
                self.settings.setValue('LastDilogPathforScript', self.path)
                self.path = path
                
                # text_parts = text.split('\n')  
                self.defult_file = True
                # self.textEdit.clear()
                # for line in text_parts:    
                #     self.textEdit.append(line)
                self.preserved_text = text
                self.update_title() 
            self.path = path  

            if path in self.recentFiles:
                self.recentFiles.remove(path)
            self.recentFiles.append(path)
            self.settings.setValue('recentFileList', self.recentFiles)
            
            self.loadRecentFilePaths()
    def file_open(self):
        if self.pre_path == False:
            path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= self.settings.value('LastDilogPathforScript'),
                filter='All (*.*);; Text Document (*.txt);;Doc Pad (*.docp);; Python (*.py);; Markdown (*.md);; Rich Text Document (*.rtf);; Html (*.html);; SRT (*.srt)'
            )
        else:
            path = self.path    
        if path:
            try:    
                with io.open(path, 'r', encoding="utf-8") as f:
                    text = f.read()    
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
                if path in self.recentFiles:
                    self.recentFiles.remove(path)
                self.settings.setValue('recentFileList', self.recentFiles)
                self.loadRecentFilePaths()     
                return
            
            self.settings.setValue('LastDilogPathforScript', self.path)
            self.path = path
                
            self.defult_file = True
            self.textEdit.clear()
            
            try:
                file_name, file_extension = os.path.splitext(str(path))
                if file_extension == ".docp" or file_extension == ".html":
                    self.textEdit.setHtml(text)
                else:
                    self.textEdit.setText(text)
            except Exception as e:
                print(path)
                print(traceback.format_exc()) 
                self.textEdit.setText(text)
                pass  
            
            # self.textEdit.setText(text)
            self.preserved_text = text
            self.update_title() 
            self.path = path  

            if path in self.recentFiles:
                self.recentFiles.remove(path)
            self.recentFiles.append(path)
            self.settings.setValue('recentFileList', self.recentFiles)
            
            self.loadRecentFilePaths()  
    def file_save(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:

                if (self.path.split("."))[1] == "docp" or (self.path.split("."))[1] == "html":
                    text = self.textEdit.toHtml()
                else:
                    text = self.textEdit.toPlainText()   

                with io.open(self.path, 'w', encoding="utf-8") as f:
                    f.write(text)
                    f.close()
                self.preserved_text = self.textEdit.toPlainText()   
            except Exception as e:  
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![2]\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()
        if self.actionOpen_with_last_saved.isChecked() == True:
            try:    
                with open('.//Res//last_file_path.txt', "w") as LFP:
                    LFP.write(str(self.path))
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![2]\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()    
    def file_save_as_plainText(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                with open(self.path, 'r', encoding="utf-8") as f:
                    f_pos = f.read()
                text_parts = f_pos.split('\n')
                if 'Nms Script Pad document[' in text_parts[0]:
                    current_font = self.fontComboBox.currentText()
                    with open('.//Res//Make_italic.txt', "r") as MIF:
                        MIF_pos = MIF.read()
                    font_size = int(self.font_size_comboBox.currentText())
                    with open('.//Res//Alignment.txt', "r") as ALT:
                        ALT_pos = ALT.read()
                    line_space = self.Line_spaces_comboBox.currentText()    
                    with open('.//Res//Make_Bold.txt', "r") as MBF:
                        MBF_pos = MBF.read()
                    letter_space_current_value = 100 + int(self.latter_space_spinBox.value())    
                    text = f'Nms Script Pad document[\n{current_font}\n{font_size}\n{line_space}\n{MBF_pos}\n{MIF_pos}\n{ALT_pos}\n{letter_space_current_value}\n]\n{(self.textEdit.toPlainText())}'     
                else:    
                    text = self.textEdit.toPlainText()
                with io.open(self.path, 'w', encoding="utf-8") as f:
                    f.write(text)
                    f.close()
                self.preserved_text = self.textEdit.toPlainText()   
            except Exception as e:  
                msg = QMessageBox()
    def update_title(self):
        self.setWindowTitle('{0} -Nms Script Pad'.format(os.path.basename(self.path) if self.path else 'Unittled'))

    def file_saveAs(self):
        self.preserved_text = self.textEdit.toPlainText() 
        
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as',
            '',
            self.filterTypes
        )                               

        if not path:
            return

        
        else:
            self.path = path

            if (self.path.split("."))[1] == "docp" or (self.path.split("."))[1] == "html":
                text = self.textEdit.toHtml()
            else:
                text = self.textEdit.toPlainText()    
            try:
                with io.open(path, 'w', encoding="utf-8") as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 14pt \"Fixedsys\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Opps!")
                msg.setText(f"Something went wrong![3]\nerror: {e}")
                msg.setIcon(QMessageBox.Warning)
                msg_exec = msg.exec_()
            else:
                self.path = path
                self.update_title()
            if self.actionOpen_with_last_saved.isChecked() == True:
                with open('.//Res//last_file_path.txt', "w") as LFP:
                    LFP.write(str(path))            
    def New(self):
        self.path = None
        self.setWindowTitle('Untitled -Nms Script Pad')
        self.textEdit.setText("")
        self.Line_spaces_comboBox.setCurrentText('1')
        self.change_linespace()
        self.font_size_comboBox.setCurrentText("12")
        self.make_bold_again()
        self.make_under_line_again()
        self.make_italic_again()
    def Show_self(self):
        self.show()
    def closeEvent(self, event):
        content_text = self.textEdit.toPlainText()
        if self.preserved_text != content_text and self.preserved_text !="" and content_text !="":
            close = QMessageBox.question(self,
                                         "Quit?",
                                         "Do you want to save changes to this file?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if close == QMessageBox.Yes:
                self.file_save()
            if close == QMessageBox.No:
                pass
            if close == QMessageBox.Cancel:
                event.ignore() 
                return
        self.TTSE_class.close_self()  
        event.accept()       
    def close_msg_action(self, i, event):
        print(i.text())
        if str(i.text()) == "&Yes":
            self.file_save()
        if str(i.text()) == "&No":
            pass
        if str(i.text()) == "Cancel":
            event.ignore()
            return
        event.accept()
    def Error_msg(self, e):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{\n"
                        "color: white;\n"
                        "background-color: rgb(108, 177, 223);\n"

                        "font: 14pt \"MS Shell Dlg 2\";\n"
                        "gridline-color: #EAEDED;\n"
                        "}")
        msg.setWindowTitle("Opps!")
        msg.setText(f"Something went wrong![2]\nerror: {e}")
        msg.setIcon(QMessageBox.Warning)
        msg_exec = msg.exec_()
        pass
    def call_for_file_save(self):
        self.file_save()    
if __name__ == "__main__":
    # multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    ex = Ui_nms_pad() # Ui_self()  # if yout need to chang startup from main.py to splash then you need to change only here!
    ex.show()
    sys.exit(app.exec_())