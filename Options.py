from PyQt5 import QtWidgets, uic
import sys
import win32api
from PyQt5.QtWidgets import QApplication, QMessageBox
import speech_recognition as sr
from PyQt5.QtMultimedia import QAudioDeviceInfo, QAudio
from PyQt5.QtCore import QSettings
import os

class Options_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(Options_UI, self).__init__()
        uic.loadUi('.//Uis//Options.ui', self)

        self.settings_changed = False

        with open('.//Res//Recoard_settings.txt', "r") as RS:
            RS_pos = RS.read()
        settings = (RS_pos.split('\n'))
        self.Energy_spinBox.setValue(int(settings[0]))
        self.Pause_doubleSpinBox.setValue(float(settings[1]))
        self.Phrase_doubleSpinBox.setValue(float(settings[2]))
        self.Non_speaking_daration_doubleSpinBox.setValue(float(settings[3]))  
        # self.Operation_time_out_comboBox.setCurrentText(settings[4])

        self.Apply_pushButton.clicked.connect(self.Apply_func)
        self.Reset_pushButton.clicked.connect(self.Reset_all)
        self.Developer_recomendation_Button.clicked.connect(self.Developrs_recomendation)
        self.Reset_Energy_Button.clicked.connect(self.reset_Energy_spinBox)
        self.Reset_Pause_Button.clicked.connect(self.reset_Pause_doubleSpinBox)
        self.Reset_Phrase_Button.clicked.connect(self.reset_Phrase_doubleSpinBox)
        self.Reset_non_speaking_duration_Button.clicked.connect(self.reset_Non_speaking_daration_doubleSpinBox)
        # self.Reset_operation_timeout_Button.clicked.connect(self.reset_Operation_time_out_comboBox)

        self.Energy_spinBox.valueChanged.connect(self.settings_changed_)
        self.Pause_doubleSpinBox.valueChanged.connect(self.settings_changed_)
        self.Phrase_doubleSpinBox.valueChanged.connect(self.settings_changed_)
        self.Non_speaking_daration_doubleSpinBox.valueChanged.connect(self.settings_changed_)
        # self.Operation_time_out_comboBox.currentIndexChanged.connect(self.settings_changed_)
        
        self.MicSettings = QSettings('MicSettings')
        mic_list = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)

        micNameList = []
        for device in mic_list[:]:
            micNameList.append(device.deviceName())
        mics = []
        selected_mic_name = self.MicSettings.value('SelectedMic')
        for d in micNameList[:]:
            if d not in mics:
                mics.append(d)
                try:
                    if str(selected_mic_name) in str(d):
                        mic_name_to_select = d
                except Exception:
                    pass        
        self.comboBox.addItems(mics)        
        
        try:
            self.TimeOutDoubleSpinBox.setValue(int(int(self.MicSettings.value('TimeOut'))/1000))
            self.comboBox.setCurrentText(mic_name_to_select)
        except Exception as e:
            # print(e)
            pass    
        self.Manage_pushButton.clicked.connect(self.Open_Manager)

    # def reset_Operation_time_out_comboBox(self):
    #     self.Operation_time_out_comboBox.setCurrentText('None')
    def Open_Manager(self):
        os.system('c:\windows\system32\control.exe mmsys.cpl,,1')
    def reset_Non_speaking_daration_doubleSpinBox(self):
        self.Non_speaking_daration_doubleSpinBox.setValue(0.5)
    def reset_Phrase_doubleSpinBox(self):
        self.Phrase_doubleSpinBox.setValue(0.3)
    def reset_Pause_doubleSpinBox(self):
        self.Pause_doubleSpinBox.setValue(0.8)
    def reset_Energy_spinBox(self):
        self.Energy_spinBox.setValue(300)
    def Reset_all(self):
        self.Energy_spinBox.setValue(300)                       # 1
        self.Pause_doubleSpinBox.setValue(0.8)                  # 2
        self.Phrase_doubleSpinBox.setValue(0.3)                 # 3
        self.Non_speaking_daration_doubleSpinBox.setValue(0.5)  # 4
        # self.Operation_time_out_comboBox.setCurrentText('None') # 5
    def Developrs_recomendation(self):
        self.Energy_spinBox.setValue(300)                       # 1
        self.Pause_doubleSpinBox.setValue(0.3)                  # 2
        self.Phrase_doubleSpinBox.setValue(0.3)                 # 3
        self.Non_speaking_daration_doubleSpinBox.setValue(0.2)  # 4
        # self.Operation_time_out_comboBox.setCurrentText('None') # 5
        
        WM_APPCOMMAND = 0x319
        APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a
        APPCOMMAND_VOLUME_MIN = 0x09
        win32api.SendMessage(-1, 0x319, 0x30292, APPCOMMAND_MICROPHONE_VOLUME_UP * 0x10000)
    def Apply_func(self):
        try:
            miliSecs = (self.TimeOutDoubleSpinBox.value())*1000
            self.MicSettings.setValue('TimeOut', miliSecs)
            

            Energy = str(self.Energy_spinBox.value())
            Pause = str(self.Pause_doubleSpinBox.value())
            Phrase = (self.Phrase_doubleSpinBox.value())
            Non_speaking_daration = (self.Non_speaking_daration_doubleSpinBox.value())
            sr_mic_list = sr.Microphone.list_microphone_names() 
            mic_selecterd = self.comboBox.currentText()
            for m in sr_mic_list[:]:
                if m in mic_selecterd:
                    mic_to_select = m
                    
                    break

            mic_index_in_sr_mic_list = sr_mic_list.index(mic_to_select)
            if Phrase < Non_speaking_daration:
                msg = QMessageBox()
                msg.setStyleSheet("QMessageBox{\n"
                                "color: white;\n"
                                "background-color: rgb(108, 177, 223);\n"

                                "font: 12pt \"MS Shell Dlg 2\";\n"
                                "gridline-color: #EAEDED;\n"
                                "}")
                msg.setWindowTitle("Could'nt apply the settings!")
                msg.setText(f"Note that; \nPhrase Threshold can't be less then Non speaking duration.")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                return 


            # Operation_time_out = str(self.Operation_time_out_comboBox.currentText())
            self.settings_changed = False
            
            self.MicSettings.setValue('Non_speaking_daration', Non_speaking_daration)    
            self.MicSettings.setValue('Phrase', Phrase)    
            self.MicSettings.setValue('Pause', Pause)    
            self.MicSettings.setValue('Energy', Energy)    
            self.MicSettings.setValue('SelectedMic', mic_to_select) 
            self.MicSettings.setValue('mic_index_in_sr_mic_list', mic_index_in_sr_mic_list) 

            # self.MicSettings.setValue('Operation_time_out', Operation_time_out) 


            with open('.//Res//Recoard_settings.txt', "w") as RS:
                RS.write(f'{Energy}\n{Pause}\n{str(Phrase)}\n{str(Non_speaking_daration)}\n{"Operation_time_out"}\n{mic_index_in_sr_mic_list}\n{mic_to_select}')    
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Settings Applied.")
            msg.setText(f"Settings applied.\nNow you can press 'Ok' and close the window.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font: 12pt \"MS Shell Dlg 2\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Opps")
            msg.setText(f"{e}")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()    
        # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
        # os.execv(sys.executable, ['python'] + sys.argv)
    def Show_settings(self):
        self.show()    
    def settings_changed_(self):
        self.settings_changed = True 
    def closeEvent(self, event):
        if self.settings_changed == True:
            msg = QMessageBox()
            msg.setStyleSheet("QMessageBox{\n"
                            "color: white;\n"
                            "background-color: rgb(108, 177, 223);\n"

                            "font:75 12pt \"MS Shell Dlg 2l\";\n"
                            "gridline-color: #EAEDED;\n"
                            "}")
            msg.setWindowTitle("Q?")
            msg.setText("Don't you want to apply the changed settings?")
            msg.setIcon(QMessageBox.Question)
            butn = msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.close_msg_action)
            msg_exec = msg.exec_() 
        else:
            self.close()    
    def close_msg_action(self, i):
        if str(i.text()) == "&Yes":
            self.Apply_func()
        if str(i.text()) == "&No":
            pass
        if str(i.text()) == "&Cancel":
            return
        # QApplication. quit()  
        self.close()


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    ex = Options_UI() 
    ex.show()
    sys.exit(app.exec_())
    # sr_mic_list = sr.Microphone.list_microphone_names()
    # mic_list = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)
    # for device in mic_list[:]:
    #     print(device.deviceName())    
        # print(sr_mic_list)


    


    
