from machine import Pin
from m5stack import lcd, speaker, buttonA, buttonB, buttonC
from configuration_wifi import connect
from encoder import Encoder
import network
import time
import select
try:
  import usocket as socket
except:
  import socket
from SubMQTTt import connectmqtt

"""
    Génère une page web avec les données de capteurs actuelles pour affichage sur le navigateur.
    Retourne une chaîne de caractères contenant le code HTML de la page.
"""
def web_page():    
    # Récupérer la position de l'encodeur
    position1 = str(position)
    temperature = temp
    humidite = hum
    # Récupérer la date et l'heure courante
    current_time = time.localtime()
    datetime_str = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    html = """
    <html>
      <head>
        <meta charset="utf-8">
        <title>HEG Station Méteo</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
          }}
          table {{
            border-collapse: collapse;
            margin: 50px auto;
            width: 80%;
            max-width: 800px;
          }}
          th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
          }}
          th {{
            background-color: #ddd;
          }}
        </style>
      </head>
      <body>
        <h1>HEG Méteo</h1>
        <table>
          <thead>
            <tr>
              <th>Nom du capteur</th>
              <th>Valeur</th>
              <th>Date et heure</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Capteur de température</td>
              <td>{}°C</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>Capteur d'humidité</td>
              <td>{}%</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>Direction du vent</td>
              <td>{} degrés</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>Vitesse du vent</td>
              <td>{} m/s</td>
              <td>{}</td>
            </tr>
          </tbody>
        </table>
         <table>
          <thead>
            <tr>
              <th>{}</th>
            </tr>
          </thead>
          </table>
      </body>
    </html>""".format(temperature,datetime_str,humidite,datetime_str,direction_vent,datetime_str,position,datetime_str,presence)
    
    return html 

# Configuration du Wi-Fi
'''
La fonction connect() du module configuration_wifi
est appelée pour configurer la connexion Wi-Fi de l'appareil.
'''
connect()


# Configuration de l'encodeur
e=Encoder()
lcd.println("Mise en marche de Serveur", color = lcd.YELLOW)



# Configuration du socket TCP
'''
Un socket TCP est configuré pour écouter les connexions entrantes sur
l'adresse IP 192.168.0.164 et le port 80.
Le socket est configuré en mode non bloquant.
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.116.227', 65000))
s.listen(2)
s.setblocking(False)  # configurez le socket pour qu'il soit non bloquant
time.sleep(1)

temp = 0
hum = 0
presence = ""
http = "GET / HTTP/1.1"#constante qui sert à traiter les requettes http

lcd.clear()#effacer l'ancien affichage de l'appareil
lcd.setColor(lcd.WHITE)

topic_pub1 = b'/Direction_du_vent'
topic_pub2 = b'/Vitesse_du_vent'
topic_pub3 = b'/temperature'
topic_pub4 = b'/humidite'

try:
    client = connectmqtt()
except OSError :
    print("erreur de connexion au broker")
    pass


# Variables pour la simulation du vent
vitesse_vent = 0
direction_vent = 0

# Boucle principale
while True:
    # Lecture de la position de l'encodeur
    position = e.getPosition()
    # Mise à jour de la vitesse et de la direction du vent
    vitesse_vent = position * 0.1  # Utilisation directe de la position comme vitesse 
    direction_vent = position % 360  # Utilisation de la position modulo 360 comme direction 
    print(e.i2c.scan())  
    print(e.getButtonStatus(),' - ',position)
    e.setLEDColor(1,0x00,0x00,0xff)
    print('-------')
    time.sleep(1)
    pass
    ready_to_read, _, _ = select.select([s], [], [], 0)  # surveillez le socket pour une connexion        
    if ready_to_read:
        s.settimeout(0.1)
        try :
            conn, addr = s.accept()
            print('Une connexion de %s' % str(addr))
            request = conn.recv(1024)
            request1 = request.decode("utf-8")
            print(request1)
            donnees2 = request1.split(' ')
            print(donnees2[0])           

            tempp = 'Temperature'
            humm = 'humidite'
            
             # Traitement des différents requêtes
            if request1 == 'packet'  :
                print("allume")
                conn.sendall(str(e.getPosition()).encode("UTF-8"))
                
            if donnees2[0] == tempp and donnees2[3] == humm:               
                temp = (donnees2[2].split('.'))[0]
                hum = (donnees2[4].split('.'))[0]
                print(donnees2)
                conn.close()

            if request1 == 'personne':
                presence = "le controleur n'est pas présent "
                conn.close()

            if request1 == 'presence':
                presence = "le controleur est présent "
                conn.close()

            
            # Traitement de la requête
            if http in request1:
                response = web_page()
                #Envoi de la réponse
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
                conn.close()
           
        except:
            pass
    # Affichage des données sur l'écran LCD   
    lcd.setCursor(0,150)
    lcd.font(lcd.FONT_DejaVu18)
    
    lcd.println("Le vitesse du vent  :"+str(+e.getPosition()), color = lcd.YELLOW)
    lcd.println("La direction du vent :"+str(direction_vent), color = lcd.YELLOW)

    if e.getPosition() > 1000: # ajuster cette valeur en fonction de votre capteur d'encodeur
        lcd.print("Vent dangereux !", lcd.CENTER, 120)
        
    else:
        lcd.print("Vent normal", lcd.CENTER, 120)    
    lcd.image(100, 0, file="vent.jpg", scale=2, type=lcd.JPG)
    
    try:
        
        msg = str(e.getPosition())
        msg2 = str(position % 360)
        msg3_temprerature = str(temp) 
        msg_humidite= str(hum)
        client.publish(topic_pub1, msg)
        client.publish(topic_pub2, msg2)
        client.publish(topic_pub3, msg3_temprerature)
        client.publish(topic_pub4, msg_humidite)


    except:
        print("erreur connect MQTT")
        pass
    time.sleep(1)
    if buttonC.isPressed():
       e.setLEDColor(1, 0x00, 0x00, 0x00)
       break
  
    
    time.sleep(0.01)

