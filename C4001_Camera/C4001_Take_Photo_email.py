import smbus2

import time
from picamera2 import Picamera2, Preview
import time

import smtplib
from email.message import EmailMessage

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


# Email settings
from_email_addr = ""
from_email_pass = ""   # Gmail App Password
to_email_addr = ""

# File to save readings
file_name = "env_readings.txt"

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
        filename = f"/home/kiran/C4001/Capture_{capture_count}_{timestamp}.jpg"
        picam2.capture_file(filename)
        capture_count += 1
        print("Photo Captured >> ", filename)
        print("\n")

        # Create email
        msg = EmailMessage()
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        msg['Subject'] = 'Captured Image'
        msg.set_content("Hi,\n\nPlease find attached the latest captured photo.\n")

         # Attach the image (instead of txt file)
        with open(filename, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="image",
                subtype="jpeg",
                filename=filename
            )

        # Send email
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email_addr, from_email_pass)
            server.send_message(msg)
            print("Email with photo attachment sent!")
        except Exception as e:
            print("Error sending email:", e)
        finally:
            server.quit()
            
    time.sleep(1)
    