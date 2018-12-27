import unittest

from checkout import Checkout
from pricing_rules import NforY, PricingRules, UnitPrice

RULES = PricingRules([
    UnitPrice('A', 50),
    UnitPrice('B', 30),
    UnitPrice('C', 20),
    UnitPrice('D', 15),
    NforY('A', 3, 130),
    NforY('B', 2, 45),
])


def checkout_total(goods):
    checkout = Checkout(RULES)
    for item in goods:
        checkout.scan(item)
    return checkout.total()


class TestPrice(unittest.TestCase):
    def test_totals(self):
        expected_prices = {
            '':       0,
            'A':      50,
            'AB':     80,
            'CDBA':   115,

            'AA':     100,
            'AAA':    130,
            'AAAA':   180,
            'AAAAA':  230,
            'AAAAAA': 260,

            'AAAB':   160,
            'AAABB':  175,
            'AAABBD': 190,
            'DABABA': 190,
        }
        for goods, total in expected_prices.items():
            self.assertEqual(total, checkout_total(goods))

    def test_incremental(self):
        checkout = Checkout(RULES)

        def assert_total(expected):
            self.assertEqual(expected, checkout.total())

        assert_total(0)
        checkout.scan('A')
        assert_total(50)
        checkout.scan('B')
        assert_total(80)
        checkout.scan('A')
        assert_total(130)
        checkout.scan('A')
        assert_total(160)
        checkout.scan('B')
        assert_total(175)


if __name__ == '__main__':
    unittest.main()
