import unittest

from rules_engine import calculate_base_amount, calculate_children_amount, calculate_supplement

# TODO test when using program that doesnt exist?

class TestRulesEngineWinterSupplement(unittest.TestCase):
    def setUp(self):
        self.program = 'winter_supplement'

    def test_calculate_base_amount_single(self):
        family_composition = 'single'
        expected_base_amount = 60
        self.assertEqual(calculate_base_amount(self.program, family_composition), expected_base_amount)

    def test_calculate_base_amount_couple(self):
        family_composition = 'couple'
        expected_base_amount = 120
        self.assertEqual(calculate_base_amount(self.program, family_composition), expected_base_amount)

    def test_calculate_base_amount_invalid_composition(self):
        family_composition = 'alone'
        self.assertRaises(KeyError, calculate_base_amount, self.program, family_composition)

    def test_calculate_children_amount_0(self):
        number_of_children = 0
        expected_children_amount = 0
        self.assertEqual(calculate_children_amount(self.program, number_of_children), expected_children_amount)

    def test_calculate_children_amount_1(self):
        number_of_children = 1
        expected_children_amount = 20
        self.assertEqual(calculate_children_amount(self.program, number_of_children), expected_children_amount)
    
    def test_calculate_children_amount_4(self):
        number_of_children = 4
        expected_children_amount = 80
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

    def test_calculate_supplement_single_1(self):
        number_of_children = 1
        family_composition = 'single'
        eligible = True
        expected_base_amount = 60
        expected_children_amount = 20.0
        expected_supplement_amount = 80.0

        response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
        self.assertEqual(response['baseAmount'], expected_base_amount)
        self.assertEqual(response['childrenAmount'], expected_children_amount)
        self.assertEqual(response['supplementAmount'], expected_supplement_amount)

    def test_calculate_supplement_single_2(self):
        number_of_children = 2
        family_composition = 'single'
        eligible = True
        expected_base_amount = 60
        expected_children_amount = 40.0
        expected_supplement_amount = 100.0

        response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
        self.assertEqual(response['baseAmount'], expected_base_amount)
        self.assertEqual(response['childrenAmount'], expected_children_amount)
        self.assertEqual(response['supplementAmount'], expected_supplement_amount)

    def test_calculate_supplement_couple_0(self):
        number_of_children = 0
        family_composition = 'couple'
        eligible = True
        expected_base_amount = 120
        expected_children_amount = 0.0
        expected_supplement_amount = 120.0

        response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
        self.assertEqual(response['baseAmount'], expected_base_amount)
        self.assertEqual(response['childrenAmount'], expected_children_amount)
        self.assertEqual(response['supplementAmount'], expected_supplement_amount)

    def test_calculate_supplement_couple_1(self):
        number_of_children = 1
        family_composition = 'couple'
        eligible = True
        expected_base_amount = 120
        expected_children_amount = 20.0
        expected_supplement_amount = 140.0

        response = calculate_supplement(self.program, number_of_children, family_composition, eligible)
        self.assertEqual(response['baseAmount'], expected_base_amount)
        self.assertEqual(response['childrenAmount'], expected_children_amount)
        self.assertEqual(response['supplementAmount'], expected_supplement_amount)