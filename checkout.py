from collections import defaultdict

class Checkout:
    """Representation of the checkout process."""

    def __init__(self, rules):
        """Create a checkout object from the current pricing rules."""
        self.rules = rules
        self.item_quantities = defaultdict(int)

    def scan(self, item):
        """Increase the number of items of the given SKU by one."""
        self.item_quantities[item] += 1

    def total(self):
        """Compute the total price for the scanned items."""
        return self.rules.total(self.item_quantities)
