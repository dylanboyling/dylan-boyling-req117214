import unittest

from validation import validate_bool, validate_key_in_set, validate_keys, validate_non_negative_int, validate_winter_supplement_input_data


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.field_name = 'value'

    def test_validate_keys_valid(self):
        test_cases = [
            ({'id'}, {'id'}),
            ({'id', 'numberOfChildren', 'familyComposition', 'familyUnitInPayForDecember'}, {
             'id', 'numberOfChildren', 'familyComposition', 'familyUnitInPayForDecember'})
        ]
        for required_keys, input_keys in test_cases:
            with self.subTest(required_keys=required_keys):
                self.assertIsNone(validate_keys(required_keys, input_keys))

    def test_validate_keys_invalid(self):
        required_keys = {'id', 'numberOfChildren',
                         'familyComposition', 'familyUnitInPayForDecember'}
        test_cases = [
            (required_keys, set({})),
            (required_keys, {'id'}),
            (required_keys, {'id', 'numberOfChildren', 'familyComposition'})
        ]
        for required_keys, input_keys in test_cases:
            with self.subTest(required_keys=required_keys):
                self.assertRaises(ValueError, validate_keys,
                                  required_keys, input_keys)

    def test_key_in_set_valid(self):
        test_cases = [
            ('single', {'single'}),
            ('single', {'single', 'couple'})
        ]
        for key, valid_set in test_cases:
            with self.subTest(key=key):
                self.assertIsNone(validate_key_in_set(
                    key, valid_set, self.field_name))

    def test_key_in_set_invalid(self):
        test_cases = [
            ('single', set({})),
            ('single', {'couple'}),
            ('invalid', {'single', 'couple'})
        ]
        for key, valid_set in test_cases:
            with self.subTest(key=key):
                self.assertRaises(ValueError, validate_key_in_set,
                                  key, valid_set, self.field_name)

    def test_validate_non_negative_int_valid(self):
        test_cases = [0, 1, 100, 1000]
        for value in test_cases:
            with self.subTest(value=value):
                self.assertIsNone(validate_non_negative_int(
                    value,  self.field_name))

    def test_validate_non_negative_int_invalid(self):
        test_cases = [-1, "bad value", True, ["hello"], None]
        for value in test_cases:
            with self.subTest(value=value):
                self.assertRaises(
                    ValueError, validate_non_negative_int, value, self.field_name)

    def test_validate_bool_valid(self):
        test_cases = [True, False]
        for value in test_cases:
            with self.subTest(value=value):
                self.assertIsNone(validate_bool(value, self.field_name))

    def test_validate_bool_invalid(self):
        test_cases = ["True", 1, 0, None]
        for value in test_cases:
            with self.subTest(value=value):
                self.assertRaises(
                    ValueError, validate_bool, value, self.field_name)


class TestValidateWinterSupplement(unittest.TestCase):
    def test_input_data_valid(self):
        valid_data = {
            'id': '123',
            'numberOfChildren': 1,
            'familyComposition': 'single',
            'familyUnitInPayForDecember': True
        }
        self.assertIsNone(validate_winter_supplement_input_data(valid_data))

    def test_input_data_missing_key(self):
        invalid_data = {
            'id': '123',
            'numberOfChildren': 2,
            'familyComposition': 'single'
        }
        with self.assertRaises(ValueError):
            validate_winter_supplement_input_data(invalid_data)

    def test_input_data_invalid_family_composition(self):
        invalid_data = {
            'id': '123',
            'numberOfChildren': 2,
            'familyComposition': 'invalid_composition',
            'familyUnitInPayForDecember': True
        }
        with self.assertRaises(ValueError):
            validate_winter_supplement_input_data(invalid_data)

    def test_input_data_negative_integer(self):
        invalid_data = {
            'id': '123',
            'numberOfChildren': -1,
            'familyComposition': 'single',
            'familyUnitInPayForDecember': True
        }
        with self.assertRaises(ValueError):
            validate_winter_supplement_input_data(invalid_data)

    def test_input_data_invalid_boolean(self):
        invalid_data = {
            'id': '123',
            'numberOfChildren': 2,
            'familyComposition': 'single',
            'familyUnitInPayForDecember': "true"
        }
        with self.assertRaises(ValueError):
            validate_winter_supplement_input_data(invalid_data)
