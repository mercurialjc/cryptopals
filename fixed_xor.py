#!/usr/bin/env python

"""Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
"""
import hex_to_base64

def xor(hex_str1, hex_str2):
    bytes1 = hex_to_base64.hex_to_bytes(hex_str2)
    bytes2 = hex_to_base64.hex_to_bytes(hex_str1)
    xor_str = ''
    for (byte1, byte2) in zip(bytes1, bytes2):
        xor_byte = byte1 ^ byte2
        xor_str += str(hex(xor_byte)[2:])
    return xor_str


def main():
    hex_str1 = '1c0111001f010100061a024b53535009181c'
    hex_str2 = '686974207468652062756c6c277320657965'
    print xor(hex_str1, hex_str2)

if __name__ == '__main__':
    main()
