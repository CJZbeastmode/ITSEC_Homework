import json
import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

BLOCK_LENGTH = 16

def byte_wise_xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

with requests.Session() as session:
    resp = session.get('https://t12.itsec.sec.in.tum.de')
    data = bytes.fromhex(session.cookies['session'])
    iv, ciphertext = data[:BLOCK_LENGTH], data[BLOCK_LENGTH:]    

    plaintext = pad(json.dumps({"u": "tester"}).encode(), BLOCK_LENGTH)
    replacement = pad(json.dumps({"u": "admin"}).encode(), BLOCK_LENGTH)
    difference = byte_wise_xor(plaintext, replacement)
    new_iv = byte_wise_xor(iv, difference)
    
    session.cookies.clear()
    session.cookies['session'] = (new_iv + ciphertext).hex()
    webpage = session.get('https://t12.itsec.sec.in.tum.de')
    print(webpage.content)