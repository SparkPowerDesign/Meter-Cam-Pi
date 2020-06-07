### Meter Camera MQTT Control v0.01 by Brad Hutson Jr @ 12/5/2019 ###

import paho.mqtt.client as mqttClient
import time
import uuid
import os
import datetime
import subprocess as sp
import psutil

ver = 0.01

#Set unique device ID (currently set to MAC address)
deviceid = hex(uuid.getnode())


#MQTT broker configuration
broker_address= "134.209.79.62"
port = 1883
user = "admin"
password = "admin"
topic = "Metercamera" #Main topic

print ('**** Meter Camera MQTT Control v0.01 ****')
print ('Device ID:', deviceid)

#Begin MQTT client init
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to MQTT broker.")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection to MQTT broker failed.")
 
def on_message(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    print("Message received:",message.payload)
    

    #Command List
    if message.payload == 'hello': #basic information about this device
        now = datetime.datetime.now()
        hellostring = "Hello there! I am {}, running version: v{}. My current Date/Time is: {}"
        print(hellostring.format(deviceid, ver, now.strftime("%Y-%m-%d %H:%M")))
        client.publish(topic+'/'+deviceid+'/control',hellostring.format(deviceid, ver, now.strftime("%Y-%m-%d %H:%M")))
        
    if message.payload == 'capture': #Forces device to take a picture
        print('Capturing picture now...')
        os.system('python3 meter-pub.py')
        
    if message.payload == 'capturetimed': #Starts the image capture timed script
        print('Launching timed image capture script...')
        pid = open("pid","r") #Read pid file
        pidnum = pid.read()
        pid.close()
        if pidnum == '': #Checks if pid is present, if so timed script is already running and will not start another
            extProc = sp.Popen(['python3','meter-pub-timed.py'])
            global procpid
            procpid = extProc.pid
            print ('Timed capture script started with PID',procpid)
        else:
            print ('Timed capture script already started with PID',pidnum)

    if message.payload == 'stopcapturetimed': #Stops the image capture timed script, only if launched by this script
        pid = open("pid","r") #Read pid file
        pidnum = pid.read()
        pid.close()
        print('Attempting to stop timed capture script...')
        if pidnum == '': #Check if script is running
            print ('Timed capture script is not running')
        else:
            print('Stoping timed image capture script running with PID',pidnum)
            pidnumint = int(pidnum)
            parent = psutil.Process(pidnumint)
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()
            pidnum = '' 
            pid = open("pid","w+")
            pid.write('{}'.format(pidnum)) #Write a blank to pid file
            pid.close()
        
    if message.payload == 'terminate': #Forces this script to exit
        print('Exiting script...')
        exit()


Connected = False   #global variable for the state of the connection
 
 
client = mqttClient.Client("Python sub")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe(topic+'/'+deviceid+'/control')
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("Exiting...")
    client.disconnect()
    client.loop_stop()
