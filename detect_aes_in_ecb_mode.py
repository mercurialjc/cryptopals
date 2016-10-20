#!/usr/bin/env python

"""Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
"""
def read_ciphertext(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.rstrip('\n'))
    return lines


def similarity(line):
    count = 0
    s = line.decode('hex')
    for i in range(len(s)):
        if i+16 < len(s) and s[i] and s[i+16]:
            if s[i] == s[i+16]:
                count += 1
    return count
        

def most_determinlistic_entry(lines):
    return sorted(lines,
                  key=lambda line:similarity(line),
                  reverse=True)[0]

def main():
    lines = read_ciphertext('8.txt')
    num = len(lines)
    size = 5
    print most_determinlistic_entry(lines)
    

if __name__ == '__main__':
    main()
