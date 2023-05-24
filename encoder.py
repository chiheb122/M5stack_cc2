from machine import I2C, Pin
import time
class Encoder:
     ENCODER_REG=16
     BUTTON_REG=32
     RGB_LED_REG=48
     def __init__(self, scl_pin=22, sda_pin=21, i2c_address=0x40):
         self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
         self.i2c_addr = i2c_address
         time.sleep_ms(50)
     def getButtonStatus(self):
         #data=self.i2c.readfrom_mem(self.i2c_addr,'\x20',1)
         data=self.i2c.readfrom_mem(self.i2c_addr,self.BUTTON_REG,1)
         return data

     def getPosition(self):
         data=self.i2c.readfrom_mem(self.i2c_addr,self.ENCODER_REG,2)
         return int.from_bytes(data,'big')
        
     def setLEDColor(self,idx,r,v,b):
         data=bytes([idx, r, v, b])
         self.i2c.writeto_mem(self.i2c_addr,self.RGB_LED_REG,data)
         





