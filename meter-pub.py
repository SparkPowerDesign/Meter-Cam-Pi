### Meter Camera Capture and publish v0.01 by Brad Hutson Jr @ 12/5/2019 ###

import paho.mqtt.client as mqttClient
import time
import picamera
import base64
import uuid


#Set unique device ID
deviceid = hex(uuid.getnode())

#MQTT Broker Configuration
broker_address= "134.209.79.62"
port = 1883
user = "admin"
password = "admin"
topic = "Metercamera" #Main topic

print ('**** Meter Camera Capture and Publish v0.01 ****')
print ('Device ID:', deviceid)
#Setup Pi Camera and take a picture
camera = picamera.PiCamera()
try: 
    print('Capturing picture...')
    camera.start_preview()
    time.sleep(1)
    camera.capture('image.jpg', resize=(320,240))
    camera.stop_preview()
    pass
finally:
    camera.close()
    print ('Picture capture successful.')
 
 
#Convert to Base64
image = 'image.jpg'
image_64 = base64.encodebytes(open(image,"rb").read())
print ('Base64 conversion complete.')

#Publish via MQTT
def on_connect(client, userdata, flags, rc):

    if rc == 0:
 
        print("Connected to MQTT broker:", broker_address)
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection to MQTT broker failed.")
 
Connected = False   #global variable for the state of the connection
 

 
client = mqttClient.Client("Python pub")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker


client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    if True:
        print("Publishing Base64 image data to topic:", topic+'/'+deviceid)
        client.publish(topic+'/'+deviceid,image_64)
        print("Publish successful!")
        
finally:
    print ("Exiting...")
    client.disconnect()
    client.loop_stop()
