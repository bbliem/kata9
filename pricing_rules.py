from collections import defaultdict
from decimal import Decimal

class NforY:
    """Pricing rule for 'Buy N items for price Y'."""

    def __init__(self, item, quantity, price):
        """Create an 'N for Y' pricing rule.

        Arguments:
            item:
                The SKU to which this rule applies.
            quantity:
                How many items ('N') you need to buy to get the given price.
            price:
                The price ('Y') for the given quantity of the item. Must be of
                type int or Decimal to ensure precise arithmetic.

        Raises:
            ValueError:
                (1) The given price is not an instance of int or Decimal, or
                (2) the quantity is not positive.
        """
        if not (isinstance(price, Decimal) or isinstance(price, int)):
            raise ValueError("Prices must be instances of Decimal or int")

        if quantity < 1:
            raise ValueError("Invalid quantity")

        self.item = item
        self.quantity = quantity
        self.price = price

    def apply(self, num_in_cart):
        """Apply this rule as often as possible for the given number of items.

        Arguments:
            num_in_cart:
                Number of items of the relevant SKU in the shopping cart.

        Returns:
            A pair (x, y), where x is the total price obtained by applying this
            rule as often as possible, and y is the number of items in the
            shopping cart that have not been used for obtaining this price.
        """
        quotient, remainder = divmod(num_in_cart, self.quantity)
        return Decimal(quotient * self.price), remainder


class UnitPrice(NforY):
    """Rule determining the price of a single item."""

    def __init__(self, item, price):
        """Create a unit price rule.

        Arguments:
            item:
                The SKU to which this rule applies.
            price:
                The price for one unit of the item. Must be of type int or
                Decimal to ensure precise arithmetic.

        Raises:
            ValueError:
                The given price is not an instance of int or Decimal.
        """
        super().__init__(item, 1, price)


class PricingRules:
    """A set of pricing rules that are in effect at a time.

    For every SKU, we assume that the price of items of this SKU only depends
    on the number of items of the same SKU in the cart. Furthermore, we assume
    that the total price for items of this SKU in a cart is non-decreasing
    (i.e., buying more of an SKU may not cost less).
    """

    def __init__(self, rules):
        """Create a set of pricing rules.

        Arguments:
            rules:
                An iterable containing the rules that are in effect.

        Raises:
            ValueError:
                (1) Prices for an SKU are not monotonically increasing, or
                (2) some SKUs were given without a unit price.
        """
        # Group the rules by SKU
        self.rules = defaultdict(list)
        for rule in rules:
            self.rules[rule.item].append(rule)

        # Since we only have "buy n for y" rules (or special cases thereof) so
        # far, the optimal order to apply rules for an SKU is obvious: Apply
        # rules with the largest quantities first.
        # To this end, sort quantity-price pairs by quantity (descending).
        for item, rules in self.rules.items():
            self.rules[item] = sorted(rules,
                                      key=lambda r: (r.quantity, r.price),
                                      reverse=True)

            # Ensure that prices are non-decreasing.
            prices = [r.price for r in self.rules[item]]
            if any(x < y for x, y in zip(prices, prices[1:])):
                raise ValueError("Prices are decreasing")

            # We need a unit price for each item.
            smallest_quantity = self.rules[item][-1].quantity
            if smallest_quantity > 1:
                raise ValueError("Must provide unit price")

    def total_for_item(self, item, quantity):
        """Compute the price of a certain quantity of a certain SKU."""
        result = Decimal(0)
        for rule in self.rules[item]:
            subtotal, quantity = rule.apply(quantity)
            result += subtotal
        assert quantity == 0
        return result

    def total(self, item_quantities):
        """Compute the total price for a given shopping cart.

        Arguments:
            item_quantities:
                A dict mapping SKUs to the number of such items bought.

        Returns:
            The total price for the cart according to the rules in effect.
        """
        result = Decimal(0)
        for item, quantity in item_quantities.items():
            result += self.total_for_item(item, quantity)
        return result
