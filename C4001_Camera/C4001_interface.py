import smbus2

import time
from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

# RPi I2C bus
bus = smbus2.SMBus(1)

# Replace with your detected address (e.g. 0x50)
DEVICE_ADDR = 0x2a
capture_count = 0  # counter for filenames

picam2.start_preview(Preview.QTGL)
print("Started preview")
picam2.start()

while True:
    
    objects = bus.read_byte_data(DEVICE_ADDR, 0x10)
    print("Number of Objects:", objects)

    data_l = bus.read_byte_data(DEVICE_ADDR, 0x11)
    data_h = bus.read_byte_data(DEVICE_ADDR, 0x12)
    object_range = (data_h * 256) + data_l
    print("Object Range:", object_range)

    data_l = bus.read_byte_data(DEVICE_ADDR, 0x13)
    data_h = bus.read_byte_data(DEVICE_ADDR, 0x14)
    speed =(data_h * 256) + data_l
    print("Speed:", speed)

    data_l = bus.read_byte_data(DEVICE_ADDR, 0x15)
    data_h = bus.read_byte_data(DEVICE_ADDR, 0x16)
    energy =(data_h * 256) + data_l
    print("Energy:", energy)
    print("\n")
    
    if objects > 0:
        
        time.sleep(0.3)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"Capture_{capture_count}_{timestamp}.jpg"
        picam2.capture_file(filename)
#        picam2.stop_preview()
        capture_count +=1
        print("Ptoto Captured")
        
    time.sleep(2)
    
# Example: write to register 0x01
#bus.write_byte_data(DEVICE_ADDR, 0x01, 0xFF)

#for reg in range(0x00, 0x20):
#    val = bus.read_byte_data(DEVICE_ADDR, reg)
#    print(f"Reg 0x{reg:02X} = {val}")
