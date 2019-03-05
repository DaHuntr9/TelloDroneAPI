"""
import time
import cv2
from threading import Thread
from djitellopy.decorators import accepts
"""
import asyncio
import socket
import threading
import cv2

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
        super().__init__()
        # Prepare socket for connection with drone.
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.bind(('', self.DRONE_PORT))  # Prepare to listen for messages from drone

        self.control = DroneControl(self)
        self.connection = DroneConnection(self)

        self.cap = None
        self.cap_frame = None

        self.video_address = 'udp://@' + self.VIDEO_IP + ':' + str(self.VIDEO_PORT)

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

        self._initialize_drone_listener()
        self.send_command(command, ignore_error=True)
        response = await self.await_drone_response()
        if bool(response):
            self.connected = True

        return self.connected

    def get_capture_frame(self):
        """
        Initializes the drone's video capture and returns capture frame
        :return: Frame from video capture
        """
        if self.cap_frame is None:
            self.cap = cv2.VideoCapture(self.video_address)

            if not self.cap.isOpened():
                self.cap.open(self.video_address)

            _, self.cap_frame = self.cap.read()

            thread = threading.Thread(target=self.read_capture, args=())
            thread.daemon = True
            thread.start()

        return self.cap_frame

    def read_capture(self):
        while self.cap.isOpened():
            (_, self.cap_frame) = self.cap.read()

    def _initialize_drone_listener(self):
        """
        Starts another thread that listens for responses from the drone.
        :return: None
        """
        thread = threading.Thread(target=self._drone_response_listener)
        thread.daemon = True
        thread.start()

    def _drone_response_listener(self):
        """
        Infinite loop that constantly polls for responses from the drone and stores them in
        drone_response. This should be run on another thread to prevent blocking the rest of the
        application
        :return: None
        """
        while True:
            try:
                data, addr = self.sender.recvfrom(1024)  # buffer size is 1024 bytes
                # Convert response back into string since it's returned as bytes
                self.drone_response = data.decode('UTF-8').strip() or None
            except:
                # Ignore any errors here and hope for the next response to be good.
                pass

    def send_command(self, message, ignore_error=False):
        super(TelloDrone, self).send_command(message, ignore_error=ignore_error)
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
        Utility function to allow cleanly async-awaiting responses from the drone. Blocks until we
        get a response from the drone, then clears out drone_response and returns the last value.
        :return: The string response from the drone or None if there is no response.
        """
        while self.drone_response is None:
            pass
        else:
            result = self.drone_response
            self.drone_response = None
            return result
