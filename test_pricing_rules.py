import unittest

from pricing_rules import n_for_y, unit_price

class TestPricingRules(unittest.TestCase):
    def test_valid_rules(self):
        expected_price_for_two = {
            unit_price(0):           0,
            unit_price(1):           2,
            n_for_y({1: 10, 3: 25}): 20,
        }
        for rule, expected in expected_price_for_two.items():
            self.assertEqual(expected, rule(2))

    def test_invalid_rules(self):
        invalid_rules = [
            (unit_price, 0.5),        # neither int nor Decimal
            (n_for_y, {2: 10}),       # no unit price
            (n_for_y, {1: 10, 2: 9}), # decreasing
        ]
        for rule, arg in invalid_rules:
            self.assertRaises(ValueError, rule, arg)


if __name__ == '__main__':
    unittest.main()
