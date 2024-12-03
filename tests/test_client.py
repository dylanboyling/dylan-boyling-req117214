import json
import unittest
from unittest.mock import MagicMock, patch

from client import MQTTClientWrapper
from config import HOST, KEEP_ALIVE, PORT


class TestMQTTClientWrapper(unittest.TestCase):
    def setUp(self):
        self.input_topic = 'test/input'
        self.output_topic = 'test/output'
        self.topic_id = '123'
        self.message_handler = None

    @patch('client.mqtt.Client')
    def test_start_forever(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, self.message_handler)
        client.start_forever()

        mock_client.connect.assert_called_once_with(HOST, PORT, KEEP_ALIVE)
        mock_client.loop_forever.assert_called_once()

    @patch('client.mqtt.Client')
    def test_on_connect_subscription(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, self.message_handler)
        client._on_connect(mock_client, None, None, 0, None)

        mock_client.subscribe.assert_called_once_with(f'{self.input_topic}/{self.topic_id}')

    @patch('client.mqtt.Client')
    def test_publish_json(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, self.message_handler)
        test_output_data = {"test_key": "test_value"}
        encoded_output_data = json.dumps(test_output_data, indent=2).encode('utf-8')
        client.publish_json(test_output_data)

        mock_client.publish.assert_called_once_with(f'{self.output_topic}/{self.topic_id}', encoded_output_data)

class TestMQTTClientWrapperOnMessage(unittest.TestCase):
    def setUp(self):
        self.input_topic = 'test/input'
        self.output_topic = 'test/output'
        self.topic_id = '123'
        self.publish_topic = f'{self.output_topic}/{self.topic_id}'
        
    @patch('client.mqtt.Client')
    def test_on_message_valid(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        test_input_data = {"id": "test_id"}
        test_output_data = {"id": "test_id", "test": "output"}
        message_handler = MagicMock(return_value=test_output_data)
        
        msg = MagicMock()
        msg.payload = json.dumps(test_input_data).encode("utf-8")
        msg.topic = self.input_topic  

        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, message_handler)
        client._on_message(mock_client, None, msg)

        message_handler.assert_called_once_with(self.input_topic, test_input_data)
        mock_client.publish.assert_called_once_with(
            self.publish_topic, json.dumps(test_output_data, indent=2).encode('utf-8')
        )

    @patch('client.mqtt.Client')
    def test_on_message_json_error(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        test_input_data = {"id": "test_id"}
        test_output_data = {"id": "test_id", "test": "output"}
        message_handler = MagicMock(return_value=test_output_data)
        
        msg = MagicMock()
        msg.payload = json.dumps(test_input_data).encode("utf-8")
        msg.topic = self.input_topic  

        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, message_handler)
        client._on_message(mock_client, None, msg)

        message_handler.assert_called_once_with(self.input_topic, test_input_data)
        mock_client.publish.assert_called_once_with(
            self.publish_topic, json.dumps(test_output_data, indent=2).encode('utf-8')
        )

    @patch('client.mqtt.Client')
    def test_on_message_json_decode_error(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        message_handler = MagicMock()

        msg = MagicMock()
        msg.payload = b'invalid_json'  
        msg.topic = self.input_topic

        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, message_handler)
        client._on_message(mock_client, None, msg)

        message_handler.assert_not_called() 
        mock_client.publish.assert_called_once_with(
            self.publish_topic,
            json.dumps({
                "id": "unknown_id",
                "error": "Expecting value: line 1 column 1 (char 0)"
            }, indent=2).encode('utf-8')
        )

    @patch('client.mqtt.Client')
    def test_on_message_exception(self, MockMQTTClient):
        mock_client = MockMQTTClient.return_value
        message_handler = MagicMock(side_effect=Exception("Test exception"))
        test_input_data = {"id": "test_id"}

        msg = MagicMock()
        msg.payload = json.dumps(test_input_data).encode("utf-8")
        msg.topic = self.input_topic

        client = MQTTClientWrapper(self.input_topic, self.output_topic, self.topic_id, message_handler)
        client._on_message(mock_client, None, msg)

        message_handler.assert_called_once_with(self.input_topic, test_input_data)
        mock_client.publish.assert_called_once_with(
            self.publish_topic,
            json.dumps({
                "id": "test_id",
                "error": "Test exception"
            }, indent=2).encode('utf-8')
        )
