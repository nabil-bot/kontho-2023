word_soFar = "প্রধান্মন্ত্রি"
the_word = "অঘটনঘটনপটীয়সী" 

def smertCompletor(word_soFar, the_word):
  for i in range(len(the_word))[:]:
    if the_word[i] == word_soFar[i]:
      pass
    else:
      same_index = i
      break
  return len(word_soFar[same_index:]), the_word[same_index:]   

times_to_tap_backspace, restOfWord = smertCompletor(word_soFar, the_word) 
print(times_to_tap_backspace)
print(restOfWord)

