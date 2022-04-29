import json

import requests
import datetime
import base64

host = "http://192.168.0.42:5000/file"

encoded_string = ""

def encode_base64(data):
    base64_encoded_data = base64.b64encode(data)
    return base64_encoded_data.decode('utf-8')


with open("img/erwin.jpg", "rb") as image_file:
    encoded_string = encode_base64(image_file.read())

response = requests.put("%s/%s" % (host, "1"), data={
    "TITLE": "Test",
    "DEVICE": "PC",
    "UPLOADDATE": datetime.datetime.now(),
    "PICTURE": encoded_string,
    "EXTENSION": "jpg",
    "DESCRIPTION": "test services",
    "SERVICE": "analysis"
}).json()
print(json.dumps(response, indent=4))
