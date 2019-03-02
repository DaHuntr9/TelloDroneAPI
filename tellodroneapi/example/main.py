from tellodroneapi.TelloDrone import TelloDrone
import asyncio


async def main():
    drone = TelloDrone()
    connected = await drone.connect()
    print(f"Drone was {'unsuccessfully' if not connected else ''} connected. Response: {connected}")

if __name__ == '__main__':
    asyncio.run(main())
