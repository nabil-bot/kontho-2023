# -*- coding:utf-8 -*-

import transliterate

def english_to_bangla_phonetics(word):
    return transliterate.translit(word, 'bn', reversed=True)

print(english_to_bangla_phonetics("transliterate"))    

