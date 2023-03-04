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
# englaList = englaList[:36000]
# englaList = wordsList

englishDictionaryPath = './/Res//Dictionaries//EnglishWords.txt'
with io.open(englishDictionaryPath, "r", encoding="utf-8") as wordTxt:
    EnglishWordsSTR = wordTxt.read()
EnglishwordsList = EnglishWordsSTR.split("|")


# print("Before:")
# print(len(EnglishwordsList))

# wordsPath = './/Res//Dictionaries//words.txt'
# with io.open(wordsPath, "r", encoding="utf-8") as wordTxt:
#     wordsSTR = wordTxt.read()
# wordsList = wordsSTR.split("\n")
# print(f"number of new words: {len(wordsList)}")

# for w in wordsList:
#     if w not in EnglishwordsList and w.lower() not in EnglishwordsList and "-" not in w:
#         EnglishwordsList.append(w)

# print("after:")
# print(len(EnglishwordsList))
# EnglishwordsList.sort()

# stringToWrite = ""

# for w in EnglishwordsList:
#    stringToWrite += f"{w}|"

# stringToWrite = stringToWrite[:-1]

# with io.open(englishDictionaryPath, "w", encoding="utf-8") as wordTxt:
#     wordTxt.write(stringToWrite)

# print("finish!")










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


special_characters_of_keyboard = [
    "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"
]

englishNumbers = ["1","2","3","4","5","6","7","8","9","0"]
englishLatters = ["1","2","3","4","5","6","7","8","9","0"]
for l in range(26)[:]:
    englishLatters.append(englishLatter[l])
    englishLatters.append(englishLatterUpper[l])
    englishAlphabets.append(englishLatter[l])
    englishAlphabets.append(englishLatterUpper[l])



banglaAlphabates_str = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্"
banglaUnicodesStr = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্র্য্০১২৩৪৫৬৭৮৯"
banglaAlphabates = []
banglaUnicodesLatters = []
for i in range(len(banglaUnicodesStr)):
    banglaUnicodesLatters.append(banglaUnicodesStr[i])

for i in range(len(banglaAlphabates_str)):
    banglaAlphabates.append(banglaAlphabates_str[i])  

banglaNumbs = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "০"]

DefultThemePath = './/Res//DefultTheme.txt'
with io.open(DefultThemePath, "r", encoding="utf-8") as wordTxt:
    DefultTheme = wordTxt.read()

BlueThemePath = './/Res//BlueTheme.txt'
with io.open(BlueThemePath, "r", encoding="utf-8") as wordTxt:
    BlueTheme = wordTxt.read()   

YellowThemePath = './/Res//YellowTheme.txt'
with io.open(YellowThemePath, "r", encoding="utf-8") as wordTxt:
    YellowTheme = wordTxt.read()   


RedThemePath = './/Res//RedTheme.txt'
with io.open(RedThemePath, "r", encoding="utf-8") as wordTxt:
    RedTheme = wordTxt.read()  


BanglaThemePath = './/Res//BanglaStylesheet.txt'
with io.open(BanglaThemePath, "r", encoding="utf-8") as wordTxt:
    BanglaTheme = wordTxt.read()     

EnglishThemePath = './/Res//EnglishStylesheet.txt'
with io.open(EnglishThemePath, "r", encoding="utf-8") as wordTxt:
    EnglishTheme = wordTxt.read()         

getCaretPosPath = './/Res//getCaretPos.txt'
with io.open(getCaretPosPath, "r", encoding="utf-8") as wordTxt:
    getCaretPos_Script = wordTxt.read()            


