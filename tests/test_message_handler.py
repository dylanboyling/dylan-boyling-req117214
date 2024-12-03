import unittest

from message_handler import winter_supplement_message_handler


class TestWinterSupplementMessageHandler(unittest.TestCase):
    def setUp(self):
        self.topic_id = '123'

    def test_message_handler_missing_id(self):
        input_data = {
            'numberOfChildren': 1, 
            'familyComposition': 'single',
            'familyUnitInPayForDecember': True
            }
        expected_response = {
            'id': 'unknown_id',
            'error': "Missing required input key(s) {'id'}"
            }

        response = winter_supplement_message_handler(self.topic_id, input_data)
        self.assertEqual(response, expected_response)

    def test_message_handler_missing_family(self):
        input_data = {
            'id': '1', 
            'numberOfChildren': 1, 
            'familyComposition': 'single'
            }
        expected_response = {
            'id': '1',
            'error': "Missing required input key(s) {'familyUnitInPayForDecember'}"
            }

        response = winter_supplement_message_handler(self.topic_id, input_data)
        self.assertEqual(response, expected_response)

    def test_message_handler_valid_input(self):
        input_data = {
            'id': 1,
            'numberOfChildren': 1, 
            'familyComposition': 'single',
            'familyUnitInPayForDecember': True
            }
        expected_keys = {'id', 'baseAmount', 'childrenAmount', 'isEligible', 'supplementAmount'}

        response = winter_supplement_message_handler(self.topic_id, input_data)
        self.assertTrue(expected_keys.issubset(response.keys()))
        self.assertIsInstance(response['id'], int)
        self.assertIsInstance(response['baseAmount'], float)
        self.assertIsInstance(response['childrenAmount'], float)
        self.assertIsInstance(response['isEligible'], bool)
        self.assertIsInstance(response['supplementAmount'], float)
