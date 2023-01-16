# from pywinauto import desktop
import time

time.sleep(5)
# caret_pos = desktop.Caret().position()
# print(caret_pos)
# import ctypes

# def get_caret_pos():
#     class POINT(ctypes.Structure):
#         _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
#     point = POINT()
#     ctypes.windll.user32.GetCaretPos(ctypes.byref(point))
#     return point.x, point.y

# print(get_caret_pos())

from pywinauto import application
# app = application.Application().connect(title_re=".*")
from pywinauto import findwindows
handle = findwindows.find_windows(title='*p1 - Notepad')[0]
app = application.Application().connect(handle=handle)


# app = application.Application().connect(title='*p1 - Notepad')

dlg = app.top_window()
caret_pos = dlg.caret_coordinates()
print(caret_pos)
