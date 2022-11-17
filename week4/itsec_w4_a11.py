import base64
import json
import requests

NONCE_LENGTH = 12

def encrypt1(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

with requests.Session() as session:
    resp = session.post('https://t11.itsec.sec.in.tum.de/login', data={"username": "testuser", "password": "foobar"})

    print(session.cookies)
    data = base64.b64decode(session.cookies['session'])
    nonce, ciphertext = data[:NONCE_LENGTH], data[NONCE_LENGTH:]
    stromtext = encrypt1(json.dumps({"user": "testuser"}).encode(), ciphertext)
    print(len(stromtext))
    print(len(json.dumps({"user": "admin"}).encode()))
    result = encrypt1(stromtext, json.dumps({"user": "admin"}).encode())
    session.cookies['session'] = base64.b64encode(nonce + result).decode()
    print(session.cookies)

    webpage = session.get('https://t11.itsec.sec.in.tum.de')
    print(webpage.content)
    data = session.cookies
    print(data)