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
MONOGRAM_FREQUENCIES = {
    'A':  8.55, 'K':  0.81, 'U':  2.68,
    'B':  1.60, 'L':  4.21, 'V':  1.06,
    'C':  3.16, 'M':  2.53, 'W':  1.83,
    'D':  3.87, 'N':  7.17, 'X':  0.19,
    'E': 12.10, 'O':  7.47, 'Y':  1.72,
    'F':  2.18, 'P':  2.07, 'Z':  0.11,
    'G':  2.09, 'Q':  0.10,
    'H':  4.96, 'R':  6.33,
    'I':  7.33, 'S':  6.73,
    'J':  0.22, 'T':  8.94
}

COMMON_ENGLISH_WORDS_FREQUENCIES = {
    'THE' : 6.42, 'ON'   : 0.78, 'ARE' : 0.47,
    'OF'  : 2.76, 'WITH' : 0.75, 'THIS': 0.42,
    'AND' : 2.75, 'HE'   : 0.75, 'I'   : 0.41,
    'TO'  : 2.67, 'IT'   : 0.74, 'BUT' : 0.40,
    'A'   : 2.43, 'AS'   : 0.71, 'HAVE': 0.39,
    'IN'  : 2.31, 'AT'   : 0.58, 'AN'  : 0.37,
    'IS'  : 1.12, 'HIS'  : 0.55, 'HAS' : 0.35,
    'FOR' : 1.01, 'BY'   : 0.51, 'NOT' : 0.34,
    'THAT': 0.92, 'BE'   : 0.48, 'THEY': 0.33,
    'WAS' : 0.88, 'FROM' : 0.47, 'OR'  : 0.30
}

BIGRAM_FREQUENCIES = {
    'TH': 2.71, 'EN': 1.13, 'NG': 0.89,
    'HE': 2.33, 'AT': 1.12, 'AL': 0.88,
    'IN': 2.03, 'ED': 1.08, 'IT': 0.88,
    'ER': 1.78, 'ND': 1.07, 'AS': 0.87,
    'AN': 1.61, 'TO': 1.07, 'IS': 0.86,
    'RE': 1.41, 'OR': 1.06, 'HA': 0.83,
    'ES': 1.32, 'EA': 1.00, 'ET': 0.76,
    'ON': 1.32, 'TI': 0.99, 'SE': 0.73,
    'ST': 1.25, 'AR': 0.98, 'OU': 0.72,
    'NT': 1.17, 'TE': 0.98, 'OF': 0.71
}

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

QUADGRAM_FREQUENCIES = {
    'TION': 0.31, 'OTHE': 0.16, 'THEM': 0.12,
    'NTHE': 0.27, 'TTHE': 0.16, 'RTHE': 0.12,
    'THER': 0.24, 'DTHE': 0.15, 'THEP': 0.11,
    'THAT': 0.21, 'INGT': 0.15, 'FROM': 0.10,
    'OFTH': 0.19, 'ETHE': 0.15, 'THIS': 0.10,
    'FTHE': 0.19, 'SAND': 0.14, 'TING': 0.10,
    'THES': 0.18, 'STHE': 0.14, 'THEI': 0.10,
    'WITH': 0.18, 'HERE': 0.13, 'NGTH': 0.10,
    'INTH': 0.17, 'THEC': 0.13, 'IONS': 0.10,
    'ATIO': 0.17, 'MENT': 0.12, 'ANDT': 0.10
}

QUINTGRAM_FREQUENCIES = {
    'OFTHE': 0.18, 'ANDTH': 0.07, 'CTION': 0.05,
    'ATION': 0.17, 'NDTHE': 0.07, 'WHICH': 0.05,
    'INTHE': 0.16, 'ONTHE': 0.07, 'THESE': 0.05,
    'THERE': 0.09, 'EDTHE': 0.06, 'AFTER': 0.05,
    'INGTH': 0.09, 'THEIR': 0.06, 'EOFTH': 0.05,
    'TOTHE': 0.08, 'TIONA': 0.06, 'ABOUT': 0.04,
    'NGTHE': 0.08, 'ORTHE': 0.06, 'ERTHE': 0.04,
    'OTHER': 0.07, 'FORTH': 0.06, 'IONAL': 0.04,
    'ATTHE': 0.07, 'INGTO': 0.06, 'FIRST': 0.04,
    'TIONS': 0.07, 'THECO': 0.05, 'WOULD': 0.04
}


def generate_ascii_char():
    for i in range(0, 128):
        yield chr(i)


def xor_str(str1, str2):
    str = ''
    for c1, c2 in zip(str1, str2):
        str += chr(ord(c1)^ord(c2))
    return str


def count_non_english(string):
    english = '''
    abcdefghijklmnopqrstuvwxyz
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    1234567890~`!@#$%^&*()-_=+
    [{]}\|;:'",<.>/?
    '''
    count = 0
    for c in string:
        if not c in english:
            count += 1
    return count

def grade(string):
    score = 0.0
    score -= count_non_english(string)
    for monogram in MONOGRAM_FREQUENCIES.keys():
        if monogram in string or monogram.lower() in string:
            score += MONOGRAM_FREQUENCIES[monogram]
    for word in COMMON_ENGLISH_WORDS_FREQUENCIES.keys():
        if word in string or word.lower() in string:
            score += COMMON_ENGLISH_WORDS_FREQUENCIES[word]
    for bigram in BIGRAM_FREQUENCIES.keys():
        if bigram in string or bigram.lower() in string:
            score += BIGRAM_FREQUENCIES[bigram]
    for trigram in TRIGRAM_FREQUENCIES.keys():
        if trigram in string or trigram.lower() in string:
            score += TRIGRAM_FREQUENCIES[trigram]
    for quadgram in QUADGRAM_FREQUENCIES.keys():
        if quadgram in string or quadgram.lower() in string:
            score += QUADGRAM_FREQUENCIES[quadgram]
    for quintgram in QUINTGRAM_FREQUENCIES.keys():
        if quintgram in string or quintgram.lower() in string:
            score += QUINTGRAM_FREQUENCIES[quintgram]
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
