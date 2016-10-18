#!/usr/bin/env python

"""Detect single-character XOR
One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)
"""
import single_byte_xor_cipher

def main():
    with open('4.txt') as lines:
        max_score = 0.0
        decrypted_str = ''
        for line in lines:
           suspect = line.rstrip('\n').decode('hex')
           length = len(suspect)/2
           for char in single_byte_xor_cipher.generate_ascii_char():
               key = (char.encode('hex')*length).decode('hex')
               curr_decoded_str = single_byte_xor_cipher.xor_str(suspect, key)
               score = single_byte_xor_cipher.grade(curr_decoded_str)
               if score >= max_score:
                   max_score = score
                   decrypted_str = curr_decoded_str
        if decrypted_str != '':
            print decrypted_str


if __name__ == '__main__':
    main()
