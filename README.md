# Meter-Cam-Pi
Raspberry Pi based meter camera

Basic implementation of a Rasberry Pi based meter camera.
Takes a picture on an interval and submits to an mqtt server with base64 image conversion.

Features include a timed mode to take pictures and transmit via mqtt on a specified interval.

Files Included:

meter-pub.py - Allows the device to submit a picture when ran via mqtt.
meter-sub.py - Allows the device to listen for commands issued via mqtt to take a picture and submit base64 encoded pic via mqtt.
meter-pub-timed.py - Allows the device to submit a picture on a timed interval and submit base64 encoded pic via mqtt.


Written in python

Uses Raspberry Pi hardware equiped with a Pi Cam.

TODO:

-Better handling of process detection
