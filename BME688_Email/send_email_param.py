import bme680
import time

import smtplib
from email.message import EmailMessage


# Initialize the sensor
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Configure the sensor
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

#Set the sender email and password and recipient emaiç
from_email_addr =""
from_email_pass =""
#from_email_addr ="shingote_k@yahoo.com"
to_email_addr =""

while True:
    # Read and display data
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        pressure = sensor.data.pressure
        humidity = sensor.data.humidity
        gas_resistance = sensor.data.gas_resistance

        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Gas Resistance: {gas_resistance:.2f} O\n")
        time.sleep(5)

        # Create a message object
        msg = EmailMessage()

        # Build email body with sensor data
        body = f"""
        Weather Report from Raspberry Pi:

        1. Temperature: {temperature:.2f} °C
        2. Pressure: {pressure:.2f} hPa
        3. Humidity: {humidity:.2f} %
        4. Gas Resistance: {gas_resistance:.2f} O
        """
        msg.set_content(body)

        # Set sender and recipient
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr

        # Set your email subject
        msg['Subject'] = 'Weather Parameters'

        # Connecting to server and sending email
        # Edit the following line with your provider's SMTP server details
        server = smtplib.SMTP('smtp.gmail.com', 587)

        # Comment out the next line if your email provider doesn't use TLS
        server.starttls()
        # Login to the SMTP server
        server.login(from_email_addr, from_email_pass)

        # Send the message
        server.send_message(msg)

        print('Email sent')

        #Disconnect from the Server
        server.quit()

