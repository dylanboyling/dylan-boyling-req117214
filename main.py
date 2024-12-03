import logging

from client import MQTTClientWrapper
from config import INPUT_TOPIC, OUTPUT_TOPIC, TOPIC_ID
from message_handler import winter_supplement_message_handler

logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding='utf-8', level=logging.INFO)


if __name__ == "__main__":
    client = MQTTClientWrapper(INPUT_TOPIC, OUTPUT_TOPIC, TOPIC_ID, winter_supplement_message_handler)
    client.start_forever()
