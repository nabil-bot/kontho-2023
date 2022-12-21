# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint 
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsDropShadowEffect, QFileDialog
from PyQt5.QtGui import QColor # QPainter, 
import sys
import converter
import io


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

    B_f_words = custom_text.split(" ")
    new_text = ''
    for w in B_f_words[10:]:
        if B_f_words.index(w) == 10:
            new_text += f'{w}'
        else:
            new_text += f' {w}'          
    custom_text  = new_text
    return custom_text 

class Ui_conveter(QWidget):
    def __init__(self):
        super(Ui_conveter, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('Conveter_gui.ui', self) # Load the .ui file

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setOffset(1)
        shadow.setColor(QColor(0, 244, 255, 255))
        self.Convert_pushButton.setGraphicsEffect(shadow)
        self.Convert_pushButton.clicked.connect(self.Convert_text)
        self.Paste_pushButton.clicked.connect(self.paste)
        self.Copy_pushButton.clicked.connect(self.copy_converted)
        self.Clear_pushButton.clicked.connect(self.clear)
        self.Open_text_pushButton.clicked.connect(self.Open_text)
    def Convert_text(self):
        try:    
            text = self.Unicode_TextEdit.toPlainText()
            converted_text = convert(text)
            self.Bijoy_textEdit.setText(converted_text)
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
    def paste(self):
        self.Unicode_TextEdit.paste()
    def copy_converted(self):
        import pyperclip as pc
        text = self.Bijoy_textEdit.toPlainText()
        pc.copy(text)    
    def clear(self):
        self.Bijoy_textEdit.setText('') 
        self.Unicode_TextEdit.setText('') 
    def Open_text(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            file_name = dialog.selectedFiles()
            if file_name[0].endswith('.txt'):

                with io.open(file_name[0], 'r', encoding="utf-8") as f:
                    data = f.read()
                    self.Unicode_TextEdit.setText(data)
                    f.close()
            else:
                pass      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_conveter() # Ui_self()  # if yout need to chang startup from main.py to splash then you need to change only here!
    ex.show()
    sys.exit(app.exec_())        