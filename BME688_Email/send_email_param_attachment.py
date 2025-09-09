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

# Email settings
from_email_addr = ""
from_email_pass = ""   # Gmail App Password
to_email_addr = ""

# File to save readings
file_name = "env_readings.txt"

while True:
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        pressure = sensor.data.pressure
        humidity = sensor.data.humidity
        gas_resistance = sensor.data.gas_resistance

        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Gas Resistance: {gas_resistance:.2f} Ω\n")
        time.sleep(5)

        # Write/Append to file
        with open(file_name, "a") as f:
            f.write(
                f"Temperature: {temperature:.2f} °C | "
                f"Pressure: {pressure:.2f} hPa | "
                f"Humidity: {humidity:.2f} % | "
                f"Gas Resistance: {gas_resistance:.2f} Ω\n"
            )

        # Create email
        msg = EmailMessage()
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        msg['Subject'] = 'Weather Parameters'
        msg.set_content("Hi,\n\nPlease find attached the latest environment readings from Raspberry Pi.\n")

        # Attach file (correct way with EmailMessage)
        with open(file_name, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=file_name
            )

        # Send email
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email_addr, from_email_pass)
            server.send_message(msg)
            print("Email with attachment sent!")
        except Exception as e:
            print("Error sending email:", e)
        finally:
            server.quit()