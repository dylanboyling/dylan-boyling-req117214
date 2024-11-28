import json

import paho.mqtt.client as mqtt

from config import *
from rules_engine import calculate_winter_supplement
from validation import validate_input_data


def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected with result code {reason_code}')
    client.subscribe(f'{INPUT_TOPIC}/{TOPIC_ID}')

def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload}')

    input_data = json.loads(msg.payload)
    try:
        validate_input_data(input_data)
    except ValueError as e:
        print(f'Input validation error {e}')
        # TODO publish error message with 0 values, it does nothing but would be good practice I think
        return
    except Exception as e:
        print(f'Unexpected error {e}')
        return

    calculated_amounts = calculate_winter_supplement(input_data['numberOfChildren'], 
                                                     input_data['familyComposition'], 
                                                     input_data['familyUnitInPayForDecember'])

    output_data = {
        "id": input_data['id'], 
        "isEligible": input_data['familyUnitInPayForDecember'], 
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