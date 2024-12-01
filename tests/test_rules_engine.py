import unittest

from rules_engine import calculate_base_amount, calculate_children_amount, calculate_supplement

class TestRulesEngineWinterSupplement(unittest.TestCase):
    def setUp(self):
        self.program = 'winter_supplement'
    
    def test_calculate_base_amount(self):
        test_cases = [
            ('single', 60),
            ('couple', 120)
        ]
        for family_composition, expected_base_amount in test_cases:
            with self.subTest(family_composition=family_composition):
                    self.assertEqual(calculate_base_amount(self.program, family_composition), expected_base_amount)

    def test_calculate_base_amount_invalid_composition(self):
        family_composition = 'alone'
        self.assertRaises(KeyError, calculate_base_amount, self.program, family_composition)

    def test_calculate_children_amount(self):
        test_cases = [
            (0, 0),
            (1, 20),
            (4, 80)
        ]
        for number_of_children, expected_children_amount in test_cases:
            with self.subTest(number_of_children=number_of_children):
                    self.assertEqual(calculate_children_amount(self.program, number_of_children), expected_children_amount)

    def test_calculate_supplement_ineligible(self):
        number_of_children = 2
        family_composition = 'couple'
        eligible = False
        expected_supplement_amount = 0.0

        response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
        self.assertEqual(response['baseAmount'], expected_supplement_amount)
        self.assertEqual(response['childrenAmount'], expected_supplement_amount)
        self.assertEqual(response['supplementAmount'], expected_supplement_amount)

    def test_calculate_supplement(self):
        eligible = True
        test_cases = [
            (1, 'single', 60, 20.0, 80.0),
            (2, 'single', 60, 40.0, 100.0),
            (4, 'single', 60, 80.0, 140.0),
            (10, 'single', 60, 200.0, 260.0),
            (0, 'couple', 120, 0.0, 120.0),
            (1, 'couple', 120, 20.0, 140.0),
            (4, 'couple', 120, 80.0, 200.0),
            (10, 'couple', 120, 200.0, 320.0),
        ]
        for number_of_children, family_composition, expected_base_amount, expected_children_amount, expected_supplement_amount in test_cases:
            with self.subTest(number_of_children=number_of_children, family_composition=family_composition, eligible=eligible):
                    response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
                    self.assertEqual(response['baseAmount'], expected_base_amount)
                    self.assertEqual(response['childrenAmount'], expected_children_amount)
                    self.assertEqual(response['supplementAmount'], expected_supplement_amount)

    def test_calculate_supplement_invalid_composition(self):
        number_of_children = 2
        family_composition = 'alone'
        eligible = True
        self.assertRaises(KeyError, calculate_supplement, self.program, number_of_children, family_composition, eligible)

    def test_calculate_supplement_invalid_program(self):
        self.program = 'fake_supplement'
        number_of_children = 2
        family_composition = 'single'
        eligible = True
        self.assertRaises(KeyError, calculate_supplement, self.program, number_of_children, family_composition, eligible)