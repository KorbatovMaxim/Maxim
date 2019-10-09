
#Importing the library 'random'
import random

p_bool = False
q_bool = False

#the function to check for a Prime number
def is_prime(n):
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE

    #check that the number is divisible only by itself
    d = 2
    while n % d != 0:
       d += 1
    return d == n
    #pass

#public and private key generation function
def generate_keypair(p, q):

    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    # PUT YOUR CODE HERE
    n = p*q

    # phi = (p-1)(q-1)
    # PUT YOUR CODE HERE
    phi = (p-1)*(q-1)

    # Choose an integer e such that e and phi(n) are coprime
    #e = random.randrange(1, phi)

    # Random e to find the part of the publick key
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)

    #Finding the part of the public key e in the cycle
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        print("e = " + str(e) + "g = " +str(g))

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    print ("Public key is (" + str(e) + "," + str(n) +") and private key is (" + str(d) + "," + str(n) + ")")
    return ((e, n), (d, n))

#The first part of the Euclid's Algorithm - finding the smallest common divisor
def gcd(a, b):
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # PUT YOUR CODE HERE
    while b != 0:
        a, b = b, a % b
    #print("a = " + str(a))
    return a
    #pass

#Finding the part of the private key d
def multiplicative_inverse(e, phi):
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    # PUT YOUR CODE HERE
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    #Extended Euclid's Algorithm 
    while e > 0:
        celoe = int(temp_phi/e)
        ostatok = temp_phi - celoe * e
        temp_phi = e
        e = ostatok

        x = x2- celoe * x1
        y = d - celoe * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

    #pass

# encrypt function
def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #Return the array of bytes
    return cipher

# decrypt function
def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)


while (p_bool==False):
    p = input("Input the first Prime integer p: ")
    p_bool = is_prime(int(p))
print("Ok!!!")

while (q_bool==False):
    q = input("Input the second Prime integer q: ")
    q_bool = is_prime(int(q))
print("Ok!!!")
print("You have introduced two Prime numbers: " + p + " end " + q)
#proba = gcd(12,15)
#proba1 = multiplicative_inverse(7, 40)
#print ("private key = " + str(proba1))
public, private = generate_keypair(int(p), int(q))
message = input("Enter a message to encrypt with your private key: ")
encrypted_msg = encrypt(private, message)
print("Your encrypted message is: ")
print(str(encrypted_msg))
print("Decrypting message with public key " + str(public) + " . . .")
print("Your message is: ")
print(decrypt(public, encrypted_msg))