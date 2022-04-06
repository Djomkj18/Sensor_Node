# Sensor_Nodes
Handles the temperature sensor, the SIM card, and the data transmission to the central ESP processor 

### boot.py File!! ###
If the board is bussy when you power it with the computer: 
    
    Press Ctrl-C 
    -> https://techexplorations.com/guides/esp32/micropython-with-the-esp32/16-how-to-run-a-program-at-boot/

### TEMPERATURE SENSOR ###
References for the Temperature Sensor:

    Connections and Code 
    -> https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/
    
    More code 
    -> https://RandomNerdTutorials.com
    
    Sensor Datasheet 
    -> https://cdn-shop.adafruit.com/datasheets/DS18B20.pdf

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

### SD CARD ###
References for the SD Card Module:

    os for controlling the filesystem ->
    https://docs.micropython.org/en/latest/esp8266/tutorial/filesystem.html
    
    sd library with micropython ->
    https://learn.adafruit.com/micropython-hardware-sd-cards/micropython
    
    file read, write, etc ->
    https://www.pythontutorial.net/python-basics/python-write-text-file/
    
    hardware connections ->
    https://learn.adafruit.com/micropython-hardware-sd-cards/micropython?view=all

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
