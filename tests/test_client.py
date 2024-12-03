import unittest
from unittest.mock import MagicMock, patch

from client import MQTTClientWrapper
from config import HOST, KEEP_ALIVE, PORT


class TestMQTTClientWrapper(unittest.TestCase):
    def setUp(self):
        self.input_topic = 'test/input'
        self.output_topic = 'test/output'
        self.topic_id = '123'
        self.on_message = MagicMock()

    @patch('client.mqtt.Client')
    def test_start_forever(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        client = MQTTClientWrapper(
            self.input_topic, self.output_topic, self.topic_id, self.on_message
        )
        client.start_forever()

        mock_client.connect.assert_called_once_with(
            HOST, PORT, KEEP_ALIVE)
        mock_client.loop_forever.assert_called_once()

    @patch('client.mqtt.Client')
    def test_on_connect_subscription(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        client = MQTTClientWrapper(
            self.input_topic, self.output_topic, self.topic_id, self.on_message
        )
        client._on_connect(
            mock_client, None, None, 0, None
        )

        mock_client.subscribe.assert_called_once_with(
            f'{self.input_topic}/{self.topic_id}')
