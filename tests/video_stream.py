import cv2
from tellodroneapi.TelloDrone import TelloDrone
import asyncio


async def main():
    drone = TelloDrone()
    connected = await drone.connect()
    print(f"Drone was{' unsuccessfully' if not connected else ''} connected. Response: {connected}")

    if connected:
        battery = await drone.connection.get_battery_level()
        print(f"Battery is currently at {battery}%")

        await drone.connection.set_stream_off()
        await drone.connection.set_stream_on()

        while True:
            cv2.imshow("Tello", drone.get_capture_frame())

            if cv2.waitKey(1) == 27:
                await drone.connection.set_stream_off()
                break


if __name__ == '__main__':
    asyncio.run(main())
