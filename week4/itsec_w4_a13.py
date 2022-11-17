import binascii
import socket
import telnetlib

BLOCK_SIZE = 16
# First take a look at the server. Afterwards, comment out the next three lines...
#t = telnetlib.Telnet("itsec.sec.in.tum.de", 7023)
#t.interact()
#sys.exit(0)

# If you have done that, copy over a hexlified message + IV over to this script (replacing the zeros)
iv = binascii.unhexlify("8a35c5ee7d333227a216340090fb0f3c")
msg = binascii.unhexlify("20ed304fe76e08ceeabe2cce810a1d2cd1163075d8c53f8cbdd061aaa6d356b7f5d3b23fa2a1135872e01114e277ca33019d98a7edd4f6771a5e56829ef1fbbe")

def read_until(s, token):
    """Reads from socket `s` until a string `token` is found in the response of the server"""
    buf = b""
    while True:
        data = s.recv(2048)
        buf += data
        if not data or token in buf:
            return buf

# The server allows you to process a single message with each connection.
# Connect multiple times to decrypt the (IV, msg) pair above byte by byte.
#for i in range(len(msg)):
for j in range(256):
    s = socket.socket()
    s.connect(("itsec.sec.in.tum.de", 7023))

    start = read_until(s, b"Do you")

    ########################################
    # Implement padding oracle attack here #
    ########################################

    new_msg = bytearray(msg)
    new_msg[-BLOCK_SIZE] = 228
    new_msg[-BLOCK_SIZE-1] = j
    s.send(binascii.hexlify(iv) + b"\n")
    s.send(binascii.hexlify(new_msg) + b"\n")

    response = read_until(s, b"\n")
    if b'OK' in response:
        print(str(j) + " " + str(response))
    #print(str(j) + " " + str(response))

#padding \x04\x04\x04\x04
#padding \x04\x04\x04\x01

#001 - 00000001 xor I = x
#160 - 10100000 xor I = 1
#175 - 10101111 xor I = 1
#228 - 11100100 xor I = 1