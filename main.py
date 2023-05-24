# Importation des modules nécessaires
from machine import Pin
import time
try:
    import usocket as socket
except:
    import socket

# Importation d'une fonction depuis le module "configwifi" pour se connecter au Wi-Fi
from configwifi import connect

#Connexion au Wi-Fi
connect()

# Classe utilisée pour contrôler un capteur PIR
class Pir():
    def __init__(self):
        # Initialisation du pin du capteur PIR
        self.pin = Pin(22, Pin.IN)
        self.mvt = 0
        # Configuration du capteur
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING) ,
            handler=self.actionInterruption)
    def actionInterruption(self,pin):
        pir = ""
        # Gestion de l'interruption déclenchée par le capteur PIR
        if (pin.value()==1):
            pir = "presence"
            print(pin.value())
            lcd.println("presence", color=lcd.CYAN)
        else:
            pir = "personne"
            lcd.println("personne", color=lcd.PURPLE)
            
        # Création d'un socket et connection au serveur
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.116.227', 65000))
            
        # Envoi de l'état du capteur PIR au socket
        s.send(str(pir))
            
        # Fermeture de la connexion du socket
        s.close()
    
# Création d'une instance de la classe Pir pour contrôler le capteur PIR
c = Pir()

while True:
    # Attente de 1 seconde entre chaque mesure
    time.sleep(5)