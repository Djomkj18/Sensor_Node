"""
References for the Temperature Sensor:
    Connections and Code -> https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/
    More code -> https://RandomNerdTutorials.com
    Sensor Datasheet -> https://cdn-shop.adafruit.com/datasheets/DS18B20.pdf

Useful Code Snippets for the Temperature Sensor:
    # Creates a ds18x20 object called temp_sensor on the sensor_pin defined earlier
    temp_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_pin))

    # Scans for the DS18B20 sensors and saves the address found... returns a list with the address
    DS18B20_address = temp_sensor.scan()
        
    # Needed everytime we want to read the temp
    temp_sensor.convert_temp() 
    time.sleep_ms(750) # Delay of 750 ms to give enough time to convert the temperature
        
    # Return the temperature in Celcius
    temp_sensor.read_temp(DS18B20_address[0]) 

"""

"""
References for the SD Card Module:
    os for controlling the filesystem -> https://docs.micropython.org/en/latest/esp8266/tutorial/filesystem.html
    sd library with micropython -> https://learn.adafruit.com/micropython-hardware-sd-cards/micropython
    file read, write, etc -> https://www.pythontutorial.net/python-basics/python-write-text-file/
    hardware connections -> https://learn.adafruit.com/micropython-hardware-sd-cards/micropython?view=all

Useful Code Snippets for the SD Card Module:
    spi = machine.SPI(1, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
    #sck in the ESP is CLK on the SD Card Module
    #mosi or Pin(13) in the ESP is DI on the SD Card Module 
    #miso or Pin(12) in the ESP is DO on the SD Card Module  
    #GPIO Pin(18) is cs on the SD Card Module
        
    # Makes an SD card object  
    sdcard = sdcard.SDCard(spi, cs)

    # Makes the SD card the new root filesystem 
    vfs = os.VfsFat(sdcard)
    os.mount(vfs, "/sd")
"""

import machine # Needed for the Pin 
import onewire # OneWire communication for the sensor
import ds18x20 # The sensor the team has
import time # Needed because the sensor ".convert_temp()" function needs "time.sleep_ms(750)" to work

import sdcard # SD card Library 
import os # Need it to control over the filesystem
import math

from machine import Timer
from machine import RTC

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
    
#[Year Month Date Weekday Hour Min Sec Micro_sec]
date_time = [2022, 3, 24, 6, 5, 50, 0, 0]
rtc = RTC() 
rtc.datetime((date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5], date_time[6], date_time[7])) 
 
tim1 = Timer(1) 
tim1.init(period=1000, mode=Timer.PERIODIC, callback=read_temp_callback)

### end

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
