"""One floor as plain data (no linked-list pointers).

Why: the tower is a list of these objects. Keeping Floor simple avoids mixing
node pointers with material math; weight/capacity stay O(1) property checks.
"""

from logic.data.constants import CAPACITY_CONSTANT


class Floor:
    def __init__(self, roll_data):
        # Copy the decoded roll into fields the tower algorithms will use.
        self.material_name = roll_data["material_name"]
        self.tier = roll_data["tier"]
        self.height = roll_data["height"]
        self.units = roll_data["units"]
        self.weight_per_unit = roll_data["weight_per_unit"]
        self.strength = roll_data["capacity_mult"]
        self.health = 1.0  # challenges multiply this down

        if "image" in roll_data:
            self.image = roll_data["image"]
        else:
            self.image = self.material_name

    def get_weight(self):
        # O(1): mass used when summing load above a floor.
        weight = self.units * self.weight_per_unit
        return weight

    def get_max_load(self):
        # O(1): how much weight this floor can hold right now.
        max_load = (
            self.strength
            * self.height
            * CAPACITY_CONSTANT
            * self.health
        )
        return max_load

    def take_damage(self, percent):
        # Multiplicative damage (10% twice → 0.9 × 0.9); never below 0.
        new_health = self.health * (1.0 - percent)
        if new_health < 0.0:
            new_health = 0.0
        self.health = new_health

    def label(self):
        # Short text for demos / sidebar-style prints.
        text = self.material_name + ":" + str(self.height) + "m"
        return text
