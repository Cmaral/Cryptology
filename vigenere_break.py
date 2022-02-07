# pylint: disable=invalid-name
import sys
from math import sqrt


alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
# Swedish alphabet frequency table obtained from:
# http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/swedish-letter-frequencies/
alphabet_frequencies = {'a': 10.04, 'b': 1.31, 'c': 1.71, 'd': 4.90, 'e': 9.85, 'f': 1.81, 'g': 3.44, 'h': 2.85,
                        'i': 5.01, 'j': 0.90, 'k': 3.24, 'l': 4.81, 'm': 3.55, 'n': 8.45, 'o': 4.06, 'p': 1.57,
                        'q': 0.01, 'r': 7.88, 's': 5.32, 't': 8.89, 'u': 1.86, 'v': 2.55, 'w': 0.14, 'x': 0.11,
                        'y': 0.71, 'z': 0.04, 'å': 1.66, 'ä': 2.10, 'ö': 1.50}

min_key_length = 3
max_key_length = 16

def findFactors(n):
    """
    Returns a list containing the factors of n between min_key_length and max_key_length
    """
    factors = []
    for i in range(min_key_length, max_key_length+1):
        if n % i == 0:
            factors.append(i)
    return factors

def repeatedBigrams(ciphertext):
    """
    Returns a list containing all the possible key lengths,
    obtained by measuring and factoring the distance between the
    repeated bigrams found in the ciphertext
    """
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
    return all_factors

def sortKeyLengths(bigram_factors):
    """
    Given a list of factors bigram_factors, returns a sorted list
    containing all the candidate key lengths and their number of
    appearances, sorted by how likely they are to be the correct
    key length
    """
    key_length_dict = {}
    for x in bigram_factors:
        if not x in key_length_dict:
            key_length_dict[x] = 1
        else:
            key_length_dict[x] += 1

    key_length_list = sorted(key_length_dict.items(), key=lambda values: values[1], reverse=True)
    return key_length_list

def getFrequency(text):
    """
    Given a text, returns a list containing all the letters in the
    Swedish alphabet and how many times they appear in the text
    """
    freq_dict = {}

    # Count letters in text
    # If letter does not appear in the text, add it to the list
    # with value 0
    for letter in text:
        if letter not in freq_dict:
            freq_dict[letter] =  1
        else:
            freq_dict[letter] +=  1

    for letter in alphabet:
        if letter not in freq_dict:
            freq_dict[letter] = 0

    # Convert dict to list and sort letters alphabetically
    freq_list = sorted(freq_dict.items(), reverse=False)
    return freq_list

def tryAttack(ciphertext, key_length):
    """
    Given a ciphertext and a possible key length,
    attempts to break the cipher and obtain the key.
    Returns the best guess for a key of length key_length
    obtained using the chi-squared test
    """
    # Sort the letters in the ciphertext into columns
    # one for each letter in the key:
    columns = []
    for i in range(key_length):
        current_column = []
        for j in ciphertext[i::key_length]:
            current_column.append(j)
        columns.append(current_column)

     # Obtain letter frequency by column
    frequencies = []
    print("Letter count by column: ")
    for column in columns:
        print("Column ", columns.index(column))
        column_freq = getFrequency(column)
        frequencies.append(column_freq)
        print(column_freq, "\n")

    # Guess most likely key for each column
    # using the chi-squared method
    key = ''
    for column in columns:
        freq_key = -1
        current_key = ''
        for i in alphabet:
            # For each letter in the Swedish alphabet,
            # decrypt the column using key = i
            freq_sum = 0
            shifted_text = decrypt(column, i) # Shift column by letter i
            freq_cipher_shifted = getFrequency(shifted_text) # Letter counts in column shifted by i
            for shifted_letter in freq_cipher_shifted:
                # Actual letter count of current letter in the shifted text:
                freq_cipher = shifted_letter[1] 
                # Expected letter count of current letter in the shifted text:
                freq_swedish = (alphabet_frequencies[shifted_letter[0]]/100)*len(column)
                # Compute chi squared for current letter/key combo and add to the total:
                freq_sum += (sqrt(abs(freq_cipher-freq_swedish)))/freq_swedish

            # If the chi-squared statistic for this column deciphered with the current letter
            # is lower than the previous values, this letter is more likely to be the key
            # for this column
            if (freq_sum<freq_key or freq_key==-1):
                freq_key = freq_sum
                current_key = i

        # Add the guessed key for the current column
        # to the complete key
        key += current_key

    # Return complete key
    return key

def decrypt(ciphertext, key):
    """
    Given a ciphertext and a key, shifts each letter in the text
    with its corresponding key letter to obtain the original message
    Returns the plaintext after decrypting it
    """
    plaintext = ''
    full_key = ''

    # Repeat the key until it covers the full
    # length of the ciphertext
    for i in ciphertext[0::len(key)]:
        for j in key:
            full_key += j

    n = len(ciphertext)

    # Shift each letter in the ciphertext by its corresponding
    # key
    for i in range(n):
        x = alphabet.find(ciphertext[i])
        k = alphabet.find(full_key[i])
        x = x - k
        x = x % 29
        plaintext += alphabet[x]    
    return plaintext

def printTextSeparated(text, space):
    """
    Prints a given text separating it into chunks of size space
    """
    print("The resulting decrypted text is: ")
    for i in range(len(text)):
        print(text[i], end= '')
        if (i+1)%space==0:
            print(end = ' ')
    print()


def main():
    option = input("Choose option: \n"
                "1. Try to break cipher without knowing key, \n"
                "2. Decrypt text given a key \n")
    if option=='1':
        ciphertext = input("Input ciphertext: ")
        ciphertext = ciphertext.lower()

        # Kasiski Method
        ## Step 1: Find repeated bigrams and spacing between them
        all_factors = repeatedBigrams(ciphertext)

        ## Step 2: Sort key lengths by how likely they are to be the correct key length
        key_length_list = sortKeyLengths(all_factors)
        print("\nList of possible key lengths and their number of appearances:")
        print(key_length_list)

        ## Step 3: Try key lengths starting by the most possible one
        key = ''
        for i in key_length_list:
            key_length = i[0]
            answer = input("\nTry to hack with key length " + str(key_length) + "? (Y/N) ")
            if answer in ('Y', 'y', 'yes', 'Yes', 'YES', ''):
                key = tryAttack(ciphertext, key_length) 
                print("\nKey obtained: " + key)
                plaintext = decrypt(ciphertext, key)
                printTextSeparated(plaintext, key_length)
            else:
                pass

    if option=='2':
        key = ''
        ciphertext = input("Input ciphertext: ")
        while key not in ('e', 'E'):
            key = input("\nInput key: (input E to exit)")
            plaintext = decrypt(ciphertext, key)
            printTextSeparated(plaintext, len(key))
    else:
        pass

if __name__ == '__main__':
    main()
