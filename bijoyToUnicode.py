# import time
# import keyboard as kb2


# kb2.block_key(15)

# time.sleep(10)


# class MultiCursorPlainTextEdit(QPlainTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#     def mousePressEvent(self, event):
#         if event.modifiers() & Qt.AltModifier:
#             cursor = self.cursorForPosition(event.pos())
#             self.setTextCursor(cursor)
#         else:
#             super().mousePressEvent(event)


# import os
# import sqlite3
# import win32crypt

# def get_cookies_from_chrome():
#     cookie_file = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Default\Cookies'
#     conn = sqlite3.connect(cookie_file)
#     sql = "select host_key, name, encrypted_value from cookies where host_key like '%google%'"
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     cookies = {}
#     for host_key, name, encrypted_value in results:
#         decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
#         cookies[name] = decrypted_value.decode('utf-8')
#     return cookies

# def save_cookies_to_txt(cookies):
#     with open("cookies.txt", "w") as f:
#         for name, value in cookies.items():
#             f.write(f"{name}={value}\n")

# cookies = get_cookies_from_chrome()
# save_cookies_to_txt(cookies)


def smertCompletor(word_soFar, the_word):
    try:    
        i = 0
        # if len(word_soFar) <= len(the_word):
        for x in range(len(the_word)):
            try:
                if the_word[i] == word_soFar[i]:
                    same_index = i
                else:
                    break
                i += 1
            except Exception as e:
                same_index = i

        if len(word_soFar) <= len(the_word):
            return_slot = len(word_soFar[same_index:]), the_word[same_index:]
        else:    
            return_slot = len(word_soFar[same_index+1:]), the_word[same_index+1:]

        return return_slot
    except Exception as e:
        print(e)
        print(f"word_soFar: {word_soFar}, the_word: {the_word}") 

print(smertCompletor("ac", "academicians"))
print(smertCompletor("academicians","ac"))
