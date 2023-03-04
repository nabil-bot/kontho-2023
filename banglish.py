# -*- coding:utf-8 -*-

import io
from LoadWords import Word_list, englaList
import traceback

layout_dictionary1 = {"ক":"ko","খ":"kho","গ":"go","ঘ":"gho","ঙ":"Ngo","চ":"co","ছ":"cho","জ":"jo", "ঝ":"jho","ঞ":"NGo", "ট":"To","ঠ":"Tho","ড":"Do","ঢ":"Dho","ণ":"No","ত":"to", "থ":"tho", "দ":"do", "ধ":"dho","ন":"no","প":"po","ফ":"fo","ব":"bo","ভ":"bho","ম":"mo","য":"Zo","র":"ro","ল":"lo","শ":"sho","ষ":"Sho","স":"so","হ":"ho","ড়":"Ro","ঢ়":"Rho","য়":"yo","ৎ":"THo","ং":"ng","ঃ":"","ঁ":"","অ":"o","আ":"a","ই":"i","ঈ":"Ei", "উ":"u","ঊ":"U","ঋ":"Ri","এ":"e","ঐ":"Oi","ও":"O","ঔ":"OU","া":"a","ি":"i","ী":"I","ু":"u","ূ":"U","ৃ":"ri","ে":"e","ৈ":"Oi","ো":"O","ৌ":"Ou","্":"", ",":"", "।":"", " ":" "}
kal_list = ["া", "ি", "ী", "ে", "ু", "ূ", "ৃ", "ো", "ৌ", "ৈ"] 

debug_mode = False

engla_list = englaList

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

            if latter in kal_list and banglish[-1] in ["o", "O"]: # nothibhukoto  # if count 1
                banglish = banglish[:-1]
                condition = 1
            try:    
                if latter == "্" and bangla_word[i+1] not in ["য", "র", "য", "ব", "ম"]:     # if count 2    
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

                                condition = 2
            except Exception as e :
                # print(e)
                pass                    
                            # print(f"->=====-> {first_part}+{second_part}")
            i_f_l = len(bangla_word) - i # index from last

            # try:  
            #     if len(bangla_word) > 5:
            #         if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and i_f_l > 2 and previous_former_previous_latter != "্":   # if count 3
            #             custom_banglish = banglish[:-1]
            #             custom_banglish_last = custom_banglish[-1]
            #             if custom_banglish_last == "o":
            #                 custom_banglish = custom_banglish[:-1]
            #                 banglish = custom_banglish+banglish[-1] 

            #                 condition = 3
            #     else:
            #         if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and previous_former_previous_latter != "্":    # if count 4
            #             custom_banglish = banglish[:-1]
            #             custom_banglish_last = custom_banglish[-1]
            #             if custom_banglish_last == "o":
            #                 custom_banglish = custom_banglish[:-1]
            #                 banglish = custom_banglish+banglish[-1]  

            #                 condition = 4           
            # except Exception as e:
            #     # print(e) 
            #     pass             
            
            try:
                m = i
                if m+1 <= len(bangla_word) and latter == "র": # if count 5
                     
                    if bangla_word[m+1] == "্": 
                                                    # ref
                        second_part =  banglish[-2:]  
                        first_part = banglish[0:-2]
                        last_v = first_part[-1] 
                        if last_v == "o":    
                            
                            if banglish.index("o") != 0:
                                
                                custom_first_part = first_part[:-1] 
                                banglish = custom_first_part+second_part

                                condition = 5

            except Exception as e:
                pass                

            if latter == "্" and previous_latter == "র" and banglish[-1] == "o": # if count 6
               banglish = banglish[:-1] 
               condition = 6

            try:        
                value = layout_dictionary1[latter]
                condition = "v"
            except Exception:
                pass
                print(f"value error(latter):{latter}")    
            if latter == "ষ" and previous_latter == "্" and former_previous_latter == "ক": # if count 7
                try:    
                    last_value = banglish[-1]
                except Exception:
                    last_value = ""   
                if last_value == "o":     
                    banglish = banglish[:-1]
                value = "kho"

                condition = 7

            if previous_latter == "্" and former_previous_latter != "র" and latter in ["র", "ব", "ম", "য"]: # this block is for fola #  ro is for # if count 8
                # print(f'latter: {latter}')
                if latter == "র":
                    # print("in if")
                    banglish = banglish[:-1]
                    pass
                if latter == "ব": 
                    banglish = banglish[:-1]
                    value = "o"
                if latter == "ম":
                    banglish = banglish[:-1]
                    if former_previous_latter == "দ":
                        value = "do"
                    else:
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
                condition = 8        
 
            banglish += value 

            try:    
                print(f"index:{i},condition = {condition}, {banglish}")
            except Exception:
                print(latter)
                pass    
            former_previous_value = previous_value
            previous_value = value
            
            F_P_F_P_F_P_L = P_F_P_F_P_L
            P_F_P_F_P_L = former_previous_former_previous_latter
            former_previous_former_previous_latter = previous_former_previous_latter   # জনসম্পৃক্ততা
            previous_former_previous_latter = former_previous_latter
            former_previous_latter = previous_latter
            previous_latter = latter
        
    except Exception as e:
        # print(traceback.format_exc())
        banglish +=layout_dictionary1[latter]
    try:    
        last_value = banglish[-1]
    except Exception:
        last_value = ""    


    if last_value == "o" and "krito" not in banglish and former_previous_latter not in ["্"] and last_value != "O" : # and former_previous_latter != "ি" if count 8
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
    

    if len(banglish) > 4:       # this cut   
        
        if last_value in ["a", "e"] and banglish[-3] == 'o' and former_previous_former_previous_latter != "্": # if count 8 
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
        
        # txt_to_save += f"{word},{banglish}|"
        return banglish
    
    # prefix = "ও,o|ো,o|া,a|ি,i|ী,i|ু,u|ূ,u|ৃ,ri|ে,e|ৈ,oi|ৌ,ou|"
    
    # textToPut = (prefix+txt_to_save).replace("|,|", "|")
    
    # with io.open("BanglishList2.txt", 'w', encoding="utf-8") as f:
    #     f.write(textToPut)
        # print(banglish)
    # programName = "notepad.exe"
    # fileName = "banglishPreview.txt"
    # sp.Popen([programName, fileName])


# print(convert_to_banglish_sentence(wrd))
# print(convert_to_banglish(wrd))
# print(convert_to_banglish("অন্তরঙ্গতা"))

def updateBanglish(Word_list):
    str_to_save = ""
    for wrd in Word_list:
        wrd_array = wrd.split(",")
        banglaWord = wrd_array[0]
        banglish = convert_to_banglish(banglaWord)
        str_to_save += f"{banglaWord},{banglish}|"
    with io.open("BanglishList2.txt", "w", encoding="utf-8") as file:
        file.write(str_to_save)      

# updateBanglish(Word_list)




def convert_to_banglish_old_algo(bangla_word):
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

            if latter in kal_list and banglish[-1] in ["o", "O"]: # nothibhukoto  # if count 1
                banglish = banglish[:-1]
                condition = 1
            try:    
                if latter == "্" and bangla_word[i+1] not in ["য", "র", "য", "ব", "ম"]:     # if count 2    
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

                                condition = 2
            except Exception as e :
                # print(e)
                pass                    
                            # print(f"->=====-> {first_part}+{second_part}")
            i_f_l = len(bangla_word) - i # index from last

            try:  
                if len(bangla_word) > 5:
                    if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and i_f_l > 2 and previous_former_previous_latter != "্":   # if count 3
                        custom_banglish = banglish[:-1]
                        custom_banglish_last = custom_banglish[-1]
                        if custom_banglish_last == "o":
                            custom_banglish = custom_banglish[:-1]
                            banglish = custom_banglish+banglish[-1] 

                            condition = 3
                else:
                    if latter in ["া", "ু","ি", "ী" , "ে"] and i>2 and previous_former_previous_latter != "্":    # if count 4
                        custom_banglish = banglish[:-1]
                        custom_banglish_last = custom_banglish[-1]
                        if custom_banglish_last == "o":
                            custom_banglish = custom_banglish[:-1]
                            banglish = custom_banglish+banglish[-1]  

                            condition = 4           
            except Exception as e:
                # print(e) 
                pass             
            
            try:
                m = i
                if m+1 <= len(bangla_word) and latter == "র": # if count 5
                     
                    if bangla_word[m+1] == "্": 
                                                    # ref
                        second_part =  banglish[-2:]  
                        first_part = banglish[0:-2]
                        last_v = first_part[-1] 
                        if last_v == "o":    
                            
                            if banglish.index("o") != 0:
                                
                                custom_first_part = first_part[:-1] 
                                banglish = custom_first_part+second_part

                                condition = 5

            except Exception as e:
                pass                

            if latter == "্" and previous_latter == "র" and banglish[-1] == "o": # if count 6
               banglish = banglish[:-1] 
               condition = 6

            try:        
                value = layout_dictionary1[latter]
                condition = "v"
            except Exception:
                pass
                print(f"value error(latter):{latter}")    
            if latter == "ষ" and previous_latter == "্" and former_previous_latter == "ক": # if count 7
                try:    
                    last_value = banglish[-1]
                except Exception:
                    last_value = ""   
                if last_value == "o":     
                    banglish = banglish[:-1]
                value = "kho"

                condition = 7

            if previous_latter == "্" and former_previous_latter != "র" and latter in ["র", "ব", "ম", "য"]: # this block is for fola #  ro is for # if count 8
                # print(f'latter: {latter}')
                if latter == "র":
                    # print("in if")
                    banglish = banglish[:-1]
                    pass
                if latter == "ব": 
                    banglish = banglish[:-1]
                    value = "o"
                if latter == "ম":
                    banglish = banglish[:-1]
                    if former_previous_latter == "দ":
                        value = "do"
                    else:
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
                condition = 8        
 
            banglish += value 
            # try:    
            #     print(f"index:{i},condition = {condition}, {banglish}")
            # except Exception:
            #     print(latter)
            #     pass    
            former_previous_value = previous_value
            previous_value = value
            
            F_P_F_P_F_P_L = P_F_P_F_P_L
            P_F_P_F_P_L = former_previous_former_previous_latter
            former_previous_former_previous_latter = previous_former_previous_latter   # জনসম্পৃক্ততা
            previous_former_previous_latter = former_previous_latter
            former_previous_latter = previous_latter
            previous_latter = latter
        
    except Exception as e:
        # print(traceback.format_exc())
        banglish +=layout_dictionary1[latter]
    try:    
        last_value = banglish[-1]
    except Exception:
        last_value = ""    


    if last_value == "o" and "krito" not in banglish and former_previous_latter not in ["্"] and last_value != "O" : # and former_previous_latter != "ি" if count 8
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
    

    if len(banglish) > 4:       # this cut   
        
        if last_value in ["a", "e"] and banglish[-3] == 'o' and former_previous_former_previous_latter != "্": # if count 8 
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

# print(convert_to_banglish_old_algo("হয়রান")) 


wrd = "তত্ত্বাবধায়ক"

def main_banglish_converter(wrd):
    conv_1  = convert_to_banglish(wrd)
    conv_2 = convert_to_banglish_sentence(wrd)
    conv_3 = convert_to_banglish_sentence(wrd)
    return_list = []
    for w in [conv_1,conv_2,conv_3]:
        if w not in return_list:
            return_list.append(w)
    else:
        return [conv_1]
# print(main_banglish_converter(wrd))