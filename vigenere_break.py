# pylint: disable=invalid-name
import sys
from math import sqrt

alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
min_key_length = 3
max_key_length = 16

def findFactors(n):
    factors = []
    for i in range(min_key_length, max_key_length):
        if (n % i == 0):
            factors.append(i)
    return factors

def repeatedBigrams(ciphertext):
    # Finds all repeated bigrams in the text
    # Returns a dictionary with the bigrams as keys 
    # and [location of first repetition, distance between first and second appearance, factors] as values
    bigrams = {}

    n = len(ciphertext)
    for i in range(0,n-1):
        first_bigram = ciphertext[i] + ciphertext[i+1]
        for j in range(i+1,n-1):
            second_bigram = ciphertext[j] + ciphertext[j+1]
            if (first_bigram == second_bigram and first_bigram not in bigrams):
                location = j
                distance = j-i
                factors = findFactors(distance)
                bigrams[first_bigram] = [location, distance, factors]
    print(bigrams)
    return bigrams


def decrypt(ciphertext, key):
    plaintext = ''
    full_key = ''

    for i in ciphertext[1::len(key)]:
        for j in key:
            full_key += j

    n = len(ciphertext)
    for i in range(n):
        x = alphabet.find(ciphertext[i])
        k = alphabet.find(full_key[i])
        x = x - k
        if (x > 28):
            x = x % 29
        plaintext += alphabet[x]    
        
    print(plaintext)

def main():
    ciphertext = 'kiömsåzsvlryppmlxosdpsmtåiwhrmzsvmperxjyjiynhneålrässmkiöivazewkikhröektymwnwtvkjyrnzvjuhnåxkgpshrmlbwnqxsräåsmömääxövslokuhqvhhnonnyxupkövgqnpjkxööbväröyejyxrzxnysvwssrwöyilrgqztåhxöömmucåtwöhwöhxrvrtvqnuxhyrjzbärdw'
    ciphertext = ciphertext.lower()

    # Kasiski Method
    ## Step 1: Find repeated bigrams and spacing between them
    repeatedBigrams(ciphertext)

    # Decrypt the ciphertext once the key is obtained
    key = 'hej'
    decrypt(ciphertext, key)

if __name__ == '__main__':
    main()