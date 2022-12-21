# -*- coding:utf-8 -*-
bangla_latters_str = "ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য র ল শ ষ স হ ড় ঢ় য় ৎ ং ঃ ঁ"
bangla_latters_list = bangla_latters_str.split(" ")

bijoy_str = "K L M N O P Q R S T U V W X Y Z _ ` a b c d e f g h i j k l m n o p q r s t"
bijoy_latters = bijoy_str.split(" ")

dic_str = ""
index = 0
# for i in range(len(bangla_latters_list))[:]:
#     try:    
#         dic_str += f"'{bangla_latters_list[index]}' : '{bijoy_latters[index]}', "
#         index += 1
#     except Exception:
#         pass    

# print(dic_str) 

dictionary = {'ক' : 'K', 'খ' : 'L', 'গ' : 'M', 'ঘ' : 'N', 'ঙ' : 'O', 'চ' : 'P', 'ছ' : 'Q', 'জ' : 'R', 'ঝ' : 'S', 'ঞ' : 'T', 'ট' : 'U', 'ঠ' : 'V', 'ড' : 'W', 'ঢ' : 'X', 'ণ' : 'Y', 'ত' : 'Z', 'থ' : '_', 'দ' : '`', 'ধ' : 'a', 'ন' : 'b', 'প' : 'c', 'ফ' : 'd', 'ব' : 'e', 'ভ' : 'f', 'ম' : 'g', 'য' : 'h', 'র' : 'i', 'ল' : 'j', 'শ' : 'k', 'ষ' : 'l', 'স' : 'm', 'হ' : 'n', 'ড়' : 'o', 'ঢ়' : 'p', 'য়' : 'q', 'ৎ' : 'r', 'ং' : 's', 'ঃ' : 't', 'ঁ':'u'}


word = "nabil"
if "abc" in word:
    print("gfd")