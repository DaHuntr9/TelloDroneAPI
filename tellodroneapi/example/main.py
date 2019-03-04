from tellodroneapi.TelloDrone import TelloDrone
import asyncio


async def main():
    drone = TelloDrone()
    connected = await drone.connect()
    print(f"Drone was{' unsuccessfully' if not connected else ''} connected. Response: {connected}")

    if connected:
        battery = await drone.connection.get_battery_level()
        temp = await drone.connection.get_temperature()
        print(f"Battery is currently at {battery}% and temperature is {temp} C")

        if input("Enter 'ok' to attempt takeoff and land: ") == 'ok':
            print("Attempting takeoff...")
            takeoff = await drone.control.takeoff()
            print(takeoff)

            await asyncio.sleep(10)

            print("Attempting landing")
            landed = await drone.control.land()
            print(landed)
        else:
            print("Takeoff and landing test skipped.")

        user_input = input('Live command mode active. Enter a command to run. Enter exit to end: ')
        while user_input != 'exit':
            user_input = input("> ")
            response = await drone.send_command_and_await(user_input)
            print(response)
        else:
            print("Live command mode ended")

if __name__ == '__main__':
    asyncio.run(main())
