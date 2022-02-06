# pylint: disable=invalid-name

import sys

alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
plaintext = "DetforsomenpildetflögliktenandsomflyktarförjägarensloddetbrusandebantågKringskogarnesrandettböljandeångmolnstodVisuttoochglammadehjertligtochgladttvåmuntraartisterompojkstreckchsprattVidnärmstastationkomentärnasåskön"
key = "hej"

key = key.lower()
plaintext = plaintext.lower()
n = len(plaintext)

full_key = ''
cyphertext = ''

# Extend key (repeating it) to cover plaintext of length n
for i in plaintext[0::len(key)]:
    for j in key:
        full_key += j

for i in range(n):
    x = alphabet.find(plaintext[i])
    k = alphabet.find(full_key[i])

    x = x + k
    if (x > 28):
        x = x % 29

    cyphertext += alphabet[x]    
    
print(cyphertext)
