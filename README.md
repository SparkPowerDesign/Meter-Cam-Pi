# Meter-Cam-Pi
Raspberry Pi based meter camera

Basic implementation of a Rasberry Pi based meter camera.
Allows for the Pi equiped with a Picam to take a picture on an interval and submits to an mqtt server with base64 image conversion, or to respond to mqtt commands for image capture.

Features include a timed mode to take pictures and transmit via mqtt on a specified interval.


Files Included:

meter-pub.py - Allows the device to submit a base64 encoded pic when ran via mqtt (One shot).

meter-sub.py - Allows the device to listen for commands issued via mqtt to take a picture and submit base64 encoded pic via mqtt.

meter-pub-timed.py - Allows the device to submit a picture on a timed interval and submit base64 encoded pic via mqtt.

pid - Temp storage file for script process id (this is sloppy, needs fixing)




Written in python

Uses Raspberry Pi hardware equiped with a Pi Cam.

TODO:

-Better handling of process detection
