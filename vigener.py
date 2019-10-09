# Input word to encrypt and keyword
vvod = input("Input the word to encrypt: ")
keyvvod = input("Input the keyword: ")
# Input big and small alphabet and additionals symbols
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph_sm = "abcdefghijklmnopqrstuvwxyz"
alph_num="0123456789."

# encrypt function
def encrypt_vigener(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    #denote the result variable global for use throughout the code
    global result
    result = ""

    #If the word key length is less than the word for encryption, 
    # then increase the key by repeating it
    while (len(keyword)<len(plaintext)):
        keyword+=keyword

    #remove the spaces on the right and left
    ishodnik = plaintext.strip()
    #convert the word source to a list of symbols
    ishodnik_mas = list(ishodnik)
    #convert the keyword to a list of symbols
    keystr_mas = list(keyword)
    shift = 0
       
    #we pass in the cycle of the letter in the list of word symbols
    for i in range(len(ishodnik_mas)):
            simvol = ishodnik_mas[i]

            #find the corresponding keyword symbol at the index
            for j in range(len(keystr_mas)):
                    if i == j:
                        s_k = keystr_mas[j]

            if simvol in alph:

                #Find the keyword symbol in the alphabet and find the offset      
                for simvol_alph in alph:
                    if simvol_alph == s_k.upper():
                        shift = alph.index(simvol_alph)
                #we form the result taking into account the specified offset 
                # and taking into account the transition from 'Z' to 'A'
                result+=alph[(alph.index(simvol) + shift) % len(alph)]

            elif simvol in alph_sm:
                
                for simvol_alph_sm in alph_sm:
                    if simvol_alph_sm == s_k.lower():
                        shift = alph_sm.index(simvol_alph_sm)
                result+=alph_sm[(alph_sm.index(simvol) + shift) % len(alph_sm)]

            elif simvol in alph_num:
                #result+=alph_num[(alph_num.index(simvol) + shift) % len(alph_num)]
                result+=simvol
            else:
                print("Error - undefined symbol")
    #Output the encryption result       
    print('Result: ' + result)

#Calling the encryption function
encrypt_vigener(vvod,keyvvod)

# decrypt function
def decrypt_vigener(ciphertext,keyword):
    global result
    result = ""

    while (len(keyword)<len(ciphertext)):
        keyword+=keyword
    
    #Trim the resulting keyword to the size of the source
    keyword = keyword[0:len(ciphertext)]

    ishodnik = ciphertext.strip()
    ishodnik_mas = list(ishodnik)
    keystr_mas = list(keyword)
    shift = 0
     
    #for simvol in ishodnik:
    for i in range(len(ishodnik_mas)):
            simvol = ishodnik_mas[i]
            for j in range(len(keystr_mas)):
                    if i == j:
                        s_k = keystr_mas[j]
            if simvol in alph:
                for simvol_alph in alph:
                    if simvol_alph == s_k.upper():
                        shift = alph.index(simvol_alph)
                        #Define the symbol code and make an offset in the code. 
                        # Control the correct transition from 'A' to 'Z'
                        ord_s = ord(simvol)
                        ord_decode_s = ord_s - shift
                        if ord_decode_s < ord('A'):
                            ord_decode_s = ord('Z') - (shift-(ord_s - ord('A'))-1)
                        result+=chr(ord_decode_s)
            
            elif simvol in alph_sm:        
                for simvol_alph_sm in alph_sm:
                    if simvol_alph_sm == s_k.lower():
                        shift = alph_sm.index(simvol_alph_sm)
                        ord_s = ord(simvol)
                        ord_decode_s = ord_s - shift
                        if ord_decode_s < ord('a'):
                         ord_decode_s = ord('z') - (shift-(ord_s - ord('a'))-1)
                        result+=chr(ord_decode_s)
            elif simvol in alph_num:
                result+=simvol
    print('Result: ' + result)

#Calling the decryption function
decrypt_vigener(result,keyvvod)