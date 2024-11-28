import paho.mqtt.client as mqtt
from config import *

def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected with result code {reason_code}')
    client.subscribe(f'{INPUT_TOPIC}/{TOPIC_ID}')

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(HOST, PORT, 60)

mqttc.loop_forever()