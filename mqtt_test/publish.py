import paho.mqtt.client as mqtt
import keysServer

username = keysServer.admin_username
password = keysServer.admin_password
ip = keysServer.mqtt_ip
port = keysServer.mqtt_port


def on_publish(client, userdata, result):
    print("data published \n")
    pass


client = mqtt.Client('publish_test')
client.username_pw_set(username, password)
client.on_publish = on_publish
client.connect(ip, port=port)

send = client.publish("foto/get/dev0", "photo")
