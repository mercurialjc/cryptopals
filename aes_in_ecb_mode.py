#!/usr/bin/env python

"""AES in ECB mode
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

Do this with code.
You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. You'll need it a lot later on, and not just for attacking ECB.
"""

import break_repeating_key_xor
from Crypto.Cipher import AES

def decrypt(ciphertext, key):
    IV = 16 * '\x00'
    decryption_suite = AES.new(key, AES.MODE_ECB, IV)
    return decryption_suite.decrypt(ciphertext)


def main():
    ciphertext = break_repeating_key_xor.read_ciphertext('7.txt')
    key = 'YELLOW SUBMARINE'
    plaintext = decrypt(ciphertext, key).strip('\n')
    print plaintext


if __name__ == '__main__':
    main()
