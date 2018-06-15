import aes
from secret import *
import utils

cipher = aes.AESCipher(SECRET)


def encrypt(data):
    return cipher.encrypt(data)


def decrypt(data):
    return cipher.decrypt(data)


if __name__ == "__main__":
    for i in range(100):
        data = utils.get_random_seed()
        assert data == cipher.decrypt(cipher.encrypt(data))
