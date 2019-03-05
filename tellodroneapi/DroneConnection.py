# import statements
from tellodroneapi.Drone import Drone


class DroneConnection:
    def __init__(self, drone: Drone):
        self.drone = drone

    async def get_battery_level(self) -> int:
        """
        Returns the drone's current battery level.
        :return: str
        """
        return int(await self.drone.send_command_and_await("battery?"))

    async def get_temperature(self) -> str:
        """
        Returns drone temperature in celsius. Depending on drone firmware, this may return a
        range instead of an exact number.
        :return: str
        """
        return await self.drone.send_command_and_await("temp?")

    async def get_velocity(self) -> float:
        """
        Gets drone velocity in centimeters per second.
        :return: int
        """
        return float(await self.drone.send_command_and_await("speed?"))

    async def get_altitude(self) -> int:
        """
        Returns the drone's using it's barometric calculations.
        :return: int
        """
        return int(await self.drone.send_command_and_await("baro?"))

    async def get_height(self) -> str:
        """
        Returns the current height from the drone's starting point.
        :return: str
        """
        return await self.drone.send_command_and_await("height?")

    async def get_attitude(self) -> (int, int, int):
        """Returns drone IMU attitude information as a tuple ordered as (pitch, roll, yaw)
        :return (pitch, roll, yaw)
        """
        attitude = await self.drone.send_command_and_await("attitude?")
        # Example drone response: 'pitch:-5;roll:0;yaw:0;'
        pitch, roll, yaw = attitude.strip().split(";")[0:3]
        return _get_state_value(pitch), _get_state_value(roll), _get_state_value(yaw)

    async def get_pitch(self):
        pitch, _, _ = await self.get_attitude()
        return pitch

    async def get_roll(self):
        _, roll, _ = await self.get_attitude()
        return roll

    async def get_yaw(self):
        _, _, yaw = await self.get_attitude()
        return yaw

    async def get_wifi_strength(self) -> int:
        """Returns wifi signal strength"""
        return int(await self.drone.send_command_and_await("wifi?"))

    async def get_distance_from_floor(self) -> str:
        """
        Returns drone distance from floor
        :return: str
        """
        return await self.drone.send_command_and_await("tof?")

    async def get_acceleration(self) -> (int, int, int):
        """
        Returns drone acceleration as a tuple with each axis a separate entry.
        :return: (x_acceleration, y_acceleration, z_acceleration)
        """
        # Example response from drone: 'agx:-50.00;agy:11.00;agz:-999.00;'
        acceleration = await self.drone.send_command_and_await("acceleration?")
        accel_x, accel_y, accel_z = acceleration.split(';')[0:3]

        return _get_state_value(accel_x), _get_state_value(accel_y), _get_state_value(accel_z)

    async def get_acceleration_x(self):
        accel_x, _, _ = await self.get_acceleration()
        return accel_x

    async def get_acceleration_y(self):
        _, accel_y, _ = await self.get_acceleration()
        return accel_y

    async def get_acceleration_z(self):
        _, _, accel_z = await self.get_acceleration()
        return accel_z


def _get_state_value(pair: str):
    """
    Splits a given string at the first colon and returns the second element of the resulting array.
    This is used since tello state returns things in key-value pairs.
    :param pair:
    :return:
    """
    return pair.split(':')[1]
