#!/usr/bin/env python

"""Single-byte XOR cipher
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

Achievement Unlocked
You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
"""
TRIGRAM_FREQUENCIES = {
    'THE': 1.81, 'ERE': 0.31, 'HES': 0.24,
    'AND': 0.73, 'TIO': 0.31, 'VER': 0.24,
    'ING': 0.72, 'TER': 0.30, 'HIS': 0.24,
    'ENT': 0.42, 'EST': 0.28, 'OFT': 0.22,
    'ION': 0.42, 'ERS': 0.28, 'ITH': 0.21,
    'HER': 0.36, 'ATI': 0.26, 'FTH': 0.21,
    'FOR': 0.34, 'HAT': 0.26, 'STH': 0.21,
    'THA': 0.33, 'ATE': 0.25, 'OTH': 0.21,
    'NTH': 0.33, 'ALL': 0.25, 'RES': 0.21,
    'INT': 0.32, 'ETH': 0.24, 'ONT': 0.20
}


def generate_ascii_char():
    for i in range(0, 128):
        yield chr(i)


def xor_str(str1, str2):
    str = ''
    for c1, c2 in zip(str1, str2):
        str += chr(ord(c1)^ord(c2))
    return str


def grade(str):
    score = 0.0
    for trigram in TRIGRAM_FREQUENCIES.keys():
        if trigram in str:
            score += TRIGRAM_FREQUENCIES[trigram]
    return score

def main():
    encoded_hex_str = ('1b37373331363f781'
                       '51b7f2b783431333d'
                       '78397828372d363c7'
                       '8373e783a393b3736')
    length = len(encoded_hex_str)/2
    encoded_hex_num = encoded_hex_str.decode('hex')
    max_score = 0.0
    decoded_str = ''
    for char in generate_ascii_char():
        key = (char.encode('hex')*length).decode('hex')
        curr_decoded_str = xor_str(encoded_hex_num, key)
        score = grade(curr_decoded_str)
        if score >= max_score:
            max_score = score
            decoded_str = curr_decoded_str
    if decoded_str != '':
        print decoded_str
        
        
if __name__ == '__main__':
    main()
