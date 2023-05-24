# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import machine
sys.path[1] = '/flash/lib'
from m5stack import lcd, speaker, buttonA, buttonB, buttonC

# ---------- M5Cloud ------------
def eteindre() :
    machine.deepsleep
    
if True:
    if buttonB.isPressed():
        import wifisetup
        import m5cloud
    elif buttonA.isPressed():
        eteindre()
    #else:
        #lcd.println('On: OFF-LINE Mode (CHIBA)', color = lcd.YELLOW)
        #lcd.setColor(lcd.YELLOW)
    else:
        lcd.clear()
        lcd.font(lcd.FONT_DejaVu18)
        lcd.println('BONJOUR',lcd.CENTER, 120,color = lcd.YELLOW)
        lcd.setColor(lcd.YELLOW)
        


    
buttonC.wasPressed(eteindre)