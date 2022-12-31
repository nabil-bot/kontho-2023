from time import time
import win32api
import time


# Get the caret position
import win32gui


time.sleep(5)
# Get the caret position

active_window = win32gui.GetActiveWindow()

# Give the focus to the active window
win32gui.SetFocus(active_window)
# win32gui.SetCaretPos(100, 100)
pos = win32gui.GetCaretPos()

# Print the caret position
print(pos)