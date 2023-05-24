from machine import Pin
from time import sleep
class Limite():
    def __init__(self):
        self.contact = Pin(22,Pin.IN)
        self.contact.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING), 
        handler=self.(actionInterruptionB)
 
def actionInterruptionB(self,pin):
    print('Contact')
db=Limite()
while True:
    pass