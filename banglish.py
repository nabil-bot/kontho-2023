# -*- coding:utf-8 -*-

import io
from LoadWords import Word_list, englaList


layout_dictionary1 = {"ক":"ko","খ":"kho","গ":"go","ঘ":"gho","ঙ":"Ngo","চ":"co","ছ":"cho","জ":"jo", "ঝ":"jho","ঞ":"NGo", "ট":"To","ঠ":"Tho","ড":"Do","ঢ":"Dho","ণ":"No","ত":"to", "থ":"tho", "দ":"do", "ধ":"dho","ন":"no","প":"po","ফ":"fo","ব":"bo","ভ":"bho","ম":"mo","য":"Zo","র":"ro","ল":"lo","শ":"sho","ষ":"Sho","স":"so","হ":"ho","ড়":"Ro","ঢ়":"Rho","য়":"yo","ৎ":"THo","ং":"ng","ঃ":"","ঁ":"","অ":"o","আ":"a","ই":"i","ঈ":"Ei", "উ":"u","ঊ":"U","ঋ":"Ri","এ":"e","ঐ":"Oi","ও":"O","ঔ":"OU","া":"a","ি":"i","ী":"I","ু":"u","ূ":"U","ৃ":"ri","ে":"e","ৈ":"Oi","ো":"O","ৌ":"Ou","্":"", ",":"", "।":"", " ":" "}
kal_list = ["া", "ি", "ী", "ে", "ু", "ূ", "ৃ", "ো", "ৌ", "ৈ"] 




# with io.open("result.txt", 'r', encoding="utf-8") as f:
#     words_str = f.read()
engla_list = englaList

# for w in engla_list:
#     Word_list.append(w)
jointWord = False
def jointWordSpliter(word):
    firstWord = ""
    secondWord = ""
    thirdWord = ""
    jointWord = False
    for i in range(len(word))[:]:
        firstWord = word[:i]
        if firstWord != word and i>1:   
            if firstWord in Word_list:
                secondWord = word[i:] 

                # banglish = convert_to_banglish(firstWord)+convert_to_banglish(secondWord)
                # return banglish
                if len(secondWord) > 1 and secondWord in Word_list:
                    banglish = convert_to_banglish(firstWord)+convert_to_banglish(secondWord)
                    return banglish
# def jointWordSpliter(word):
#     # words_list = []
#     # s = 0
#     # wholeWord = ""
#     # for i in range(len(word))[:]:
#     #     CurrentWord = word[s:i]
#     #     if CurrentWord != word and len(CurrentWord)>3:   
#     #         if CurrentWord in Word_list:
#     #             words_list.append(CurrentWord)
#     #             wholeWord += convert_to_banglish(CurrentWord)
#     #             s = i
#     # restOf = word[s:]
#     # words_list.append(restOf)  
#     # wholeWord += convert_to_banglish(restOf)          
#     # # print(words_list) 
#     # return wholeWord      
#     w_list = []
#     for wrd in Word_list[:]:
#         if wrd in word and wrd != word and len(wrd) > 1:
#             w_list.append(wrd)
#     return  w_list      


          

def convert_to_banglish(bangla_word):

    banglish = ""
    former_previous_latter = ""
    previous_latter = ""
    former_previous_value = ""
    previous_value = ""
    former_previous_former_previous_latter = ""
    previous_former_previous_latter = ""
    P_F_P_F_P_L = ""
    try:    
        for i in range(len(bangla_word))[:]:
            latter =  bangla_word[i]

            if latter in kal_list and banglish[-1] in ["o", "O"]: # nothibhukoto
                banglish = banglish[:-1]
            try:    
                if latter == "্" and bangla_word[i+1] not in ["য", "র", "য", "ব", "ম"]:         
                    banglish = banglish[:-1]
                    if previous_latter != "র": # makeing sure this not fola or ref of juttekho
                        # print(f"former_previous_latter:{former_previous_latter}")
                        if former_previous_latter not in ["ঘ", "ং", "ঙ", "ছ", "ঝ", "ঞ", "ঠ", "ঢ", "থ","শ","ষ"]+kal_list: # jukto borno ertra o remover    প্রধানমন্ত্রী   prodhanomon trI
                            custom_banglish = banglish[:-3]
                            custom_banglish_last = custom_banglish[-1]
                            if custom_banglish_last == "o" and previous_former_previous_latter not in ["অ"]:
                                first_part = custom_banglish[:-1]
                                second_part = banglish[-3:]
                                banglish = first_part+second_part
            except Exception as e :
                # print(e)
                pass                    
                            # print(f"->=====-> {first_part}+{second_part}")
            i_f_l = len(bangla_word) - i # index from last

            try:
                if len(bangla_word) > 5:
                    if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and i_f_l > 2 and previous_former_previous_latter != "্":   # perpectly working with the list
                        custom_banglish = banglish[:-1]
                        custom_banglish_last = custom_banglish[-1]
                        if custom_banglish_last == "o":
                            custom_banglish = custom_banglish[:-1]
                            banglish = custom_banglish+banglish[-1] 
                else:
                    if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and previous_former_previous_latter != "্":   # perpectly working with the list
                        custom_banglish = banglish[:-1]
                        custom_banglish_last = custom_banglish[-1]
                        if custom_banglish_last == "o":
                            custom_banglish = custom_banglish[:-1]
                            banglish = custom_banglish+banglish[-1]             
            except Exception as e:
                # print(e) 
                pass             
            
            try:
                m = i
                if m+1 <= len(bangla_word) and latter == "র":
                     
                    if bangla_word[m+1] == "্": 
                                                    # ref
                        second_part =  banglish[-2:]  
                        first_part = banglish[0:-2]
                        last_v = first_part[-1] 
                        if last_v == "o":    
                            
                            if banglish.index("o") != 0:
                                
                                custom_first_part = first_part[:-1] 
                                banglish = custom_first_part+second_part

            except Exception as e:
                pass                

            if latter == "্" and previous_latter == "র" and banglish[-1] == "o":
               banglish = banglish[:-1] 

            try:        
                value = layout_dictionary1[latter]
            except Exception:
                pass
                print(f"value error(latter):{latter}")    
            if latter == "ষ" and previous_latter == "্" and former_previous_latter == "ক":
                try:    
                    last_value = banglish[-1]
                except Exception:
                    last_value = ""   
                if last_value == "o":     
                    banglish = banglish[:-1]
                value = "kho"

            if previous_latter == "্" and former_previous_latter != "র" and latter in ["র", "ব", "ম", "য"]: # this block is for fola #  ro is for ref
                # print(f'latter: {latter}')
                if latter == "র":
                    # print("in if")
                    banglish = banglish[:-1]
                    pass
                if latter == "ব" or latter == "ম": 
                    banglish = banglish[:-1]
                    value = "o"
                if latter == "য":
                    
                    three_latter_valued = ["ধ", "ষ", "ল", "ব", "ক"]

                    if i < 3:
                        banglish = banglish[:-1] 
                        value =  previous_value+"aa"  
                    else:
                        mid_prt = banglish[-3]   
                        second_part = banglish[-2:]
                        mid2 = second_part[0]
                        banglish = banglish[0:-3]
                        value = mid_prt+mid2+second_part
 
            banglish += value 
            former_previous_value = previous_value
            previous_value = value
            
            F_P_F_P_F_P_L = P_F_P_F_P_L
            P_F_P_F_P_L = former_previous_former_previous_latter
            former_previous_former_previous_latter = previous_former_previous_latter   # জনসম্পৃক্ততা
            previous_former_previous_latter = former_previous_latter
            former_previous_latter = previous_latter
            previous_latter = latter
        
    except Exception as e:
        banglish +=layout_dictionary1[latter]
    try:    
        last_value = banglish[-1]
    except Exception:
        last_value = ""    


    if last_value == "o" and "krito" not in banglish and former_previous_latter not in ["্"] and last_value != "O" : # and former_previous_latter != "ি" স্থানীয়
        kar_list = ["ি", "ী", "ং", "ো"]
        if former_previous_latter in kar_list and previous_former_previous_latter not in kar_list and previous_latter in ["য়", "শ", "ট", "ল"]:
            pass
        elif former_previous_latter == "্" and former_previous_former_previous_latter not in ["া", "ু","ি", "ী" , "ে"]:
            pass
        elif previous_latter == "ত" and former_previous_latter in ["ি", "ী"]:
            pass
        elif previous_latter in ["হ"]:
            pass
        else:
            banglish = banglish[:-1]
    

    if len(banglish) > 4:        
        
        if last_value in ["a", "e"] and banglish[-3] == 'o' and former_previous_former_previous_latter != "্":
            banglish = banglish[0:-3]+banglish[-2:]


    # banglish = banglish.replace("gg", "g")
    banglish = banglish.replace("aaa", "aa")
    banglish = banglish.replace("aa", "a")
    banglish = banglish.replace("hh", "h")
    banglish = banglish.replace("NG", "N")
    banglish = banglish.replace("ea", "O")
    banglish = banglish.replace("Oa", "a")
    banglish = banglish.replace("Ngk", "Nk")
    return(banglish)       

def convert_to_banglish_sentence(sentence):
    words = sentence.split("|")
    txt_to_save = "" 
    for word in words:
        convertion = jointWordSpliter(word) 
        
        if convertion != None:
            banglish = convertion
        else:
            banglish = convert_to_banglish(word) 
        # banglish2Dic = {"sh":"S", "Ngk":"Nk", "kh": "K"}
        # for x, y in banglish2Dic.items():
        #     banglish2 = banglish.replace(x,y)
        
        txt_to_save += f"{word},{banglish}|"
    
    prefix = "ও,o|ো,o|া,a|ি,i|ী,i|ু,u|ূ,u|ৃ,ri|ে,e|ৈ,oi|ৌ,ou|"
    
    textToPut = (prefix+txt_to_save).replace("|,|", "|")
    
    with io.open("BanglishList2.txt", 'w', encoding="utf-8") as f:
        f.write(textToPut)
        # print(banglish)
    # programName = "notepad.exe"
    # fileName = "banglishPreview.txt"
    # sp.Popen([programName, fileName])

# convert_to_banglish_sentence(words_str) 
# print(convert_to_banglish("একাত্তর"))
# print(convert_to_banglish("অঘটন"))


# def Sorting(lst):
#     lst2 = sorted(lst, key=len)
#     return lst2

# print(Sorting(jointWordSpliter("প্রধানমন্ত্রী"))) # ঘটনপটীয়সী প্রধানমন্ত্রী অঘটনঘটনপটীয়সী
# print("check!")




# def convertToEngla(EnglishText):
#     englaText = ""
#     return englaText