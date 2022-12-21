#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
command=(pyinstaller --noconfirm --onefile --console --icon "C:/Users/ui/3D Objects/Kontho reboot/Uis/Imgs/kontho ico.ico"  "C:/Users/ui/3D Objects/Kontho reboot/Main.py")
Run, cmd.exe
Sleep, 100
Clipboard = %command%
Send, ^v
Sleep, 100
send, {Enter}
Return
