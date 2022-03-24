import base64

import requests
from io import BytesIO
from time import sleep
import datetime

import paho.mqtt.client as mqtt
from picamera import PiCamera

import keysRaspberry

host = keysRaspberry.hostHome
mqtt_ip = keysRaspberry.mqtt_ip
mqtt_port = keysRaspberry.mqtt_port
username = keysRaspberry.admin_username
password = keysRaspberry.admin_password

client = mqtt.Client('raspberryPi')
channelSend = "foto/get/dev0"
channelPost = "foto/taken/dev0"


def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    if data == "photo":
        enc = encode_base64(take_photo(channelPost))
        req_put(enc)
        print("Photo shot successfully")
    else:
        print("Can't execute %s!" % data)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connection established")
        return
    print("Error while connecting")


def publish_mqtt(channel, message):
    client.publish(channel, message)


def subscribe_mqtt(channel):
    client.subscribe(channel)


def encode_base64(data):
    base64_encoded_data = base64.b64encode(data)
    return base64_encoded_data.decode('utf-8')


def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)


def take_photo(channel):
    my_stream = BytesIO()
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture(my_stream, "jpeg")
    publish_mqtt(username, password, channel, "foto taken")
    return my_stream.getvalue()


def req_put(photo):
    response = requests.put("%s/%s" % (host, "1"), data={
        "TITLE": "Test",
        "DEVICE": "RaspberryPI",
        "UPLOADDATE": datetime.datetime.now(),
        "PICTURE": photo,
        "EXTENSION": "png",
        "DESCRIPTION": "test on raspberry pi"

    }).json()
    print(response)


def req_delete(id):
    response = requests.delete("%s/%s" % (host, str(id))).json()
    print(response)


def req_get(id):
    response = requests.get("%s/%s" % (host, str(id))).json()
    if "message" not in response:
        path = "/tmp/%s.%s" % (response["ID"], response["EXTENSION"])
        decode_Base64(path, response["PICTURE"])
        print("Picture saved in %s" % path)
    else:
        print(response)


if __name__ == '__main__':
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    print("Connecting...")
    client.connect(mqtt_ip, port=mqtt_port)
    print("Subscribing...")
    client.subscribe(channelSend)
    client.on_message = on_message
    client.loop_start()
    print("Finished!")
