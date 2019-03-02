"""
import socket
import time
import threading
import cv2
from threading import Thread
from djitellopy.decorators import accepts
"""

class Drone:
    #IP address of drone when on drone network. 
    DRONE_IP = '192.168.10.1'
    
    """
    UDP PORT for the drone controls to be send on this network.
    Set up a UDP client on PC, Mac or Mobile device to send,
    and receive message from Tello via the same port.
    """
    DRONE_PORT = 8889 
    
    #Variables to be implemented
    #Time out for responses from and to the drone
    #Last time the communcation was made with the drone.

    #Video Stream port and server address provided by the SDK
    #Do Remark2 if you haven’t. Then send “streamon” command to Tello via UDP PORT 8889 to start the streaming. 
    VIDEO_IP = '0.0.0.0' 
    VIDEO_PORT = 11111

    #need to create a capturing object Pref OPEN CV2

    #Constructor of Drone Class
    def __init__(self):
        #This is the address and port that the drone will send and receive messages.
        self.address();