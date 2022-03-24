# PhotoServer

## Starting mosquitto: 
- execute cmd as admin
- "net start mosquitto"
- overwrite mosquitto.conf with mosquitto.conf in mqtt_test
- execute mosquitto_passwd.exe -c <pw.txt> <username> <br> (if you change name of pw.txt, you have to change it in mosquitto.conf too)