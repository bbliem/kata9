from decimal import Decimal
from collections import OrderedDict

class PricingRules:
    """
    TODO: docstring

    A rule is a function mapping the quantity of an item to its price.
    """

    def __init__(self, rules):
        """rules is a dict mapping items to rules."""
        self.rules = rules

    def total(self, item_quantities):
        result = Decimal(0)
        for item, quantity in item_quantities.items():
            result += self.rules[item](quantity)
        return result


"""Periodic piecewise linear function. We assume that it is monotonically
increasing. Prices must be instances of integer or Decimal because we're
dealing with money and want precise arithmetic.

Iterating over prices yields quantity-price pairs."""
def n_for_y(prices):
    # Sort quantity-price pairs by quantity (descending)
    prices = OrderedDict(sorted(prices.items(), reverse=True))

    if 1 not in prices:
        raise ValueError("Must provide unit price")

    if not all(isinstance(price, Decimal) or isinstance(price, int)
               for price in prices.values()):
        raise ValueError("Prices must be instances of Decimal")

    # We assume that prices are monotonically increasing (i.e., buying more
    # never costs less).
    if list(prices.values()) != sorted(prices.values(), reverse=True):
        raise ValueError("Prices must be monotonically increasing")

    def rule(quantity):
        result = Decimal(0)
        for n, price in prices.items():
            quotient, remainder = divmod(quantity, n)
            result += quotient * price
            quantity = remainder
        return result
    return rule


"""Nicer syntax for the special case when we only have a unit price."""
def unit_price(price):
    # equivalent to return lambda q: q * price
    return n_for_y({1: price})
