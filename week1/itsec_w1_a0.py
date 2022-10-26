import requests

with requests.Session() as sess:
    response = sess.get("https://t0.itsec.sec.in.tum.de")
    print(response.text)
