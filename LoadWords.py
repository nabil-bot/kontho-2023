# -*- coding:utf-8 -*-
import io

banglaDictionaryPath = './/Res//Dictionaries//BanglishList2.txt'
with io.open(banglaDictionaryPath, "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
wordsList = wordsSTR.split("|")

englaDictionaryPath = './/Res//Dictionaries//engla.txt' #  result.txt
with io.open(englaDictionaryPath, "r", encoding="utf-8") as wordTxt:
    wordsSTR = wordTxt.read()
englaList = wordsSTR.split("|")
# englaList = []

englishDictionaryPath = './/Res//Dictionaries//EnglishWords.txt'
with io.open(englishDictionaryPath, "r", encoding="utf-8") as wordTxt:
    EnglishWordsSTR = wordTxt.read()
EnglishwordsList = EnglishWordsSTR.split("|")

Word_list = []
for w in wordsList:
    wrd_array = w.split(",")
    banglaWrd = wrd_array[0]
    Word_list.append(banglaWrd)


AbbreviationsPath = './/Res//Abbreviations.txt'
with io.open(AbbreviationsPath, "r", encoding="utf-8") as RKS:
    abriStr = RKS.read()
abris = abriStr.split("\n")


englishLatter = "qwertyuiopasdfghjklzxcvbnm"
englishLatterUpper = englishLatter.upper()

englishAlphabets = []


englishNumbers = ["1","2","3","4","5","6","7","8","9","0"]
englishLatters = ["1","2","3","4","5","6","7","8","9","0"]
for l in range(26)[:]:
    englishLatters.append(englishLatter[l])
    englishLatters.append(englishLatterUpper[l])
    englishAlphabets.append(englishLatter[l])
    englishAlphabets.append(englishLatterUpper[l])

# print(englishAlphabets)

banglaAlphabates_str = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্"
banglaUnicodesStr = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্০১২৩৪৫৬৭৮৯"
banglaAlphabates = []
banglaUnicodesLatters = []
for i in range(len(banglaUnicodesStr)):
    banglaUnicodesLatters.append(banglaUnicodesStr[i])

for i in range(len(banglaAlphabates_str)):
    banglaAlphabates.append(banglaAlphabates_str[i])  

banglaNumbs = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "০"]
