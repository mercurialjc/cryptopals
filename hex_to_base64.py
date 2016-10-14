#!/usr/bin/env python

"""Convert hex to base64
The string:
'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
Should produce:
'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
So go ahead and make that happen. You'll need to use this code for the rest of the exercises.

Cryptopals Rule:
Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.
"""

import sys
import base64

def hex_to_bytes(hex_str):
    return bytearray.fromhex(hex_str)


def bytes_to_base64(bytes):
    return base64.b64encode(bytes)


def hex_to_base64(hex):
    return bytes_to_base64(hex_to_bytes(hex))


def main():
    hex_str = sys.argv[1]
    print hex_to_base64(hex_str)


if __name__ == '__main__':
    main()
