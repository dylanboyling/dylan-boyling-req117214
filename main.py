import json
import logging

from client import MQTTClientWrapper
from config import INPUT_TOPIC, OUTPUT_TOPIC, TOPIC_ID
from rules_engine import calculate_supplement
from validation import validate_winter_supplement_input_data

logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding='utf-8', level=logging.INFO)


def on_message(client, userdata, msg):
    logger.info(f'{msg.topic}: {msg.payload}')

    input_data = json.loads(msg.payload)
    try:
        validate_winter_supplement_input_data(input_data)
    except ValueError as e:
        logger.info(f'Input validation error: {e}')
        # TODO publish error message with 0 values, it does nothing but would be good practice I think
        return
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return

    calculated_amounts = calculate_supplement(
        'winter_supplement',
        input_data['numberOfChildren'],
        input_data['familyComposition'],
        input_data['familyUnitInPayForDecember']
    )

    output_data = {
        "id": input_data['id'],
        "isEligible": input_data['familyUnitInPayForDecember'],
        "baseAmount": calculated_amounts['baseAmount'],
        "childrenAmount": calculated_amounts['childrenAmount'],
        "supplementAmount": calculated_amounts['supplementAmount']
    }
    encoded_output_data = json.dumps(output_data, indent=2).encode('utf-8')
    # TODO web app not publishing? delete this later, currently publishing from CLI
    print(encoded_output_data)
    client.publish(f'{OUTPUT_TOPIC}/{TOPIC_ID}', encoded_output_data)


client = MQTTClientWrapper(INPUT_TOPIC, OUTPUT_TOPIC, TOPIC_ID, on_message)
client.start()
