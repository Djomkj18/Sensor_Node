from temperature_node_2 import *
from machine import Timer
import network
from esp import espnow

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)

e = espnow.ESPNow()
e.init()
master = b'\x94\x3c\xc6\x6d\x17\x48' #94:3c:c6:6d:17:48'  # MAC address of peer's wifi interface
e.add_peer(master)

e.send("Starting data transmition...")       # Send to all peers

while True:
    
    temp_node_1 = temperature_sensors_data()
    temp_to_fahrenheit = cel_to_fah(temp_node_1)
    print(temp_to_fahrenheit)
    e.send(master, str(temp_to_fahrenheit), True)
    time.sleep(1)
