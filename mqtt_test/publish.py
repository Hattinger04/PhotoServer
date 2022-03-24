import paho.mqtt.client as mqtt
import keysServer

admin_username = keysServer.admin_username
password = keysServer.admin_password
ip = keysServer.mqtt_ip
port = keysServer.mqtt_port

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connection established")
        return
    print("Error while connecting")


client = mqtt.Client('X12')  # Der Parameter ist die client-ID, diese sollte möglichst eindeutig sein.
client.username_pw_set(admin_username, password)
client.connect(ip, port=port)  # Im Moment verwenden wir die lokale mosquitto Installation, spaeter durch die IP zu ersetzen

client.publish("foto/get/dev0", "ON")
