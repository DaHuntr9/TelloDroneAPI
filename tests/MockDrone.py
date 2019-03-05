from tellodroneapi.Drone import Drone, DroneResponse
from tellodroneapi.DroneConnection import DroneConnection
from tellodroneapi.DroneControls import DroneControl

DRONE_RESPONSES = {
    "battery?": "95",
    "temp?": "40-43 C",
    "speed?": "100.0",
    "baro?": "12.00",
    "height?": "100cm",
    "attitude?": "pitch:-5;roll:0;yaw:0;",
    "wifi?": "90",
    "tof?": "100dm",
    "acceleration?": "agx:-50.00;agy:11.00;agz:-999.00;"
}


class MockDrone(Drone):
    def __init__(self):
        super().__init__()
        self.control = DroneControl(self)
        self.connection = DroneConnection(self)
        self.drone_response = None

    async def connect(self) -> bool:
        self.connected = True
        return True

    def send_command(self, message: str) -> None:
        super(MockDrone, self).send_command(message)
        self.send_mock_command(message)

    async def await_drone_response(self, timeout: int) -> DroneResponse:
        response = self.drone_response
        self.drone_response = None
        return response

    async def send_command_and_await(self, message: str, timeout: int = None) -> DroneResponse:
        self.send_command(message)
        return await self.await_drone_response(timeout)

    def send_mock_command(self, command):
        self.drone_response = DRONE_RESPONSES.get(command, "Unknown Command: " + command)
