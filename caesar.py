# Input offset and word to encrypt
sdvig = int(input("Input shift: "))
vvod = input("Input the word to encrypt: ")
# Input big and small alphabet and additionals symbols
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph_sm = "abcdefghijklmnopqrstuvwxyz"
alph_num="0123456789."

# encrypt function
def encrypt_caesar(plaintext, shift):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    #denote the result variable global for use throughout the code
    global result
    result = ""
    #remove the spaces on the right and left
    ishodnik = plaintext.strip()
    #we pass in the cycle of the letter in the word source
    for simvol in ishodnik:
            #different conditions for large and small alphabet
            if simvol in alph:
                #we form the result taking into account the specified offset 
                # and taking into account the transition from 'Z' to 'A'
                result+=alph[(alph.index(simvol) + shift) % len(alph)]
            elif simvol in alph_sm:
                result+=alph_sm[(alph_sm.index(simvol) + shift) % len(alph_sm)]
            elif simvol in alph_num:
                #result+=alph_num[(alph_num.index(simvol) + shift) % len(alph_num)]
                result+=simvol
            else:
                print("Error - undefined symbol")
    #Output the encryption result
    print('Result: ' + result)

#Calling the encryption function
encrypt_caesar(vvod,sdvig)

# decrypt function
def decrypt_caesar(ciphertext,shift1):
    result1 = ""
    ishodnik = ciphertext.strip()
    for simvol in ishodnik:
            if simvol in alph:
                #Define the symbol code and make an offset in the code. 
                # Control the correct transition from 'A' to 'Z'
                ord_s = ord(simvol)
                ord_decode_s = ord_s - shift1
                if ord_decode_s < ord('A'):
                    ord_decode_s = ord('Z') - (shift1-(ord('A')-ord_decode_s))
                result1+=chr(ord_decode_s)
            elif simvol in alph_sm:
                ord_s = ord(simvol)
                ord_decode_s = ord_s - shift1
                if ord_decode_s < ord('a'):
                    ord_decode_s = ord('z') - (shift1-(ord('a')-ord_decode_s))
                result1+=chr(ord_decode_s)
            elif simvol in alph_num:
                #result+=alph_num[(alph_num.index(simvol) + shift) % len(alph_num)]
                result1+=simvol
    print('Result: ' + result1)

#Calling the decryption function
decrypt_caesar(result, sdvig)