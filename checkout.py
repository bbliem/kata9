from collections import defaultdict

class Checkout:
    def __init__(self, rules):
        self.rules = rules
        self.item_quantities = defaultdict(int)

    def scan(self, item):
        self.item_quantities[item] += 1

    def total(self):
        return self.rules.total(self.item_quantities)
