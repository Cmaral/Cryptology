# pylint: disable=invalid-name
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
key_length_max = 16
key = ''

def main():
    ciphertext = 'öeåzbpvh'
    n = len(ciphertext)

    # Decrypt the ciphertext once the key is obtained
    key = 'hej'
    decrypt(ciphertext, n)

def decrypt(ciphertext, n):
    plaintext = ''
    full_key = ''
    for i in ciphertext[1::len(key)]:
        for j in key:
            full_key += j

    for i in range(n):
        x = alphabet.find(ciphertext[i])
        k = alphabet.find(full_key[i])
        x = x - k
        if (x > 28):
            x = x % 29
        plaintext += alphabet[x]    
        
    print(plaintext)


if __name__ == '__main__':
    main()