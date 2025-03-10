import random
import os


def encrypt(data, m, q=1):
    res = []
    for x in data:
        enc = (m*x+q) & 0xff
        res.append(enc)
    return bytes(res)


def main():
    key = 2*random.randint(0, 1 << 128)+1
    ciphertext = encrypt("7f1d26c428628a1dd436311d36b0054536f1a79c62f1f59c7b4a8ffc9ca7f19c31bbf16b1dc062e6b2".encode(), key)
    print(ciphertext.hex())


main()
