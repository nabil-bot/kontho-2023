import io
import pyperclip

with io.open("SoreOwords.txt", 'r', encoding="utf-8") as f:
        words_str = f.read()
list_ = words_str.split("|")
print(f"Before words num:{len(list_)}; total length:{len(words_str)}")


def Read_english_words():
    with io.open("En2.txt", 'r', encoding="utf-8") as f:
        E_words_str = (f.read()).lower()
    list_e = E_words_str.split('\n')
    print(len(list_e))
    to_append_str = ""
    for word in list_e:
        to_append_str += f"{word}|"
    with io.open("EnglishWords.txt", 'w', encoding="utf-8") as f:
        f.write(to_append_str) 
# Read_english_words()           
def filter_word(word):
    word = word.replace(' ', "")
    word = word.replace('‘', "")
    word = word.replace('’', "")
    word = word.replace('।', "")
    word = word.replace(',', "")


    bangla_latters_str = "কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ্ক্ষঙ্কঙ্গজ্ঞঞ্চঞ্ছণ্ডহ্মষ্ণত্তঞ্জ্য্রঅআইঈউঊঋএঐওঔািীুূৃেৈোৌ"
    bangla_latters_list = [] 
    for i in range(len(bangla_latters_str)):
        bangla_latters_list.append(bangla_latters_str[i])
    filtered_word = ""
    for i in range(len(word)):
        if word[i] in bangla_latters_list:
            filtered_word += word[i]
        else:
            break
    return filtered_word 

def filter_text_list(words_str):
    words =  words_str.split("|")    

    custom_word_list = []

    for word in words:
        filtered_word = filter_word(word)
        if filtered_word not in custom_word_list:
            custom_word_list.append(filtered_word)

    custom_words_str = ""

    for word in custom_word_list:
        custom_words_str += f"{word}|"

    print(f"After words num:{len(custom_word_list)}; total length:{len(custom_words_str)}")


    with io.open("SoreOwords.txt", 'w', encoding="utf-8") as f:
        f.write(custom_words_str)

    print("finished!")  

def add_new_words(words_str):
    main_words_list = list_ 
    adding_list = []
    words_list_given = words_str.split(" ")
    for word in words_list_given[:]:
        filtered_word = filter_word(word)
        if filtered_word not in main_words_list and filtered_word not in adding_list and filtered_word != "":
            adding_list.append(filtered_word)

    custom_words_str = ""

    for word in adding_list:
        custom_words_str += f"|{word}"

    print(f"After Words num:{len(main_words_list) + len(adding_list)}; total length:{len(custom_words_str)}")
    print(f"New Words:{len(adding_list)} , new_words:{adding_list}")
    with io.open("SoreOwords.txt", 'a', encoding="utf-8") as f:
        f.write(custom_words_str)
    print("finish!") 

def search_word(word):
    if word in list_:
        print(f"index_of_the_word:{list_.index(word)}")
    else:
        print("The word is not found!")    

# filter_text_list(words_str)       
# add_new_words(pyperclip.paste())
add_new_words("প্রধানমন্ত্রী")

# search_word("হামলার")

