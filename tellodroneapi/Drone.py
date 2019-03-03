class Drone:
    """
    A base class representing a drone. Implementations of Drones should be subclasses of this class.
    """
    async def connect(self) -> bool:
        """
        Attempts to connect to a drone device.
        :return: True if successfully connected, otherwise False
        """
        raise RuntimeError("Connecting has not been implemented by this drone.")

    async def send_command(self, message: bytes) -> None:
        """
        Sends a message to a drone device.
        :param message: str The message or command to send to the drone.
        :return: None
        """
        pass

    async def await_drone_response(self, timeout: int) -> str or None:
        """
        Waits for a response from the drone to verify a command has been received, optionally timing
        out if there's no response.
        :param timeout: int The amount of time, in seconds to wait before considering this a timeout.
        :return: The string response from the drone, or None if there is no response.
        """
        pass
