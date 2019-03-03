"""
import time
import cv2
from threading import Thread
from djitellopy.decorators import accepts
"""
import asyncio
import socket

from tellodroneapi.Drone import Drone, DroneResponse
from tellodroneapi.DroneControls import DroneControl
from tellodroneapi.DroneConnection import DroneConnection


class TelloDrone(Drone):
    # This is the address and port that the drone will send and receive messages.
    # IP address of drone when on drone network.
    DRONE_IP = '192.168.10.1'

    """
    UDP PORT for the drone controls to be send on this network.
    Set up a UDP client on PC, Mac or Mobile device to send,
    and receive message from Tello via the same port.
    """
    DRONE_PORT = 8889
    DRONE_RECV_PORT = 8890

    # Variables to be implemented
    # Time out for responses from and to the drone
    # Last time the communication was made with the drone.

    # Video Stream port and server address provided by the SDK
    VIDEO_IP = '0.0.0.0'
    VIDEO_PORT = 11111

    DEFAULT_TIMEOUT = 3  # seconds

    # need to create a capturing object Pref OPEN CV2

    # Constructor of Drone Class
    def __init__(self):
        # Prepare socket for connection with drone.
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.settimeout(self.DEFAULT_TIMEOUT)
        self.sender.bind(('', self.DRONE_RECV_PORT))  # Prepare to listen for messages from drone
        self.drone_response = None

        self.control = DroneControl(self)
        self.connection = DroneConnection(self)

    # This is going to set up the socket for the connection to be established to the drone.
    async def connect(self):
        """
        Establishes and attempts to connect to a drone by sending the initial "command" command.
        :return: True if a connection was successful, or False otherwise.
        """
        print("Establishing connection to...")
        print("Target IP:", self.DRONE_IP)
        print("Target UDP PORT:", self.DRONE_PORT)
        command = 'command'

        self.send_command(command)
        self.drone_response = await self.await_drone_response()

        return bool(self.drone_response)

    def send_command(self, message):
        message_as_bytes = bytes(message, 'UTF-8')
        self.sender.sendto(message_as_bytes, (self.DRONE_IP, self.DRONE_PORT))

    async def await_drone_response(self, timeout=DEFAULT_TIMEOUT) -> DroneResponse:
        """
        Waits for a response from the drone's UDP connection, optionally timing
        out if there's no response.
        :param timeout: int The amount of time, in seconds to wait before considering this a timeout
        :return: The string response from the drone, or None if there is no response.
        """
        result = await asyncio.wait_for(self._wait_for_response(), timeout=timeout)
        return result

    async def send_command_and_await(self, message: str,
                                     timeout: int = DEFAULT_TIMEOUT) -> DroneResponse:
        self.send_command(message)
        return await self.await_drone_response(timeout)

    async def _wait_for_response(self):
        """
        Utility function to allow cleanly async-awaiting responses from the drone.
        :return: The string response from the drone or None if there is no response.
        """
        try:
            data, addr = self.sender.recvfrom(1024)  # buffer size is 1024 bytes
            # Convert response back into string since it's returned as bytes
            return data.decode('UTF-8')
        except socket.timeout:
            return None
