# pylint: disable=invalid-name
import sys
from math import sqrt
alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
alphabet_frequencies = {'a': 9.98, 'b': 1.36, 'c': 1.68, 'd': 4.92, 'e': 9.76, 'f':
1.81, 'g': 3.44, 'h': 2.85,
                        'i': 5.21, 'j': 0.88, 'k': 3.24, 'l': 4.81, 'm': 3.55, 'n':
8.35, 'o': 4.08, 'p': 1.45,
                        'q': 0.02, 'r': 7.88, 's': 5.22, 't': 8.85, 'u': 1.86, 'v':
2.55, 'w': 0.14, 'x': 0.13,
                        'y': 0.68, 'z': 0.04, 'å': 1.63, 'ä': 2.08, 'ö': 1.55}
MIN_KEY_LENGTH = 3
MAX_KEY_LENGTH = 16


def findFactors(n):
    """
    Returns a list containing the factors of n between MIN_KEY_LENGTH and 
MAX_KEY_LENGTH
    """
    factors = []
    for i in range(MIN_KEY_LENGTH, MAX_KEY_LENGTH+1):
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
    key_length_list = sorted(key_length_dict.items(), key=lambda values: values[1],
reverse=True)
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
        #print("Column ", columns.index(column))
        column_freq = getFrequency(column)
        frequencies.append(column_freq)
        #print(column_freq, "\n")
    # Guess most likely key for each column
    key = ''
    for column in columns:
        key_sum = -1
        current_key = ''
        for i in alphabet:
            # For each letter (i) in the Swedish alphabet
            # Decrypt column using key = i
            shifted_text = decrypt(column, i) 
            # Letter count in current column decrypted with i:
            freq_cipher_shifted = getFrequency(shifted_text) 
            chi_sum = 0
            for shifted_letter in freq_cipher_shifted:
                # Actual count of current letter in the decrypted text:
                freq_decrypted = shifted_letter[1]
                # Expected count of current letter in the decrypted text:
                freq_swedish = 
(alphabet_frequencies[shifted_letter[0]]/100)*len(column)
                # Compute chi-squared for current letter/key and add to total sum 
for this key:
                chi_sum += (sqrt(abs(freq_decrypted-freq_swedish)))/freq_swedish
            # If the chi-squared statistic for this column deciphered with the 
current key
            # is lower than the previous values, this key is more likely to be 
correct
            # for this column
            if (chi_sum<key_sum or key_sum==-1):
                key_sum = chi_sum
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
    # Shift each letter in the ciphertext by its corresponding
    # key
    for i in range(len(ciphertext)):
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
    print("\nThe resulting text is: ")
    for i in enumerate(text):
        print(i[1], end= '')
        if (i[0]+1)%space==0:
            print(end = ' ')
    print("\n")
    
def tryKeys(ciphertext, key_length_list):
    """
    Iterates over the key_length_list and attempts to break the
    ciphertext with each possible key length.
    Prompts the user to choose which key lengths to try.
    """
    key=''
    for i in key_length_list:
        key_length = i[0]
        answer = input("\nTry to hack with key length " + str(key_length) + "? 
(Y/N/Exit) ").lower()
        if answer in ('y', 'yes', ''):
            key = tryAttack(ciphertext, key_length) 
            print("\nKey obtained: " + key)
            plaintext = decrypt(ciphertext, key)
            printTextSeparated(plaintext, key_length)
        elif answer in ('exit', 'e'):
            return
        else:
            pass
                       
def tryAttackMultiple():
    """
    Attempts to break a cipher when the input is multiple
    ciphertexts that use the same key.
    Reads ciphertexts from terminal.
    Concatenates texts (after removing parts that would not
    be long enough for the key) and attempts to break them as if
    they were one.
    """
    ciphertexts = []
    key_length_list = []
    n = int(input("Number of ciphertexts to analyse: "))
    for i in range(n):
        text = input("Input ciphertext "+ str(i) + ": ")
        ciphertexts.append(text)
        key_length_list += (repeatedBigrams(text))
    key_length_list = sortKeyLengths(key_length_list)
    for key_length in key_length_list:
        cut_texts = ''
        # For a given key, trims each text so that the length of the resulting
        # text is a multiple of the key length
        for text in ciphertexts:
            split_at = 0
            for i in range(len(text)):
                j = i+key_length[0]
                if (j%key_length[0]==0 and j<len(text)):
                    split_at = j
            cut_texts += text[0:split_at]
        # Attempt to break cipher as if it was one single ciphertext
        answer = input("\nTry to hack with key length " + str(key_length[0]) + "? 
(Y/N/Exit) ").lower()
        if answer in ('y', 'yes', ''):
            key = tryAttack(cut_texts, key_length[0]) 
            print("\nKey obtained: " + key)
            plaintext = decrypt(cut_texts, key)
            printTextSeparated(cut_texts, key_length[0])
        elif answer in ('exit', 'e'):
            return
        else:
            pass
    for text in ciphertexts:
        print("Trying to decrypt ciphertext #", ciphertexts.index(text))
        tryKeys(text,key_length_list)
                       
def main():
    """
    Main function.
    Offers the user 2 options: guess the key given a ciphertext, or
    decrypt a ciphertext by providing the key.
    """
    option = input("Choose option: \n"
                "1. Try to guess key and break a Vigenere cipher, \n"
                "2. Decrypt text with a given key \n"
                "3. Try to guess key for multiple texts that use the same key\n"
                "4. Split a text into chunks of a given size\n")
    if option=='1':
        ciphertext = input("Input ciphertext: ")
        ciphertext = ciphertext.lower()
        print("\nUsing the Kasiski method to guess key length...")
        # Kasiski Method
        ## Step 1: Find repeated bigrams and spacing between them
        all_factors = repeatedBigrams(ciphertext)
        ## Step 2: Sort key lengths by how likely they are to be the correct key 
length
        key_length_list = sortKeyLengths(all_factors)
        print("List of possible key lengths and their number of appearances 
(length, appearances):")
        print(key_length_list)
        ## Step 3: Try key lengths starting by the most possible one, to guess 
correct key
        tryKeys(ciphertext, key_length_list)
    if option=='2':
        ciphertext = input("Input ciphertext: ")
        key = input("\nInput key: (input E to exit) ").lower()
        while key not in ('e', 'E'):
            plaintext = decrypt(ciphertext, key)
            printTextSeparated(plaintext, len(key))
            key = input("\nInput key: (input E to exit) ").lower()
    if option=='3':
        tryAttackMultiple()
    else:
        pass
if __name__ == '__main__':
    main()
