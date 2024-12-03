import logging

import paho.mqtt.client as mqtt

from config import HOST, KEEP_ALIVE, PORT

logger = logging.getLogger(__name__)


class MQTTClientWrapper:
    def __init__(self, input_topic, output_topic, topic_id, on_message):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.topic_id = topic_id

        self.client.on_connect = self._on_connect
        self.client.on_message = on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        logger.info(
            f'Connected to topic {self.input_topic} with result code {reason_code}')
        client.subscribe(f'{self.input_topic}/{self.topic_id}')

    def start(self):
        self.client.connect(HOST, PORT, KEEP_ALIVE)
        self.client.loop_forever()
