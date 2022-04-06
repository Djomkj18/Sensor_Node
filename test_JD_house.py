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

with open("/sd/temp_data_1.txt", "a") as f:
    f.write('Temperature vs Time(sec):'+'\n')
    f.close()
    
with open("/sd/time_sample_1.txt", "a") as f:
    f.write('Time and Date the data was taken:'+'\n')
    f.close()
### end
    

### Timer Interrupts - records temperature sensor data every second
def read_temp_callback(t):
    #temp_sensor.convert_temp() # Needed when we take a sample every minute
    #time.sleep_ms(750) # Needed when we take a sample every minute
    
    with open("/sd/temp_data_1.txt", "a") as f:
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
    
    with open("/sd/time_sample_1.txt", "a") as f:
        f.write( time + ' | ' + date + '\n') 
        f.close()
    
#[Year Month Date Weekday Hour Min Sec Micro_sec]
date_time = [2022, 3, 24, 6, 5, 50, 0, 0]
rtc = RTC() 
rtc.datetime((date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5], date_time[6], date_time[7])) 
 
tim1 = Timer(1) 
tim1.init(period=1000, mode=Timer.PERIODIC, callback=read_temp_callback)

### end