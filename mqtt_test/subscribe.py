import paho.mqtt.client as mqtt
import time

import keysServer

admin_username = keysServer.admin_username
password = keysServer.admin_password
ip = keysServer.mqtt_ip
port = keysServer.mqtt_port


# Diese paar Zeilen Code reichen aus um sich bei einem Channel einzuschreiben
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connection established")
        return
    print("Error while connecting")


# Diese Methode wird aufgerunfen, wenn eine Nachricht fuer einen Channel hereinkommt
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


# Wenn Logging-Information fuer den Client vorhanden ist (gut fuer das Fehlersuchen)
def on_log(client, userdata, level, buf):
    print("log: ", buf)


if __name__ == '__main__':
    client = mqtt.Client('test')  # Der Parameter ist die client-ID, diese sollte möglichst eindeutig sein.
    client.username_pw_set(admin_username, password)
    client.on_connect = on_connect
    client.connect(ip,port=port)

    client.subscribe("house/light")  # Eintragen fuer einen bestimmten Channel
    client.on_message = on_message  # die on_message-Methode soll aufgerfufen werden wenn einen neue Nachricht hereinkommt
    client.on_log = on_log
    client.loop_start()  # loop starten
    # client.loop_forever() # loop starten in Endlosschleife (blockiert)
    time.sleep(1000000)
    print("EXIT")
