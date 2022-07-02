import sys
import socket
import selectors
import types
from tplinkcloud import TPLinkDeviceManager
import asyncio
import json
import time
import os
import threading

username='kasa@luciochen.com'
os.environ['KASA_PASSWORD']="Kasa!990412"
password=os.getenv('KASA_PASSWORD')

device_manager = TPLinkDeviceManager(username, password)
device_name1 = "HS103-1"
device_name2 = "HS103-2"

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10001  # Port to listen on (non-privileged ports are > 1023)

lamp1 = False
future_lamp1 = False
kasa_lamp1 = 0

lamp2 = False
future_lamp2 = False
kasa_lamp2 = 0

running = True

async def get_device():
    global kasa_lamp1
    global kasa_lamp2

    kasa_lamp1 = await device_manager.find_device(device_name1)
    kasa_lamp2 = await device_manager.find_device(device_name2)


async def lampState():
    global lamp1
    global lamp2
    global future_lamp1
    global future_lamp2
    global kasa_lamp1
    global kasa_lamp2

    if kasa_lamp1:
        if future_lamp1 != lamp1:
            if future_lamp1:
                await kasa_lamp1.power_on()
            else:
                await kasa_lamp1.power_off()

        my_dict = json.dumps(await kasa_lamp1.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None)
        my_dict = json.loads(my_dict)
        print(my_dict['relay_state'])
        lamp1 = my_dict['relay_state']
        future_lamp1 = lamp1
    else:  
        print(f'Could not find {device_name1}')
    
    if kasa_lamp2:
        if future_lamp2 != lamp2:
            if future_lamp2:
                await kasa_lamp2.power_on()
            else:
                await kasa_lamp2.power_off()
        my_dict = json.dumps(await kasa_lamp2.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None)
        my_dict = json.loads(my_dict)
        print(my_dict['relay_state'])
        lamp2 = my_dict['relay_state']
        future_lamp2 = lamp2
    else:  
        print(f'Could not find {device_name2}')

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    global lamp1 
    global lamp2
    global future_lamp1
    global future_lamp2
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            chunks = str(recv_data)
            if 'lamp1:on' in chunks:
                future_lamp1 = True
                data.outb += str.encode('lamp1:on ')
            elif 'lamp1:off' in chunks:
                future_lamp1 = False
                data.outb += str.encode('lamp1:off ')
            elif 'lamp1:state' in chunks:
                if lamp1:
                    data.outb += str.encode('lamp1:on ')
                else:
                    data.outb += str.encode('lamp1:off ')
            if 'lamp2:on' in chunks:
                future_lamp2 = True
                data.outb += str.encode('lamp2:on ')
            elif 'lamp2:off' in chunks:
                future_lamp2 = False 
                data.outb += str.encode('lamp2:off ')
            elif 'lamp2:state' in chunks:
                if lamp2:
                    data.outb += str.encode('lamp2:on ')
                else:
                    data.outb += str.encode('lamp2:off ')
            if data.outb:
                data.outb += str.encode('\n')

            ##data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
 
        # helper function to execute the threads
    def run(self):
        asyncio.run(get_device())
        while True:
            asyncio.run(lampState())
            time.sleep(5)
            if not running:
                break

        #print(str(self.thread_name) +" "+ str(self.thread_ID))
            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    s.setblocking(False)
    sel.register(s,selectors.EVENT_READ,data=None)
    thread1 = thread("lamp_update",1000)
    thread1.start()
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
        s.close()
        running = False