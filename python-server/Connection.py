from tplinkcloud import TPLinkDeviceManager
import asyncio
import json
import time

username='kasa@luciochen.com'
password='Kasa!990412'

device_manager = TPLinkDeviceManager(username, password)
device_name1 = "HS103-1"
device_name2 = "HS103-2"
##View Full Info Devices
async def fetch_all_devices_sys_info():
  devices = await device_manager.get_devices()
  fetch_tasks = []
  for device in devices:
    async def get_info(device):
      print(f'Found {device.model_type.name} device: {device.get_alias()}')
      print("SYS INFO")
      print(json.dumps(device.device_info, indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None))
      print(json.dumps(await device.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None))
    fetch_tasks.append(get_info(device))
  await asyncio.gather(*fetch_tasks)

##View Brief info Devices
async def view_device():
    devices = await device_manager.get_devices()
    if devices:
        print(f'Found {len(devices)} devices')
    for device in devices:
        print(f'{device.model_type.name} device called {device.get_alias()}')


######State of Plugs######
async def tapeState():
    device_name = device_name1
    device = await device_manager.find_device(device_name)
    if device:
        my_dict = json.dumps(await device.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None)
        my_dict = json.loads(my_dict)
        print(my_dict['relay_state'])
    else:  
        print(f'Could not find {device_name}')

async def noTapeState():
    device_name = device_name2
    device = await device_manager.find_device(device_name)
    if device:
        my_dict = json.dumps(await device.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None)
        my_dict = json.loads(my_dict)
        print(my_dict['relay_state'])
    else:  
        print(f'Could not find {device_name}')

##########Tape Plug#######
#Toggle 
async def toggleTape():
    device_name = device_name1
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Toggling {device_name}')
        await device.toggle()
    else:  
        print(f'Could not find {device_name}')

#Turn on 
async def TurnOnTape():
    device_name = device_name1
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Turning On {device_name}')
        await device.power_on()
    else:  
        print(f'Could not find {device_name}')
#Turn off
async def TurnOffTape():
    device_name = device_name2
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Turning Off {device_name}')
        await device.power_off()
    else:  
        print(f'Could not find {device_name}')

###################No tape Plug##############
#Toggle 
async def toggleNoTape():
    device_name = device_name2
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Toggling {device_name}')
        await device.toggle()
    else:  
        print(f'Could not find {device_name}')

#Turn on 
async def TurnOnNoTape():
    device_name = device_name2
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Turning On {device_name}')
        await device.power_on()
    else:  
        print(f'Could not find {device_name}')
#Turn off
async def TurnOffNoTape():
    device_name = device_name2
    device = await device_manager.find_device(device_name)
    if device:
        #print(f'Found {device.model_type.name} device: {device.get_alias()}')
        print(f'Turning Off {device_name}')
        await device.power_off()
    else:  
        print(f'Could not find {device_name}')

################Both##################
contains_name = 'HS103'
#Toggle Both
async def toggleBoth():
    devices = await device_manager.find_devices(contains_name)
    if devices:
        print("Toggle Both")
        for device in devices:
           await device.toggle() 
    else:  
        print(f'Could not find {contains_name}')
async def turnOnBoth():
    devices = await device_manager.find_devices(contains_name)
    if devices:
        print("Turn On Both")
        for device in devices:
           await device.power_on() 
    else:  
        print(f'Could not find {contains_name}')

async def turnOffBoth():
    devices = await device_manager.find_devices(contains_name)
    if devices:
        print("Turn Off Both")
        for device in devices:
           await device.power_off() 
    else:  
        print(f'Could not find {contains_name}')
#asyncio.run(view_device())
asyncio.run(tapeState())
asyncio.run(noTapeState())
# #asyncio.run(fetch_all_devices_sys_info())

# asyncio.run(TurnOnTape())
# time.sleep(1)
# asyncio.run(TurnOffTape())
# time.sleep(1)

# asyncio.run(TurnOnNoTape())
# time.sleep(1)
# asyncio.run(TurnOffNoTape())
# time.sleep(1)

# asyncio.run(turnOnBoth())
# time.sleep(1)
# asyncio.run(turnOffBoth())
# time.sleep(1)
# asyncio.run(toggleBoth())
# time.sleep(1)
# asyncio.run(toggleBoth())
# time.sleep(1)




#asyncio.run(fetch_all_devices_sys_info())



