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
import machine
import onewire # OneWire communication for the sensor
import ds18x20 # The sensor the team has
import time # Needed because the sensor ".convert_temp()" function needs "time.sleep_ms(750)" to work
import os # Need it to control over the filesystem
import math
import sdcard
import network

from esp import espnow
from machine import RTC

global master

### Initialization and activationn of a WLAN interface to successfully send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)
### end

###Initialization the ESP32 peer-to-peer protocol
e = espnow.ESPNow()
e.init()
master = b'\x94\x3c\xc6\x6d\x17\x48' #94:3c:c6:6d:17:48'  # MAC address of peer's wifi interface
e.add_peer(master)
### end

### Initialization of the temperature sensor 
sensor_pin = machine.Pin(5)
temp_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_pin)) 

DS18B20_address = temp_sensor.scan()
### end

### Initialization of the SD Card
spi = machine.SPI(1, sck = machine.Pin(14), mosi = machine.Pin(13), miso = machine.Pin(12))
cs = machine.Pin(18)
sdcard = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sdcard)
os.mount(vfs, "/sd")

raw_data_file_name =  "/sd/raw_temp_data.txt"
temp_data_file_name = "/sd/temp_data.txt"
time_sample_file_name = "/sd/time_sample.txt"

with open(temp_data_file_name, "a") as f:
    f.write('Temperature vs Time(sec):'+'\n')
    f.close()
    
with open(time_sample_file_name, "a") as f:
    f.write('Time and Date the data was taken:'+'\n')
    f.close()
### end
    
#Intializing RTC
rtc = RTC()
###end


"""Description: 
    Funtion records temperature sensor data at the frequency of the hardware timer
Parameters:
    Time unit t
Returns:
    N/A
Throws:
    N/A
"""
def read_temp_callback(t):

    flag = 0
    line_count = 0
    print(index)
    with open(raw_data_file_name, "a") as f:
        f.write(str( temp_sensor.read_temp(DS18B20_address[0]) ) + '\n')
            
        f.close()
        
    with open(raw_data_file_name, "r") as f:
        for line in f:
            line_count += 1        
            if line_count == 30: # Signal if we have 30 seconds worth of data
                flag = 1
                line_count = 0
            
        f.close()
        
    time_sample()
    
    if flag == 1: # Need a flag because we need to f.close() before filtering data
        temp = filter_the_data() # Filter 30 seconds worth of data
        flag = 0
        temperature_send(temp)

    temp_sensor.convert_temp() # Needed when we take a sample every sec
    
    return


"""Description: 
    Function prints the current date and time
Parameters:
    None
Returns:
    N/A
Throws:
    N/A
"""
def time_sample(): 
    
    _date = list( rtc.datetime() )[0:4] # _date[0] = year + _date[1] = Month + _date[2] = Day
    _time = list( rtc.datetime() )[4:7] # _time[0] = hour + _time[1] = minute + _time[2] = second
    
    today = weekday(_date[3])
    
    date = str(today) + ' ' + str(_date[1]) + '/' + str(_date[2]) + '/' + str(_date[0])
    time = str(_time[0]) + ':' + str(_time[1]) + ':' + str(_time[2]) 

    with open(time_sample_file_name, "a") as f:
        f.write( time + '  |  ' + date + '\n')
        f.close()
    
    return

"""Description: 
    N/A
Parameters:
    N/A
Returns:
    N/A
Throws:
    N/A
"""
def median_filter(_data, filter_size):
    temp = []
    indexer = filter_size // 2
    for i in range(len(_data)):
        for z in range(filter_size):
            if i + z - indexer < 0 or i + z - indexer > len(_data) - 1:
                for c in range(filter_size):
                    temp.append(0)
            else:
                for k in range(filter_size):
                    temp.append(_data[i + z - indexer])

        temp.sort()
        _data[i] = temp[len(temp) // 2]
        temp = []
    return _data

"""Description: 
    N/A
Parameters:
    N/A
Returns:
    N/A
Throws:
    N/A
"""
def filter_the_data():
    
    # Gather the temperature sensor data | 30 samples 
    raw_data = []
    with open(raw_data_file_name, "r") as f:
        for line in f:
            raw_data.append(float(line))
        f.close()
    
    # Filter the data
    filtered_data = median_filter(raw_data, 7)
    
    # Save filtered data 
    with open(temp_data_file_name, "a") as f:
        temp = 0
        for number in filtered_data:
            temp += number
            f.write(str(number)+'\n')
        f.close()
        temp = temp/30
    print(temp)
    # Errase the raw data file
    os.remove(raw_data_file_name)
  
    return temp


"""Description: 
    Funtion prints the current day on the basis of the rtc.datetime() index value 
Parameters:
    Index representing the day of the week
Returns:
    A string telling the day of the week
Throws:
    N/A
Example:
    "weekday(3)" gives day = "Thursday"
"""
def weekday(day):  #Print the current day on the basis of the rtc.datetime() index value
    
    if day == 0:
        tday = "Monday" 
    elif day == 1:
        tday = "Tuesday"  
    elif day == 2:
        tday = "Wednesday"   
    elif day == 3:
        tday = "Thursday"   
    elif day == 4:
        tday = "Friday"  
    elif day == 5:
        tday = "Saturday" 
    elif day == 6:
        tday = "Sunday"
    
    return tday
  
  
"""
Description: 
    Funtion sends the temperature read by the sensor to the main processor.
    If the data was not received then the function keeps trying until the meesage was received.
Parameters:
    Value of temperature in Celsius
Returns:
    No Return  
Throws:
    N/A
Example:
    "temperature_send(23.625)" gives 23.625
"""
def temperature_send(temp_node):
    
    acknowledgement = False
    
    while acknowledgement == False:
        acknowledgement = e.send(master, str(int(temp_node * 10000)), True)
    
    return