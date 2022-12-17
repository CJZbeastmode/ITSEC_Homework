import socket
import json


import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as Padding

the_socket = socket.socket()
the_socket.connect(("itsec.sec.in.tum.de", 7053))
#the_socket.connect(("0.0.0.0", 8888))
the_bytes = b""

def decrypt(key, data):
    return  Padding.unpad(AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(data)),16)

class ServerError(Exception):
    pass

def recv_msg(the_socket):
    the_bytes = b""
    while True:
        next_byte = the_socket.recv(1)
        # just create more strings all the time....
        the_bytes += next_byte
        if next_byte == b'\n':
            msg = json.loads(the_bytes)
            print(" <", msg)
            if msg["action"] == "error":
                raise ServerError(msg["msg"])
            return msg

def recv_until(the_socket, needle):
    the_bytes = b""
    buf = b""
    while True:
        buf = the_socket.recv(1)
        if buf == b"":
            break
        the_bytes += buf
        if needle in the_bytes:
            break
    return the_bytes

def send(the_socket, msg):
    msg = json.dumps(msg) + "\n"
    print(f" > {msg}", end="", flush=True)
    the_socket.sendall(msg.encode())

def bytearray_xor(one, two):
    return bytearray(a ^ b for (a, b) in zip(one, two))

prelude = recv_until(the_socket, b"END  SETUP****\n").decode("ascii")
print(prelude)

# Key request
the_next = recv_msg(the_socket)
send(the_socket,the_next)

# Send otp to Admin
the_next = recv_msg(the_socket)
send(the_socket,the_next)

# Send Publish to Flagpublisher
the_next = recv_msg(the_socket)
for i in range(25):
    send(the_socket,the_next)

#Publish flag
flag = ""
for i in range(25):
    the_next = recv_msg(the_socket)
    flag += the_next['publicmessage']
print(flag)
