# import statements
from tellodroneapi.Drone import Drone


class DroneConnection:
    def __init__(self, drone: Drone):
        self.drone = drone
