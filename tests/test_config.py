import unittest
from config import HOST, PORT, KEEP_ALIVE, INPUT_TOPIC, OUTPUT_TOPIC, TOPIC_ID


class TestConfig(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(HOST, 'test.mosquitto.org')
        self.assertEqual(PORT, 1883)
        self.assertEqual(KEEP_ALIVE, 60)
        self.assertEqual(INPUT_TOPIC, 'BRE/calculateWinterSupplementInput')
        self.assertEqual(OUTPUT_TOPIC, 'BRE/calculateWinterSupplementOutput')
        self.assertIsInstance(TOPIC_ID, str)
