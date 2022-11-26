import requests
import os

MAC_SIZE = 4


def mh5(x):
    state = 0

    # Apply padding
    x = x + b"\x80"  # Terminate message with 0x80
    x = x + (MAC_SIZE - (len(x) % MAC_SIZE)) * b"\x00"

    # Split into chunks
    for i in range(0, len(x), MAC_SIZE):
        state += int.from_bytes(x[i:i + MAC_SIZE], byteorder="big")
        state &= (2 ** 32 - 1)
    return state.to_bytes(length=MAC_SIZE, byteorder="big")

with requests.Session() as session:
    resp = session.get('https://t14.itsec.sec.in.tum.de')
    data = session.cookies['session']
    mac, session_data = data[:MAC_SIZE], data[MAC_SIZE:]
    replacement = '{"u": "admin"}'.encode()

    # TODO: Find Secret Key
    SECRET_KEY = int.from_bytes(bytes(mac.encode()), byteorder="big") - int.from_bytes(mh5(bytes(session_data.encode())), byteorder="big") + (2 ** 32 - 1)
    SECRET_KEY &= (2 ** 32 - 1)
    # mh5(SECRET_KEY + session_data) = mac
    new_mac = SECRET_KEY + int.from_bytes(mh5(replacement), byteorder="big")
    new_mac &= (2 ** 32 - 1)

    data = new_mac.to_bytes(length=MAC_SIZE, byteorder="big").hex() + replacement.hex()
    session.cookies['session'] = data
    webpage = session.get('https://t14.itsec.sec.in.tum.de')
    print(webpage.content)

"""
MAC = 1011

SecretKey = 
1101

SessionData = 
1100
0000
0011
0001

NewMac = 
1111

NewSessionData =
0001
0010
0110
0111
"""
