# -*- coding:utf-8 -*-

def smertCompletor(word_soFar, the_word):
    try:    
        for i in range(len(the_word)):
            try:
                if the_word[i] == word_soFar[i]:
                    pass
                else:
                    same_index = i
                    break
            except Exception:
                same_index = i  
                return len(word_soFar[same_index-1:]), the_word[same_index:]
        return len(word_soFar[same_index:]), the_word[same_index:]
    except Exception as e:
        print(i)
        print(e)
        print(f"word_soFar: {word_soFar}, the_word: {the_word}") 

print(smertCompletor("Av", "Avg"))
