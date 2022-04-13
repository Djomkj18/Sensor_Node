from sensor_node_4_5_6 import *
from machine import Timer


### Hardware Timer 1 | This is a 1 second timer
# Everytime the timer fires the ESP takes a temperature sample
tim1 = Timer(1)
tim1.init(period = 1000, mode = Timer.PERIODIC, callback = read_temp_callback)
### end
    
    

    
    
