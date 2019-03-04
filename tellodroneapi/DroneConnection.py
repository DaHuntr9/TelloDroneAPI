# import statements
from tellodroneapi.Drone import Drone


class DroneConnection:
    def __init__(self, drone: Drone):
        self.drone = drone

    async def get_battery_level(self) -> int:
        return await self.drone.send_command_and_await("battery?")

    async def get_temperature(self) -> int:  # In celsius
        return await self.drone.send_command_and_await("temp?")
