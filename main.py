import json

import paho.mqtt.client as mqtt

from config import *
from rules_engine import calculate_winter_supplement


def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected with result code {reason_code}')
    client.subscribe(f'{INPUT_TOPIC}/{TOPIC_ID}')

def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload}')

    input_data = json.loads(msg.payload)
    # TODO validate input_data
    calculated_amounts = calculate_winter_supplement(input_data['numberOfChildren'], 
                                                     input_data['familyComposition'], 
                                                     input_data['familyUnitInPayForDecember'])

    output_data = {
        "id": input_data['id'], 
        "isEligible": input_data['isEligible'], 
        "baseAmount": calculated_amounts['baseAmount'],
        "childrenAmount": calculated_amounts['childrenAmount'], 
        "supplementAmount": calculated_amounts['supplementAmount'] 
    }
    encoded_output_data = json.dumps(output_data, indent=2).encode('utf-8')

    client.publish(f'{OUTPUT_TOPIC}/{TOPIC_ID}', encoded_output_data)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(HOST, PORT, 60)

mqttc.loop_forever()