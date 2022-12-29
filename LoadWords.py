# -*- coding:utf-8 -*-
import io

with io.open('BanglishList2.txt', "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
wordsList = wordsSTR.split("|")

with io.open('result.txt', "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
englaList = wordsSTR.split("|")

with io.open('EnglishWords.txt', "r", encoding="utf-8") as wordTxt:
    EnglishWordsSTR = wordTxt.read()
EnglishwordsList = EnglishWordsSTR.split("|")

englishLatter = "qwertyuiopasdfghjklzxcvbnm"
englishLatterUpper = englishLatter.upper()

englishLatters = []
for l in range(26)[:]:
    englishLatters.append(englishLatter[l])
    englishLatters.append(englishLatterUpper[l])


# print(englishLatters)
