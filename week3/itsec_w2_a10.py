import re
import socket
import binascii
from Crypto.Cipher import AES
import gmpy2

def recv_until(s, needle):
    """Receive data from a socket connection until the needle appears"""
    buf = b""
    while True:
        b = s.recv(1024)
        if not b:
            break
        buf += b
        if needle in buf:
            return buf
    return buf

s = socket.socket()
s.connect(("itsec.sec.in.tum.de", 7012))
data = recv_until(s, b"Can you help us with the decryption?")
print(data.decode())

N = int(re.search(b"N = ([0-9a-f]+)", data).group(1), 16)
e = int(re.search(b"e = (\d+)", data).group(1))

enc_k = re.search(b"enc_k = ([0-9a-f]+)", data).group(1)
enc_k = int(enc_k.decode(), 16)
iv = bytes.fromhex(re.search(b"iv = ([0-9a-f]+)", data).group(1).decode())
enc_msg = binascii.unhexlify(re.search(b"enc_msg = ([0-9a-f]*)", data).group(1))

# TODO: Compute the key *somehow* that is transmitted RSA encrypted
key = int(gmpy2.iroot(enc_k, e)[0]).to_bytes(length=16, byteorder="big")
cipher = AES.new(mode=AES.MODE_CTR, nonce=iv, key=key)
msg = cipher.decrypt(enc_msg)
print("Decrypted message:", msg.decode())
