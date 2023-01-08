# -*- coding:utf-8 -*-
import io

banglaDictionaryPath = './/Res//Dictionaries//BanglishList2.txt'
with io.open(banglaDictionaryPath, "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
wordsList = wordsSTR.split("|")

englaDictionaryPath = './/Res//Dictionaries//result.txt'
with io.open(englaDictionaryPath, "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
englaList = wordsSTR.split("|")

englishDictionaryPath = './/Res//Dictionaries//EnglishWords.txt'
with io.open(englishDictionaryPath, "r", encoding="utf-8") as wordTxt:
    EnglishWordsSTR = wordTxt.read()
EnglishwordsList = EnglishWordsSTR.split("|")

with io.open(".//Res//Dictionaries//SoreOwords.txt", 'r', encoding="utf-8") as f:
    words_str = f.read()
Word_list = words_str.split("|")

AbbreviationsPath = './/Res//Abbreviations.txt'
with io.open(AbbreviationsPath, "r", encoding="utf-8") as RKS:
    abriStr = RKS.read()
abris = abriStr.split("\n")


englishLatter = "qwertyuiopasdfghjklzxcvbnm"
englishLatterUpper = englishLatter.upper()



englishLatters = ["1","2","3","4","5","6","7","8","9","0"]
for l in range(26)[:]:
    englishLatters.append(englishLatter[l])
    englishLatters.append(englishLatterUpper[l])
banglaAlphabates = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্"
banglaUnicodesStr = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্০১২৩৪৫৬৭৮৯"
banglaUnicodesLatters = []
for i in range(len(banglaUnicodesStr)):
    banglaUnicodesLatters.append(banglaUnicodesStr[i])

banglaNumbs = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "০"]
