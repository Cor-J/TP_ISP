# Exercice 5, Cesar's cipher
# write a program that take the ciphertext as input, checks all the possible shifts
# and shows the most probable shift with the frequency method and the dictionnary method


# def encrypt(phrase,n):
# encrypttext = str()
# for lettre in phrase:
#   encryptletter = chr(ord(lettre) + n)
#  if encryptletter==" ":
#     encrypttext+=" "
# else:
#   encrypttext+=encryptletter
# print(encrypttext)

# dictionnary method !
import enchant
import re  # module for use of regexp to sanitiz ciphertext
import pandas as pd # used to ease correlation computaiton
from collections import Counter # count different char in strings

letter_frequency_english = {'e': 12.0, 't': 9.10, 'a': 8.12, 'o': 7.68,
                            'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
                            'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
                            'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
                            'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
                            'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
                            'j': 0.10, 'z': 0.07}


def decrypt_caesar(ciphertext, shift=0):
    decrypted = ''  # empty string to collect the decrypted text
    for caracter in ciphertext:  # this condition tests the UPPERCASES
        if caracter.isupper():
            decrypted += chr((ord(caracter) - ord('A') - shift) % 26 + ord('A')) # compute letter in 0-26 space and go back to 'python' coding'
        elif caracter.islower():  # caracter lowercase
            decrypted += chr((ord(caracter) - ord('a') - shift) % 26 + ord('a'))
        else:  # all the other caracters (space, apostrphes, points, etc..)
            decrypted += caracter
    return decrypted


def guess_shift_using_dictionary(ciphertext, lang='en_US'):
    """ Function which decrypt with every possible shift and then compute the number of english words
    return best shift and associated english wordcount"""
    dictionnary = enchant.Dict(lang)  # checks if a word is english
#    dictionnary = ['the','cat','is','in','a','bed']
    results = {}
    for shift in range(26):
        decrypted_sentence = decrypt_caesar(ciphertext, shift)
        wordlist = decrypted_sentence.split()  # liste that split the word
        results[shift] = sum([dictionnary.check(candidate_word) for candidate_word in wordlist])
        #results[shift] = sum([candidate_word in dictionnary for candidate_word in wordlist])
    word_count, best_shift = max(zip(results.values(), results.keys()))  # compute max on values and keep associated key
    return word_count, best_shift


def shift_from_frequencies_corr(ciphertext):
    """ Try every shift and compute for each shift the correlation between letter frequencies in english and in the
    supposed plaintext. best correlation => best shift"""
    ref = pd.DataFrame({'reference':letter_frequency_english})
    finalcipher = re.sub(r'\W|\d', '', ciphertext).lower()  # get ride of non letters and digits
    english_corr = {}
    for shift in range(26):
        decrypted = decrypt_caesar(finalcipher, shift)
        english_corr[str(shift)] = Counter(decrypted)  # no working way to compute correlation here with corrwith/other
    english_corr = pd.DataFrame(english_corr).apply(lambda column:column/column.sum()*100)  # 99% that percent not useful with corr
    english_corr = english_corr.apply(lambda column: ref.corrwith(column)) #compute corr for each shift
    return english_corr.max(axis=1)['reference'], int(english_corr.idxmax(axis=1)) # correlation, shift


if __name__ == '__main__':
    results = {}

    # opnening and reading of the file
    with open("ciphertext.txt", "r") as cipher:
        ciphertext = cipher.read()

    print("Dictionnary method\n")
    word_count, best_shift = guess_shift_using_dictionary(ciphertext)
    print("\nThe maximum word found is", word_count, "for the key", best_shift)
    print("This Caeser's Cipher has a right shift of", 26 - best_shift, ".")

    plaintext = decrypt_caesar(ciphertext, shift=best_shift)
    print("The decrypted Cipher's text is :", plaintext)


    print("\nFrequency analysis method\n")
    cifrequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0,
                     'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0,
                     'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
                     }

    finalcipher = re.sub('\W|\d', '', ciphertext).lower()  # get ride of non letters and digits
    nb_letters = len(finalcipher)

    for letter in finalcipher:
        try:
            cifrequencies[letter] += 1  # WILL WORK
        except KeyError:
            pass  # if a character was a corner case not removed by regexp, normally will never happen
    # compute frequency in percent for each letter
    cifrequencies = {letter: count / nb_letters * 100 for letter, count in cifrequencies.items()}

    xcl, ycl = max(zip(letter_frequency_english.values(), letter_frequency_english.keys()))
    xci, yci = max(zip(cifrequencies.values(), cifrequencies.keys()))
    shift = ord(yci) - ord(ycl)

    print("The highest frequency of the english language is", xcl, "for the letter", ycl)
    print("The highest frequency of the cipher text is", xci, "for the letter", yci)
    print("This Caeser's Cipher has a right shift of", 26 - shift, ".")
    plaintext = decrypt_caesar(ciphertext, shift=shift)
    print("The decrypted Cipher's text is :", plaintext)

    print('\nFrequency Analysis with correlation')
    max_corr, best_shift = shift_from_frequencies_corr(ciphertext)
    print("best shift is %s and associated correlation with english letters' frequencies is %s" % (best_shift, max_corr))
    print(decrypt_caesar(ciphertext, best_shift))

    # Save values into file
    with open('h1_V.txt','w', encoding='utf8') as f:
        f.write(plaintext + '\n' + str(26 - best_shift))
    print('\n\nResults where written in file')