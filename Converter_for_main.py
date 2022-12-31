
from PyQt5 import QtWidgets, uic
import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox 
import pyperclip as pc
import os 

from bijoy2unicode import converter  
# import Conveter_fun
# from Conveter_fun import Ui_conveter
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox   
from PyQt5.QtCore import QDir 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox   
import sys
import io
import os

from LoadWords import banglaUnicodesLatters
# from PyQt5 import QtCore

import converter

def convert(text):
    text = text.replace('ড়', 'ড়')
    text = text.replace('ঢ়', 'ঢ়')
    text = text.replace('য়', 'য়')
    test = converter.Unicode()
    demo_text = '2007 এ ফিলিস্তিনের নির্ধারিত গাজা ভূখণ্ডে নির্ধারণ প্রতিষ্ঠা করা হয়'
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
    B_f_words = custom_text.split(" ")
    new_text = ''
    for w in B_f_words[10:]:
        if B_f_words.index(w) == 10:
            new_text += f'{w}'
        else:
            new_text += f' {w}'          
    custom_text  = new_text
    return custom_text 

class Ui_converter(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_converter, self).__init__() 
        uic.loadUi('.//Uis//ConGui.ui', self) 

        file_icon = QtGui.QIcon()
        file_icon.addPixmap(QtGui.QPixmap(".//Imgs//Actions-document-open-folder-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Open_text_pushButton.setIcon(file_icon)

        file_icon = QtGui.QIcon()
        file_icon.addPixmap(QtGui.QPixmap(".//Imgs//kisspng-computer-icons-copying-cut-copy-and-paste-clipbo-paste-icon-free-download-png-and-vector-5c5f67badec551.8477141515497563469125.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Paste_pushButton.setIcon(file_icon)

        self.Convert_pushButton.clicked.connect(self.Convert_text)
        self.Paste_pushButton.clicked.connect(self.paste)
        self.Copy_pushButton.clicked.connect(self.copy_converted)
        self.Clear_pushButton.clicked.connect(self.clear)
        self.Open_text_pushButton.clicked.connect(self.Open_text)

        self.UnicodeRadioButton.toggled.connect(self.ConvertToUnicodeStateFunc)

        self.bijoyStyleSheet = 'QTextEdit{\nbackground-color: rgb(248, 248, 248);\nfont: 14pt  "Kalpurush ANSI" ;\n}'
        self.unicodeStyleSheet = 'QTextEdit{\nfont: 13pt  "./Fonts/Kalpurush" , "Kalpurush" ;\n	background-color: rgb(248, 248, 248);\n}'

        self.unicodeEngine = converter.Unicode()
    def ConvertToUnicodeStateFunc(self, selected):
        if selected:
            self.First_textEdit.setStyleSheet(self.bijoyStyleSheet)
            self.First_textEdit.setPlaceholderText("GLv‡b weRq ‡U·U wjLyb A_ev ‡c÷ Ki“b")
            self.second_textEdit.setStyleSheet(self.unicodeStyleSheet)
        else:
            self.First_textEdit.setStyleSheet(self.unicodeStyleSheet)
            self.First_textEdit.setPlaceholderText("Paste or write Unicode text here")
            self.second_textEdit.setStyleSheet(self.bijoyStyleSheet)
        pass    
    def Convert_text(self):
        try:    
            text = self.First_textEdit.toPlainText()
            if self.BijoyRadioButton.isChecked():
                converted_text = convert(self.preCustomize(text))
            else:
                converted_text = self.unicodeEngine.convertBijoyToUnicode(text)
            self.second_textEdit.clear()
            self.second_textEdit.setText(converted_text)    
        except Exception:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: #566573;\n"

                            "font: 4pt \"Fixedsys\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Suggestion")
            msg.setText("Something went wrong!")
            msg.setIcon(QMessageBox.Information)
            msg_exec = msg.exec_()
            return  

    def preCustomize(self, txt):
        txt = txt.replace("–", "-")
        return txt          
    def paste(self):
        self.First_textEdit.paste()
        text = self.First_textEdit.toPlainText()
        if text not in ["", " "]:
            if text[0] in banglaUnicodesLatters:
                self.BijoyRadioButton.setChecked(True)
            else:
                self.UnicodeRadioButton.setChecked(True)   
    def copy_converted(self):
        
        text = self.second_textEdit.toPlainText()
        pc.copy(text)    
    def clear(self):
        self.second_textEdit.setText('') 
        self.First_textEdit.setText('') 
    def Open_text(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            file_name = dialog.selectedFiles()
            if file_name[0].endswith('.txt'):

                with io.open(file_name[0], 'r', encoding="utf-8") as f:
                    data = f.read()
                    self.First_textEdit.setText(data)
                    f.close()
            else:
                pass          
    def show_converter(self):
        self.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_converter() 
    ex.show()
    sys.exit(app.exec_())          