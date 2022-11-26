import requests

MAC_SIZE = 4

def mh5(x):
    state = 0

    # Apply padding
    x = x + b"\x80" # Terminate message with 0x80
    x = x + (MAC_SIZE - (len(x) % MAC_SIZE)) * b"\x00"

    # Split into chunks
    for i in range(0,len(x), MAC_SIZE):
        state += int.from_bytes(x[i:i+MAC_SIZE], byteorder="big")
        state &= (2**32 - 1)
    return state.to_bytes(length=MAC_SIZE, byteorder="big")

with requests.Session() as session:
    resp = session.get('https://t14.itsec.sec.in.tum.de')
    data = session.cookies['session']
    mac, session_data = data[:MAC_SIZE], data[MAC_SIZE:]
    replacement = '{"u": "admin"}'.encode()

	# TODO: Find Secret Key
    SECRET_KEY = bytes(mac.encode()) - bytes(session_data.encode())
    # mh5(SECRET_KEY + session_data) = mac

    mac = mh5(SECRET_KEY + replacement)
    data = mac.hex() + replacement.hex()
    session.cookies['session'] = data
    webpage = session.get('https://t14.itsec.sec.in.tum.de')
    print(webpage.content)