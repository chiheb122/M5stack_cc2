from umqttsimple import MQTTClient
import ubinascii
import machine

mqtt_broker = '192.168.116.141'
mqtt_username = 'chiba'
mqtt_password = 'class'
mqtt_port = 50003

client_id = ubinascii.hexlify(machine.unique_id())



def connectmqtt():
  global client_id, mqtt_broker
  client = MQTTClient(client_id, mqtt_broker,mqtt_port,mqtt_username,mqtt_password)
  client.connect()
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
'''
position = e.getPosition()


try:
    client = connectmqtt()
    msg = str(e.getPosition())
    msg2 = str(position % 360)
    client.publish(topic_pub1, msg)
    client.publish(topic_pub2, msg2)

except OSError as e:
    print("erreur connect MQTT")


'''







