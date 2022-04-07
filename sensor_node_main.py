from sensor_node import *
from machine import Timer


while True:
    
    temp_node = temperature_sensors_data()
    temperature_send(temp_node)
    
    
#Hardware Timer 1
tim1 = Timer(1)
tim1.init(period = 1000, mode = Timer.PERIODIC, callback = read_temp_callback)
### end

    
    
