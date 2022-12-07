import hashlib
from random import randint
from random import shuffle, getrandbits


table = list(range(0, 256))
shuffle(table)

def generate_secret_key():
    secretkey = []
    for i in range(256):
        secretkey_pair = [getrandbits(256), getrandbits(256)]
        secretkey.append(secretkey_pair)
    return secretkey

def generate_open_key(secretkey):
    openkey = []
    for keypair_ in secretkey:
        openkey_pair = [hash256(keypair_[0]), hash256(keypair_[1])]
        openkey.append(openkey_pair)
    return openkey

def hash8(message):
    message = str(message)
    hash_ = len(str(message)) % 256
    for i in message:
        hash_ = table[(hash_ + ord(i)) % 256]
    return "{0:b}".format(hash_)

def hash256(message):
    message = str(message)
    hashcode = hashlib.sha256(message.encode('utf-8')).hexdigest()
    result = bin(int(hashcode, 16))
    return result.lstrip('0b')

def hash128(message):
    message = str(message)
    hashcode = hashlib.md5(message.encode('utf-8')).hexdigest()
    result = bin(int(hashcode, 16))
    return result.lstrip('0b')

def sign(message, secretkey):
    signature_ = []
    message_hashed = hash256(message)
    for i, bit in enumerate(message_hashed):
        signature_.append(secretkey[i][int(bit)])
    return signature_

def verify(signature_, message, openkey):
    message_hashed = hash256(message)
    hashed_mes = []
    sign_hashed = []
    for i, bit in enumerate(message_hashed):
        hashed_mes.append(openkey[i][int(bit)])
    for digit in signature_:
        sign_hashed.append(hash256(digit))
    print(hashed_mes)
    print(sign_hashed)
    return hashed_mes == sign_hashed