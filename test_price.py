import unittest

from checkout import Checkout
from pricing_rules import PricingRules, n_for_y, unit_price

RULES = PricingRules({
    'A': n_for_y({1: 50, 3: 130}),
    'B': n_for_y({1: 30, 2: 45}),
    'C': unit_price(20),
    'D': unit_price(15),
})


def checkout_total(goods):
    co = Checkout(RULES)
    for item in goods:
        co.scan(item)
    return co.total()


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
        co = Checkout(RULES)

        def assert_total(expected):
            self.assertEqual(expected, co.total())

        assert_total(0)
        co.scan('A')
        assert_total(50)
        co.scan('B')
        assert_total(80)
        co.scan('A')
        assert_total(130)
        co.scan('A')
        assert_total(160)
        co.scan('B')
        assert_total(175)


if __name__ == '__main__':
    unittest.main()
