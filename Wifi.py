import network
import time
from m5stack import lcd
from machine import Pin
try:
  import usocket as socket
except:
  import socket

# Constantes pour les types d'authentification

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

# Constantes pour les types d'authentification

SSID = "jiyanbaran"
PASSWORD = "amed20012001"

def do_connect(ssid,psw):
    
    # Initialise l'interface WLAN en mode STA (station/client)
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Obtient l'adresse MAC du dispositif
    
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
    print("Local MAC:"+mac) # Obtient l'adresse MAC locale 
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('connexion au reseau...' + ssid)
        
        # Connecte le dispositif au réseau Wi-Fi spécifié
        
        wlan.connect(ssid, psw)
     
     # Obtient le compteur en millisecondes

    start = time.ticks_ms() # Attend pendant 1 seconde
    while not wlan.isconnected():
        time.sleep(1)# Attend pendant 1 seconde
        if time.ticks_ms()-start > 50000:
            print("Timeout de connexion!")
            break
 
    if wlan.isconnected():
        print('Adresses IP:', wlan.ifconfig())
    return wlan
 
def connect():
    
    # Appelle la fonction `do_connect` avec les paramètres SSID et mot de passe
    
    do_connect(SSID, PASSWORD)