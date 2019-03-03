from tellodroneapi.TelloDrone import TelloDrone
import asyncio


async def main():
    drone = TelloDrone()
    connected = await drone.connect()
    print(f"Drone was {'unsuccessfully' if not connected else ''} connected. Response: {connected}")

    if connected:
        battery = await drone.send_command_and_await("battery?")
        print(f"Battery is currently at {battery}%")

if __name__ == '__main__':
    asyncio.run(main())
