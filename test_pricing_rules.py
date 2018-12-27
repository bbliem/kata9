import unittest

from pricing_rules import NforY, PricingRules, UnitPrice

class TestUnitPrice(unittest.TestCase):
    def test_invalid_type(self):
        self.assertRaises(ValueError, UnitPrice, 'X', 0.5)


class TestNforY(unittest.TestCase):
    def test_invalid_type(self):
        self.assertRaises(ValueError, NforY, 'X', 2, 0.5)

    def test_invalid_quantity(self):
        self.assertRaises(ValueError, NforY, 'X', 0, 1)
        self.assertRaises(ValueError, NforY, 'X', -1, 1)


class TestPricingRules(unittest.TestCase):
    def test_valid_rules(self):
        expected_price_for_two = [
            (0, [UnitPrice('X', 0)]),
            (2, [UnitPrice('X', 1)]),
            (20, [UnitPrice('X', 10), NforY('X', 3, 25)]),
        ]
        for expected, rules in expected_price_for_two:
            pricing_rules = PricingRules(rules)
            self.assertEqual(expected, pricing_rules.total_for_item('X', 2))

    def test_invalid_rules(self):
        invalid_rules = [
            [NforY('X', 2, 10)],                     # no unit price
            [UnitPrice('X', 10), NforY('X', 2, 9)],  # decreasing
        ]
        for rules in invalid_rules:
            self.assertRaises(ValueError, PricingRules, rules)


if __name__ == '__main__':
    unittest.main()
