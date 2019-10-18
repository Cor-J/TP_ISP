#Exercice 5, Cesar's cipher
#write a program that take the ciphertext as input, checks all the possible shifts
#and shows the most probable shift with the frequency method and the dictionnary method


#def encrypt(phrase,n):
   # encrypttext = str()
    #for lettre in phrase:
     #   encryptletter = chr(ord(lettre) + n)
      #  if encryptletter==" ":
       #     encrypttext+=" "
        #else:
         #   encrypttext+=encryptletter
    #print(encrypttext)

# dictionnary method !
import enchant
results={}
print("Dictionnary method\n")
#opnening and reading of the file
with open("ciphertext.txt", "r") as cipher: 
    ciphertext=cipher.read()
    DictMaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #creation of dictionnary of potential letter in ciphertex.txt
    DictMin = "abcdefghijlkmnopqrstuvwxyz"

    n=0 # this loop test every types of shifhting possible 
    while n<26:
        decryptletter=str() #empty string to collect the decrypted text
        wordlist = ()
        for caracter in ciphertext: #this condition tests the UPPERCASES 
            if caracter in DictMaj: #caracters UPPERCASE
                DECIM = ord(caracter) # transforms the caracter int its decimal value
                if DECIM <= (64+n): #special conditions since the alphabet makes a "loop" whenn encoding ceaser
                    decryptletter+=chr(DECIM + (26-n))
                else:
                    decryptletter+=chr(DECIM - n) #usual conditions to decrypt
            elif caracter in DictMin: #caracter lowercase
                DECIM=ord(caracter)
                if DECIM <=(96+n):
                    decryptletter+=chr(DECIM + (26-n))
                else:
                    decryptletter+=chr(DECIM -n)
            else: #all the other caracters (space, apostrphes, points, etc..)
                decryptletter+=caracter
        #print(decryptletter) #print the decrypted texte
        wordlist = decryptletter.split() #liste that split the word
        #print(wordlist)
        k=0 #initiation of variable that we need
        Truelist=0
        Falselist=0
        while (k<len(wordlist)): #as long as the list goes
            d=enchant.Dict("en_US") #checks if a word is english
            candidate_word = wordlist[k] # each word of the list is tested
            result=(d.check(candidate_word)) #the result of th check is stored
            #print(result)
            if result==True:
                Truelist+=1 # addition of one true
            else:
                Falselist+=1
            results[n] = Truelist #result stored in the corresponding shifting index
            k +=1
        #for x,y, in results.items():
            #print(x,y)
        n+=1
    x,y = max(zip(results.values(),results.keys())) # x is the value of the highest match, #y is the correspondinf key in dictinnary
    print("The maximum word found is",x,"for the key",y)
    print("This Caeser's Cipher has a right shift of",26-y,".")
    decryptletter=str()
    for caracter in ciphertext:  # this condition tests the UPPERCASES
        if caracter in DictMaj:  # caracters UPPERCASE
            DECIM = ord(caracter)  # transforms the caracter int its decimal value
            if DECIM <= (64 + y):  # special conditions since the alphabet makes a "loop" whenn encoding ceaser
                decryptletter += chr(DECIM + (26-y))
            else:
                decryptletter += chr(DECIM - y)  # usual conditions to decrypt
        elif caracter in DictMin:  # caracter lowercase
            DECIM = ord(caracter)
            if DECIM <= (96 + y):
                decryptletter += chr(DECIM + (26 - y))
            else:
                decryptletter += chr(DECIM - y)
        else:  # all the other caracters (space, apostrphes, points, etc..)
            decryptletter += caracter
    print("The decrypted Cipher's text is :",decryptletter)


## frequency analysis method
letter_frequency_english =  {'e' : 12.0, 't' : 9.10, 'a' : 8.12, 'o' : 7.68,
                             'i' : 7.31, 'n' : 6.95, 's' : 6.28, 'r' : 6.02,
                             'h' : 5.92, 'd' : 4.32, 'l' : 3.98, 'u' : 2.88,
                             'c' : 2.71, 'm' : 2.61, 'f' : 2.30, 'y' : 2.11,
                             'w' : 2.09, 'g' : 2.03, 'p' : 1.82, 'b' : 1.49,
                             'v' : 1.11, 'k' : 0.69, 'x' : 0.17, 'q' : 0.11,
                             'j' : 0.10, 'z' : 0.07 }

cifrequencies={'a': 0,'b': 0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0 ,
                   'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0, 
                   'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0
                   }

DictMaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #creation of dictionnary of potential letter in ciphertex.txt
DictMin = "abcdefghijlkmnopqrstuvwxyz"

print("\nFrequency analysis method\n")
#opnening and reading of the file
with open("ciphertext.txt", "r") as cipher: 
    ciphertext=cipher.read()
    removespace=ciphertext.replace(" ", "")
    removepoints=removespace.replace(".", "")
    removetraits=removepoints.replace("-","")
    removecoma=removetraits.replace(",","")
    finalcipher=removecoma.replace("'","")
    lenci=len(finalcipher)
    for letter in ciphertext:
        if letter == "A" or letter == "a":
            cifrequencies['a']+=1
        elif letter == "B" or letter == "b":
            cifrequencies['b']+=1
        elif letter == "C" or letter == "c":
            cifrequencies['c']+=1
        elif letter == "D" or letter == "d":
            cifrequencies['d']+=1
        elif letter == "E" or letter == "e":
            cifrequencies['e']+=1
        elif letter == "F" or letter == "f":
            cifrequencies['f']+=1
        elif letter == "G" or letter == "g":
            cifrequencies['g']+=1
        elif letter == "H" or letter == "h":
            cifrequencies['h']+=1
        elif letter == "I" or letter == "i":
            cifrequencies['i']+=1
        elif letter == "J" or letter == "j":
            cifrequencies['j']+=1
        elif letter == "K" or letter == "k":
            cifrequencies['k']+=1
        elif letter == "L" or letter == "l":
            cifrequencies['l']+=1
        elif letter == "M" or letter == "m":
            cifrequencies['m']+=1
        elif letter == "N" or letter == "n":
            cifrequencies['n']+=1
        elif letter == "O" or letter == "o":
            cifrequencies['o']+=1
        elif letter == "P" or letter == "p":
            cifrequencies['p']+=1
        elif letter == "Q" or letter == "q":
            cifrequencies['q']+=1
        elif letter == "R" or letter == "r":
            cifrequencies['r']+=1
        elif letter == "S" or letter == "s":
            cifrequencies['s']+=1
        elif letter == "T" or letter == "t":
            cifrequencies['t']+=1
        elif letter == "U" or letter == "u":
            cifrequencies['u']+=1
        elif letter == "V" or letter == "v":
            cifrequencies['v']+=1
        elif letter == "W" or letter == "w":
            cifrequencies['w']+=1
        elif letter == "X" or letter == "x":
            cifrequencies['x']+=1
        elif letter == "Y" or letter == "y":
            cifrequencies['y']+=1
        elif letter == "Z" or letter == "z":
            cifrequencies['z']+=1

    for x in cifrequencies:
        cifrequencies[x]/=lenci
    for x in cifrequencies:
        cifrequencies[x]*=100    

    xcl,ycl = max(zip(letter_frequency_english.values(),letter_frequency_english.keys()))
    
    xci,yci = max(zip(cifrequencies.values(),cifrequencies.keys()))
    
    Decicl = ord(ycl)
    Decici = ord(yci)
    shift = Decici - Decicl

    print("The highest frequency of the english language is",xcl,"for the letter",ycl)
    print("The highest frequency of the cipher text is",xci,"for the letter",yci)

    print("This Caeser's Cipher has a right shift of",26-shift,".")
    decryptletter=str()
    for caracter in ciphertext:  # this condition tests the UPPERCASES
        if caracter in DictMaj:  # caracters UPPERCASE
            DECIM = ord(caracter)  # transforms the caracter int its decimal value
            if DECIM <= (64 + shift):  # special conditions since the alphabet makes a "loop" whenn encoding ceaser
                decryptletter += chr(DECIM + (26-shift))
            else:
                decryptletter += chr(DECIM - shift)  # usual conditions to decrypt
        elif caracter in DictMin:  # caracter lowercase
            DECIM = ord(caracter)
            if DECIM <= (96 + shift):
                decryptletter += chr(DECIM + (26 - shift))
            else:
                decryptletter += chr(DECIM - shift)
        else:  # all the other caracters (space, apostrphes, points, etc..)
            decryptletter += caracter
    print("The decrypted Cipher's text is :",decryptletter)

