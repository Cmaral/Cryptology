# pylint: disable=invalid-name

import sys

alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
plaintext = "varsågod with spaces"
key = "hej"

key = key.lower()
plaintext = plaintext.lower()
n = len(plaintext)

full_key = ''
cyphertext = ''

# Extend key (repeating it) to cover plaintext of length n
for i in plaintext[1::len(key)]:
    for j in key:
        full_key += j

for i in range(n):

    # If current character is a space, add a space to cyphertext
    if (plaintext[i] == ' '):
        cyphertext += ' '
    # Otherwise, perform shift
    else:
        x = alphabet.find(plaintext[i])
        k = alphabet.find(full_key[i])

        x = x + k
        if (x > 28):
            x = x % 29

        cyphertext += alphabet[x]    
    
print(cyphertext)
