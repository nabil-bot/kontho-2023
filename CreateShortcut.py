import os, winshell

from win32com.client import Dispatch
import os

from pathlib import Path
home = str(Path.home())


def creat_shortcut(): # this function will add a shortcut at the start menu file
    path = os.path.join(home, "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Kontho.lnk")
    target = os.path.join(os.path.abspath(os.getcwd()), "Kontho.exe")
    wDir = os.path.abspath(os.getcwd())
    icon = os.path.join(os.path.abspath(os.getcwd()), "Kontho.exe")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()
# creat_shortcut(Installation_path)