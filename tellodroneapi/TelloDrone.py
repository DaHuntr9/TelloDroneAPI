"""
import time
import cv2
from threading import Thread
from djitellopy.decorators import accepts
"""
import asyncio
import socket
import threading
from tellodroneapi.DroneControls import DroneControl
from tellodroneapi.DroneConnection import DroneConnection


class Drone:
    drone_control = DroneControl()
    drone_connection = DroneConnection()
    sender = None
    receiver = None
    # IP address of drone when on drone network.
    DRONE_IP = '192.168.10.1'

    """
    UDP PORT for the drone controls to be send on this network.
    Set up a UDP client on PC, Mac or Mobile device to send,
    and receive message from Tello via the same port.
    """
    DRONE_PORT = 8889 
    
    # Variables to be implemented
    # Time out for responses from and to the drone
    # Last time the communication was made with the drone.

    # Video Stream port and server address provided by the SDK
    VIDEO_IP = '0.0.0.0'
    VIDEO_PORT = 11111

    # need to create a capturing object Pref OPEN CV2

    # Constructor of Drone Class
    def __init__(self):
        # This is the address and port that the drone will send and receive messages.
        self.connect()
        self.listen()

    # This is going to set up the socket for the connection to be established to the drone.
    def connect(self):
        print("Establishing connection to...")
        print("Target IP:", self.DRONE_IP)
        print("Target UDP PORT:", self.DRONE_PORT)
        command = b'command'
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.sendto(command, (self.DRONE_IP, self.DRONE_PORT))

    # Creates a listens to the drone has sent a message back.
    def listen(self):
        receiver = threading.Thread(target=self.run_udp_receiver, args=())  # Calls function to listen on the port
        receiver.daemon = True  # closing connection issues dealt here
        receiver.start()  # executes receiver thread

    # Listens for if a Message is send back on this port.
    def run_udp_receiver(self):
        try:
            asyncio.wait_for(self.wait_for_response(), timeout=1.0)
        except asyncio.TimeoutError:
            print('timeout!')

    # async receiver
    async def wait_for_response(self):
        while True:
            data, addr = self.sender.recvfrom(self.DRONE_PORT)  # buffer size is 1024 bytes
            print("received message:", data)
            if data is not None:
                print("Successful Connection!")
                return True
