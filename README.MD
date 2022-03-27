# PhotoServer

## Creating keys:

## Starting mosquitto: 
- overwrite mosquitto.conf with mosquitto.conf in mqtt_test
- execute mosquitto_passwd.exe -c <pw.txt> <username> 
<br> (if you change name of pw.txt, you have to change it in mosquitto.conf too)
- execute cmd as admin
- "net start mosquitto" or "mosquitto.exe -v -c mosquitto.conf" (better is last)

## Starting client on RapsberryPi:
- install all needed library's (pip install paho-mqtt, ...)
- run script: 
    - sudo python3 client_request.py 
    - or sudo /usr/bin/python client_request.py

## Starting client in Java: