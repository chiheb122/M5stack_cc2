import machine
from machine import I2C, Pin
import time
from m5stack import lcd

try:
    import usocket as socket
except:
    import socket

from configwifi import connect


# Connecte le dispositif à un réseau Wi-Fi

connect()

# Classe SHT30 pour mesurer la température et l'humidité

class SHT30:
    def __init__(self, scl_pin=22, sda_pin=21, i2c_address=0x44):
        
    # Initialise l'interface I2C avec les broches SCL et SDA spécifiées
        
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.i2c_addr = i2c_address
        time.sleep_ms(50)

    # Envoie la commande de mesure à SHT30

    def measure(self):
        self.i2c.writeto(self.i2c_addr, b'\x2C\x06')
        time.sleep_ms(20)
        
        # Lit les données de température et d'humidité retournées par SHT30
        
        data = self.i2c.readfrom(self.i2c_addr, 6)
        temp = (((data[0] << 8) | data[1]) * 175 / 65535) - 45
        humi = (((data[3] << 8) | data[4]) * 100 / 65535)
        return temp, humi

# Crée une instance de la classe SHT30

c = SHT30()

# Efface l'écran LCD avec un fond blanc

lcd.clear(lcd.WHITE)

while True:
    
    # Mesure la température et l'humidité avec SHT30
    
    temp, humi = c.measure()
    
    # Crée un socket TCP/IP
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Établit la connexion avec l'adresse IP et le port spécifiés
    
    s.connect(('192.168.76.227',80))
    
    # Affiche une image sur l'écran LCD
    
    lcd.image(100, 0, file="ccc.jpg", scale=2, type=lcd.JPG)

    # Affiche le titre sur l'écran LCD

    lcd.setCursor(0, 150)
    lcd.font(lcd.FONT_DejaVu18)    
    lcd.println("HEG STATION METEO", color=lcd.PINK)

    # Affiche le titre sur l'écran LCD

    lcd.println("La temperature est de :" + str(temp).split('.')[0]+ " °C", color=lcd.YELLOW)
    
    # Affiche le titre sur l'écran LCD
    
    lcd.println("L'humidite est de : " + str(humi).split('.')[0]+" %", color=lcd.YELLOW)

    # Envoie la température et l'humidité via le socket

    s.send(("Temperature "+" " +str(temp) +" "+"humidite"+" "+ str(humi)).encode())
    
    # Ferme la connexion du socket
    
    s.close()

    # Attend 60 secondes avant la prochaine mesure

    time.sleep(60)