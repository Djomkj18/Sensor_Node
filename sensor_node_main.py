from sensor_node import *
from machine import Timer

    
### Hardware Timer 1 | This is a 1 second timer
# Everytime the timer fires the ESP takes a temperature sample
tim1 = Timer(1)
tim1.init(period = 1000, mode = Timer.PERIODIC, callback = read_temp_callback)
### end

while True:
    temp_node = temperature_sensors_data()
    temperature_send(temp_node)

    
    

    
    
