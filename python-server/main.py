import asyncio
from kasa import SmartPlug

async def main():
    p = SmartPlug("192.168.10.21")
    p2 = SmartPlug("192.168.10.120")

    await p.update()  # Request the update
    await p2.update()
    print(f"{p.alias} is {p.state_information}")  # Print out the alias
    print(f"{p2.alias} is {p2.state_information}")  # Print out the alias
    await p.turn_on()
    

if __name__ == "__main__":
    asyncio.run(main())