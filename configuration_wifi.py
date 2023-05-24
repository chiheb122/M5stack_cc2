
import network
import time
from m5stack import lcd
from machine import Pin
try:
  import usocket as socket
except:
  import socket


AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = "Ukkle"
PASSWORD = "classclass"

 
def do_connect(ssid,psw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
    print("Local MAC:"+mac) #get mac 
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('connexion au reseau...' + ssid)
        wlan.connect(ssid, psw)
 
    start = time.ticks_ms() # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1) # sleep for 1 second
        if time.ticks_ms()-start > 50000:
            print("Timeout de connexion!")
            break
 
    if wlan.isconnected():
        print('Adresses IP:', wlan.ifconfig())
    return wlan
 
def connect():
 do_connect(SSID,PASSWORD)
 lcd.println("Configuration de connexion :", color = lcd.YELLOW)

 









