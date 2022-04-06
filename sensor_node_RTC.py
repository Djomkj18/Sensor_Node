import network
import machine # Needed for the Pin 
import onewire # OneWire communication for the sensor
import ds18x20 # The sensor the team has
import time # Needed because the sensor ".convert_temp()" function needs "time.sleep_ms(750)" to work
import sdcard # SD card Library 
import os # Need it to control over the filesystem
import math

from machine import RTC
from machine import Timer
from esp import espnow


### Initialization of the temperature sensor 
sensor_pin = machine.Pin(5)
temp_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_pin)) 

DS18B20_address = temp_sensor.scan()
### end


### Initialization of the SD Card
spi = machine.SPI(1, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
cs = machine.Pin(18)
sdcard = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sdcard)
os.mount(vfs, "/sd")

temp_data_file_name = "/sd/temp_data_1.txt"
time_sample_file_name = "/sd/time_sample_1.txt"

with open(temp_data_file_name, "a") as f:
    f.write('Temperature vs Time(sec):'+'\n')
    f.close()
    
with open(time_sample_file_name, "a") as f:
    f.write('Time and Date the data was taken:'+'\n')
    f.close()
### end
    
    
### Timer Interrupts - records temperature sensor data every second

"""
Description: 
    A
Parameters:
    A
Returns:
    A 
Throws:
    A
Example:
    A
"""
def read_temp_callback(t):
    #temp_sensor.convert_temp() # Needed when we take a sample every minute
    #time.sleep_ms(750) # Needed when we take a sample every minute
    temp_node_1 = temperature_sensors_data()
    temp_to_fahrenheit = cel_to_fah(temp_node_1)
    print(temp_to_fahrenheit)
    
    e.send(master, str(temp_to_fahrenheit), True)
    time.sleep(1)
    
    with open(temp_data_file_name, "a") as f:
        f.write(str( temp_sensor.read_temp(DS18B20_address[0]) ) + ' , '+ str(list( rtc.datetime() )[6]) + '\n')
        #f.write(str( temp_sensor.read_temp(DS18B20_address[0]) ) + ' , '+ str(list( rtc.datetime() )[5]) + '\n') # Needed when we take a sample every minute
        f.close()        
    time_sample()

    temp_sensor.convert_temp() # Needed when we take a sample every sec
    return


def time_sample(): # Print the current date and time
    _date = list( rtc.datetime() )[0:4] # _date[0] = year + _date[1] = Month + _date[2] = Day
    _time = list( rtc.datetime() )[4:7] # _time[0] = hour + _time[1] = minute + _time[2] = second

    date = 'Sunday ' + str(_date[1]) + '/' + str(_date[2]) + '/' + str(_date[0])
    time = str(_time[0]) + ':' + str(_time[1]) + ' & ' + str(_time[2]) + ' seconds'

    with open(time_sample_file_name, "a") as f:
        f.write( time + ' | ' + date + '\n') 
        f.close()
    
    return

"""
Description: 
    Funtion reads the temperature from the DS18B20 sensor 
Parameters:
    None
Returns:
    A float representing the temperature the sensor read 
Throws:
    N/A
Example:
    "temp_node_1 = temperature_sensors_data()" makes temp_node_1 = 23.625
"""

def temperature_sensors_data(): 
    temp_sensor.convert_temp() 
    time.sleep_ms(750)

    return temp_sensor.read_temp(DS18B20_address[0])

"""
Description: 
    A
Parameters:
    A
Returns:
    A 
Throws:
    A
Example:
    A
"""

def cel_to_fah(tc):
    tf = (9/5) * tc + 32
    tfs = str("%.2f" % tf)
    t1 = int(tfs[3])
    t2 = int(tfs[4])
    if (t1 >= 7 and t2 >= 5):
        tf = math.ceil(tf)
    else:
        tf = math.floor(tf)
    return tf


# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)

e = espnow.ESPNow()
e.init()
master = b'\x94\x3c\xc6\x6d\x17\x48' #94:3c:c6:6d:17:48'  # MAC address of peer's wifi interface
e.add_peer(master)

e.send("Starting data transmition...")       # Send to all peers


#[Year Month Date Weekday Hour Min Sec Micro_sec]
date_time=[0,0,0,0,0,0,0,0]
print("Enter current date and time:")
date_time[0] = int(input("Year? "))
date_time[1] = int(input("Month? "))
date_time[2] = int(input("Day? "))
date_time[3] = int(input("Weekday? "))
date_time[4] = int(input("Hour? "))
date_time[5] = int(input("Minute? "))
date_time[6] = int(input("Second? "))
date_time[7] = int(input("Microsecond? "))
print("")
#date_time = [2022, 3, 24, 6, 5, 50, 0, 0]
rtc = RTC() 
rtc.datetime((date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5], date_time[6], date_time[7])) 

#Hardware Timer 1
tim1 = Timer(1)
tim1.init(period = 1000, mode = Timer.PERIODIC, callback = read_temp_callback)

### end


