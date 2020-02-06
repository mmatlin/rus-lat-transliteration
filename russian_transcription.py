import re, sys
from codecs import decode, encode

# Create transcription dict
rus_to_lat = {"а": "a",
              "б": "b",
              "в": "v",
              "г": "g",
              "д": "d",
              "е": chr(0x30c) + "e", # case for consonant then е
              "^е": "je", # case for word start/vowel/ъ then е
              "ё": chr(0x30c) + "o",
              "^ё": "jo",
              "ж": "ź",
              "з": "z",
              "и": "i",
              "й": "j",
              "к": "k",
              "л": "l",
              "м": "m",
              "н": "n",
              "о": "o",
              "п": "p",
              "р": "r",
              "с": "s",
              "т": "t",
              "у": "u",
              "ф": "f",
              "х": "h",
              "ц": "c",
              "ч": "ć",
              "ш": "ś",
              "щ": "s̋",
              "ъ": "'",
              "ы": "y",
              "ь": "̌",
              "э": "e",
              "ю": chr(0x30c) + "u",
              "^ю": "ju",
              "я": chr(0x30c) + "a",
              "^я": "ja"
              }

test_str = "Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства."

def transcribe(input_text):
    output_list = [] # Initialize list to hold words and whitespace to be joined together after processing
    for word in re.split(r'(\S+)', input_text): # Split input string into words and whitespace
        if word.isspace(): # If the segment of input string is just whitespace, add it to output list and move on
            output_list.append(word)
            continue
        word_output = ""
        for (index, letter) in enumerate(word):
            upper = False
            try:
                if letter.isupper(): # If the current letter in the current word is uppercase, change a state variable and reuppercase it later
                    upper = True
                    letter = letter.lower()
                if letter in ["е","ё","ю","я"]: # If the current letter is a vowel could be transcribed with a "j" preceding
                    if index == 0 or word[index - 1] in ["а","е","ё","и","о","у","ы","э","ю","я","ъ"]: # If the current letter follows a vowel, the start of the word, or a ъ
                        letter = "^" + letter # Add a "^" before the letter for the dict lookup to add a preceding "j"
                if upper: # Reuppercase the letter if the letter needs it
                    letter_transcription = rus_to_lat[letter]
                    if len(letter_transcription) > 1: # Will reuppercase to, e.g., "Ja" instead of "JA" for "Я"
                        word_output += letter_transcription[0].upper() + letter_transcription[1:]
                    else:
                        word_output += rus_to_lat[letter].upper()
                else:
                    word_output += rus_to_lat[letter]
            except KeyError: # If the letter is punctuation/etc., just add the letter
                word_output += letter
        output_list.append(word_output) # Add the processed word to the output list
    text_output = "".join(output_list)
    
    return text_output

if __name__ == "__main__":
    if not sys.argv[1]:
        print(transcribe(test_str))
    else:
        print(transcribe(decode(encode(sys.argv[1], 'latin-1', 'backslashreplace'), 'unicode-escape')))
    # CLI args are automatically escaped by Windows (e.g., "\n" gets passed as "\\n") so it is necessary to process input
    # Solution found here https://stackoverflow.com/a/57192592