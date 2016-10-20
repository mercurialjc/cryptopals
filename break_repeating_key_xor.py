#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Break repeating-key XOR
It is officially on, now.
This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
this is a test
and
wokka wokka!!!
is 37. Make sure your code agrees before you proceed.
For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have code to do this.
For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

No, that's not a mistake.
We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.
"""
from itertools import izip, cycle
import base64
import single_byte_xor_cipher

def str_to_binary(string):
    return ''.join('{0:08b}'.format(ord(c), 'b') for c in string)


def edit_distance(str1, str2):
    binary_str1 = str_to_binary(str1)
    binary_str2 = str_to_binary(str2)
    distance = 0
    for i, j in zip(binary_str1, binary_str2):
        if i != j:
            distance += 1
    return distance


def most_probable_keysizes(ciphertext):
    SIZE = 3
    keysize_distance_tuples = []
    for keysize in xrange(2, 41):
        distance = (edit_distance(ciphertext[:keysize], ciphertext[keysize:keysize*2]) + edit_distance(ciphertext[keysize:keysize*2], ciphertext[keysize*2:keysize*3]) + edit_distance(ciphertext[keysize*2:keysize*3], ciphertext[keysize*3:keysize*4])) / float(keysize)
        keysize_distance_tuples.append((keysize, distance))
    return zip(*sorted(keysize_distance_tuples, key=lambda tup: tup[1])[:SIZE])[0]


def read_ciphertext(file_name):
    ciphertext = ''
    with open(file_name) as cipher_file:
        for line in cipher_file:
            ciphertext += line.rstrip('\n')
    ciphertext = base64.b64decode(ciphertext)
    return ciphertext
    

def break_into_blocks(text, size):
    length = len(text)
    return [text[i:i+size] for i in range(0, length, size)]


def transpose(blocks):
    transposed_len = len(blocks[0])
    transposed_blocks = []
    for i in range(transposed_len):
        string = ''
        for b in blocks:
            if i < len(b):
                string += b[i]
        transposed_blocks.append(string)
    return transposed_blocks


def find_key(ciphertext):
    length = len(ciphertext)
    max_score = 0.0
    decoded_str = ''
    probable_key = ''
    for char in single_byte_xor_cipher.generate_ascii_char():
        key = char*length
        curr_decoded_str = single_byte_xor_cipher.xor_str(ciphertext, key)
        score = single_byte_xor_cipher.grade(curr_decoded_str)
        if score >= max_score:
            max_score = score
            decrypted_str = curr_decoded_str
            probable_key = char
    return probable_key


def decrypt(ciphertext, key):
    return ''.join(chr(ord(m) ^ ord(c)) for m,c in izip(ciphertext, cycle(key)))


def main():
    ciphertext = read_ciphertext('6.txt')
    likely_keysizes = most_probable_keysizes(ciphertext)
    size_key_dict = {}
    for KEYSIZE in likely_keysizes:
        size_key_dict[KEYSIZE] = ''
        cipher_blocks = break_into_blocks(ciphertext, KEYSIZE)
        transposed_blocks = transpose(cipher_blocks)
        for t in transposed_blocks:
            size_key_dict[KEYSIZE] += find_key(t)
    plaintext = ''
    score = 0.0
    for key, value in size_key_dict.iteritems():
        curr_text = decrypt(ciphertext, value)
        curr_score = single_byte_xor_cipher.grade(curr_text)
        if curr_score >= score:
            plaintext = curr_text
            score = curr_score
    print plaintext.rstrip('\n')

if __name__ == '__main__':
    main()
