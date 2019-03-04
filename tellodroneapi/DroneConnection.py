# import statements
from tellodroneapi.Drone import Drone


class DroneConnection:
    def __init__(self, drone: Drone):
        self.drone = drone

    async def get_battery_level(self) -> str:
        """
        Returns the drone's current battery level. Depending on drone firmware, this may return a
        range instead of an exact number.
        :return: str
        """
        return await self.drone.send_command_and_await("battery?")

    async def get_temperature(self) -> str:
        """
        Returns drone temperature in celsius.
        :return:
        """
        return await self.drone.send_command_and_await("temp?")

    async def get_velocity(self) -> int:
        """
        Gets drone velocity in centimeters per second.
        :return: int
        """
        return int(await self.drone.send_command_and_await("speed?"))

    async def get_pressure(self) -> int:
        return int(await self.drone.send_command_and_await("baro?"))

    async def get_height(self) -> int:
        """
        Returns the current height from the drone's starting point in centimeters.
        :return: int
        """
        return int(await self.drone.send_command_and_await("height?"))
