# pylint: disable=invalid-name
import sys
from math import sqrt


alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
# Swedish alphabet frequency table obtained from:
# http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/swedish-letter-frequencies/
alphabet_frequencies = {'a': 9.38, 'b': 1.54, 'c': 1.49, 'd': 4.70, 'e': 10.15, 'f': 2.03, 'g': 2.86, 'h': 2.09,
                        'i': 5.82, 'j': 0.061, 'k': 3.14, 'l': 5.28, 'm': 3.47, 'n': 8.54, 'o': 4.48, 'p': 1.84,
                        'q': 0.02, 'r': 8.43, 's': 6.59, 't': 7.69, 'u': 1.92, 'v': 2.42, 'w': 0.14, 'x': 0.16,
                        'y': 0.71, 'z': 0.07, 'å': 1.34, 'ä': 1.80, 'ö': 1.31}


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
    all_factors = []

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
                for x in factors:
                    all_factors.append(x)
    return bigrams, all_factors

def sortKeyLengths(bigram_factors):
    # Given a list of factors, return list of possible key lengths sorted by pausability (number of repetitions)
    key_length_dict = {}
    for x in bigram_factors:
        if not x in key_length_dict:
            key_length_dict[x] = 1
        else:
            key_length_dict[x] += 1

    key_length_list = sorted(key_length_dict.items(), key=lambda values: values[1], reverse=True)
    return key_length_list

def getFrequency(text):
    freq_dict = {}

    # Count letters in text. If non existing, add letter with count 0
    for letter in text:
        if letter not in freq_dict:
            freq_dict[letter] =  1
        else:
            freq_dict[letter] +=  1

    for letter in alphabet:
        if letter not in freq_dict:
            freq_dict[letter] = 0

    # Calculate frequency of each letter in given text
    for i in freq_dict:
        freq_dict[i] = round((freq_dict[i]/len(text))*100, 2)

    # Return a list sorted alphabetically with the frequency of each letter
    freq_list = sorted(freq_dict.items())
    return freq_list

def shiftLetters(letters, shift):
    shifted_letters = ''
    for letter in letters:
        x = alphabet.find(letter)
        y = x + shift
        if (y > 28):
            y = y % 29
        shifted_letters += alphabet[y]
    return shifted_letters


def tryAttack(ciphertext, key_length):    
    # Sort letters in ciphertext into columns:
    columns = []
    for i in range(key_length):
        current_column = []
        for j in ciphertext[i::key_length]:
            current_column.append(j)
        columns.append(current_column)

    # Obtain letter frequency in ciphertext
    print("Letter frequency in ciphertext: ")
    ciphertext_freq = getFrequency(ciphertext)
    print(ciphertext_freq)
    print()

     # Obtain letter frequency by column
    frequencies = []
    print("Letter frequencies by column: ")
    for column in columns:
        column_freq = getFrequency(column)
        frequencies.append(column_freq)
        print(column_freq)
        print()


    # Shift by a given value
    shift = 0
    while (shift != -1):
        print()
        print("Letter: " + alphabet[shift])
        shifted_letters = shiftLetters(columns[0], shift)
        print(getFrequency(shifted_letters))
        shift = int(input("Shift: (input -1 to stop shifting)"))

def decrypt(ciphertext, key):
    plaintext = ''
    full_key = ''

    for i in ciphertext[0::len(key)]:
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
    return plaintext


    # First step: divide text into as many columns as letters in the key



def main():
    ciphertext = input("Input ciphertext: ")
    print()
    ciphertext = ciphertext.lower()

    # Kasiski Method
    ## Step 1: Find repeated bigrams and spacing between them
    bigrams, all_factors = repeatedBigrams(ciphertext)

    ## Step 2: Sort key lengths by how likely they are to be the correct key length
    key_length_list = sortKeyLengths(all_factors)
    print("List of possible key lengths and their number of appearances:")
    print(key_length_list)
    print()

    ## Step 3: Try key lengths starting by the most possible one
    print("Attempting to break with key length " + str(key_length_list[0][0]) + "...")
    print()
    tryAttack(ciphertext, key_length_list[0][0])


    # Decrypt the ciphertext once the key is obtained
    key = 'hello'
    plaintext = decrypt(ciphertext, key)
    print("The resulting decrypted text is: ")
    print(plaintext)

if __name__ == '__main__':
    main()