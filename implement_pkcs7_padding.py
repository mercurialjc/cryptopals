#!/usr/bin/env python

"""Implement PKCS#7 padding
A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance,

"YELLOW SUBMARINE"
... padded to 20 bytes would be:

"YELLOW SUBMARINE\x04\x04\x04\x04"
"""
def pkcs7_padding(string, length):
    size = length - len(string)
    number_array = [size for i in range(size)]
    return string+str(bytearray(number_array))


def main():
    print pkcs7_padding('YELLOW SUBMARINE', 20)


if __name__ == '__main__':
    main()
