from umqttsimple import MQTTClient
import ubinascii
import machine
from configwifi import connect


# Connecte le dispositif à un réseau Wi-Fi

connect()


mqtt_broker = '192.168.1.125'
mqtt_username = 'baran'
mqtt_password = 'class'
mqtt_port = 1883

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'temperature'


def connectmqtt():
  global client_id, mqtt_broker
  client = MQTTClient(client_id, mqtt_broker,mqtt_port,mqtt_username,mqtt_password)
  client.connect()
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()



try:
        client = connectmqtt()
        topic_pub = b'temperature'
        msg = str(+e.getPosition()) 
        client.publish(topic_pub, msg)
except OSError as e:
        print("erreur connect MQTT")










