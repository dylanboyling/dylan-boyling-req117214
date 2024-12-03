import json
import logging

import paho.mqtt.client as mqtt

from config import HOST, KEEP_ALIVE, PORT

logger = logging.getLogger(__name__)


class MQTTClientWrapper:
    def __init__(self, input_topic, output_topic, topic_id, message_handler):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.topic_id = topic_id
        self.message_handler = message_handler

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        logger.info(f'Connected to topic {self.input_topic} with result code {reason_code}')
        client.subscribe(f'{self.input_topic}/{self.topic_id}')

    def _on_message(self, client, userdata, msg):
        logger.info(f'Received message on topic {self.input_topic}')
        input_data = {}
        output_data = {}
        try:
            input_data = json.loads(msg.payload)
            output_data = self.message_handler(msg.topic, input_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error on topic {msg.topic}: {e}")
            output_data = {
                "id": input_data.get('id', 'unknown_id'),
                "error": str(e)
            }
        except Exception as e:
            logger.error(f'Unexpected error handling message on topic {msg.topic}: {e}')
            output_data = {
                "id": input_data.get('id', 'unknown_id'),
                "error": str(e)
            }
        finally:
            if output_data:
                self.publish_json(output_data)

    def start_forever(self):
        self.client.connect(HOST, PORT, KEEP_ALIVE)
        self.client.loop_forever()

    def publish_json(self, output_data):
        encoded_output_data = json.dumps(output_data, indent=2).encode('utf-8')
        self.client.publish(f'{self.output_topic}/{self.topic_id}', encoded_output_data)