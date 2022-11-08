import socket
import re

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

def message_to_server(s, msg):
    """This function will encode a message for sending it to the server"""
    assert (isinstance(msg, int)), "Expected a number/integer as message for the server!"
    msg = msg.to_bytes(length=2048//8, byteorder="little")
    s.send(msg.hex().encode() + b'\n')
    resp = recv_until(s, b"\n")
    return resp.decode()

s = socket.socket()
print("[+] Connecting to ITSec challenge")
s.connect(("itsec.sec.in.tum.de", 7010))
data = recv_until(s, b"just fake news...")

print("[+] Printing server message")
# Print message from the server to the console. Please read what the server tells you!
print(data.decode())

# Extract RSA constants from the message
N = int(re.search(b"N=(\d+)", data).group(1))
e = int(re.search(b"e=(\d+)", data).group(1))

sniffed_message = bytes.fromhex(re.search(b"me today: ([0-9a-f]+)", data).group(1).decode())
sniffed_message_int = int.from_bytes(sniffed_message, byteorder="little")

# TODO: Your code goes here!

# This code snippet might be useful to get the flag!
new_msg = pow(2, e, N)
new_msg = (sniffed_message_int * new_msg) % N
print("[+] Asking server to decrypt a message for us")
resp = message_to_server(s, new_msg)
result = re.search("hex\): ([0-9A-Fa-f]+)", resp).group(1)
i = bytes.fromhex(result.strip())
i_int = int.from_bytes(i, byteorder="little") // 2
res = i_int.to_bytes(length=2048//8, byteorder="little")
print(res.decode())