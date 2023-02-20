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


# def smertCompletor(word_soFar, the_word):
#     try:    
#         i = 0
#         # if len(word_soFar) <= len(the_word):
#         for x in range(len(the_word)):
#             try:
#                 if the_word[i] == word_soFar[i]:
#                     same_index = i
#                 else:
#                     break
#                 i += 1
#             except Exception as e:
#                 same_index = i

#         if len(word_soFar) <= len(the_word):
#             return_slot = len(word_soFar[same_index:]), the_word[same_index:]
#         else:    
#             return_slot = len(word_soFar[same_index+1:]), the_word[same_index+1:]

#         return return_slot
#     except Exception as e:
#         print(e)
#         print(f"word_soFar: {word_soFar}, the_word: {the_word}") 

# print(smertCompletor("ac", "academicians"))
# print(smertCompletor("academicians","ac"))



# laod table when scroll ================================

# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
# from PyQt5.QtCore import Qt

# class MainWindow(QMainWindow):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data
#         self.table = QTableWidget()
#         self.table.setColumnCount(1)
#         self.table.verticalScrollBar().valueChanged.connect(self.scrollEvent)
#         self.loadRows(0, 50)  # load the first 50 rows
#         self.setCentralWidget(self.table)
    
#     def loadRows(self, start, end):
#         for i in range(start, end):
#             if i >= len(self.data):
#                 break
#             item = QTableWidgetItem(self.data[i])
#             self.table.setItem(i, 0, item)

#     def scrollEvent(self, value):
#         # calculate the last row that is currently visible
#         lastVisibleRow = self.table.rowAt(self.table.viewport().height()) 
        
#         # if the last visible row is within a certain threshold of the end, load more rows
#         if lastVisibleRow >= self.table.rowCount() - 30:
#             self.table.setRowCount(self.table.rowCount() + 50)
#             self.loadRows(self.table.rowCount() - 50, self.table.rowCount())
    
# if __name__ == '__main__':
#     data = ['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7', 'word8', 'word9', 'word10', 'word11', 'word12', 'word13', 'word14', 'word15', 'word16', 'word17', 'word18', 'word19', 'word20']
#     app = QApplication([])
#     window = MainWindow(data)
#     window.show()
#     app.exec_()


# import io


# import re

# def has_consecutive_letters(word):
#     """Returns True if the given word has three or more consecutive occurrences of the same letter."""
#     pattern = r'(\w)\1\1'  # Matches any character (\w) that is repeated three times (\1 refers to the first group)
#     if re.search(pattern, word):
#         return True
#     else:
#         return False

# englishDictionaryPath = './/Res//Dictionaries//EnglishWords.txt'
# with io.open(englishDictionaryPath, "r", encoding="utf-8") as wordTxt:
#     EnglishWordsSTR = wordTxt.read()
# EnglishwordsList = EnglishWordsSTR.split("|")
# print(f"previously: {len(EnglishwordsList)}")


# oneHun_Path = './/Res//Dictionaries//wiki-100k.txt'
# with io.open(oneHun_Path, "r", encoding="utf-8") as wordTxt:
#     one_hunWordsSTR = wordTxt.read()

# one_hun_wordsList = one_hunWordsSTR.split("\n")

# toWrite = ''
# c=0
# new_wrd_list = []
# for w in one_hun_wordsList:
#     if w[0] != "#" and len(w) > 2 and w not in EnglishwordsList:
#         toWrite += f"{w}|"
#         c+=1

        
# print(f"Now: {c}")

# toWrite = toWrite[:-1]

# with io.open(englishDictionaryPath, "w", encoding="utf-8") as wordTxt:
#     wordTxt.write(toWrite)

from bs4 import BeautifulSoup
import requests, lxml


# Send a GET request to Google.com
# response = requests.get('https://www.google.com')

# cookies = response.cookies.get_dict()


headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  'q': 'ব্রাহ্মানবারিয়া',
  'hl': 'bn',
  'gl': 'bd'
}

html = requests.get('https://www.google.com/search?q=', headers=headers, params=params).text # , cookies=cookies
soup = BeautifulSoup(html, 'lxml')

# print(soup)
i_tag = soup.find('i')
if i_tag:
    text_in_i_tag = i_tag.get_text()
    print(text_in_i_tag)
# corrected_word = soup.select_one('a.gL9Hy').text
# corrected_word_link = f"https://www.google.com{soup.select_one('a.gL9Hy')['href']}"
# search_instead_for = soup.select_one('a.spell_orig').text
# search_instead_for_link = f"https://www.google.com{soup.select_one('a.spell_orig')['href']}"
# print(f'\n\nSearch instead: {search_instead_for}\n{search_instead_for_link}') # {corrected_word} {corrected_word_link}


