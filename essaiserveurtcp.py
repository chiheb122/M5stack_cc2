import machine
from machine import I2C, Pin
import time
from m5stack import lcd

try:
    import usocket as socket
except:
    import socket

from configwifi import connect




connect()

class SHT30:
    def __init__(self, scl_pin=22, sda_pin=21, i2c_address=0x44):
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.i2c_addr = i2c_address
        time.sleep_ms(50)

    def measure(self):
        self.i2c.writeto(self.i2c_addr, b'\x2C\x06')
        time.sleep_ms(20)
        data = self.i2c.readfrom(self.i2c_addr, 6)
        temp = (((data[0] << 8) | data[1]) * 175 / 65535) - 45
        humi = (((data[3] << 8) | data[4]) * 100 / 65535)
        return temp, humi


c = SHT30()

lcd.clear()
while True:
    temp, humi = c.measure()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.116.227', 65000))

    lcd.setCursor(0, 100)
    lcd.println("La temperature est de " + str(temp), color=lcd.YELLOW)
    lcd.println("L'humidite est de " + str(humi), color=lcd.YELLOW)

    s.send(("Temperature: " + str(temp) + "\nHumidite: " + str(humi)).encode())

    s.close()

    time.sleep(60)
