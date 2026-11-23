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
        self.image = roll_data.get("image", self.material_name)
        self.health = 1.0  # challenges multiply this down

    def get_weight(self):
        # O(1): mass used when summing load above a floor.
        return self.units * self.weight_per_unit

    def get_max_load(self):
        # O(1): how much weight this floor can hold right now.
        return (
            self.strength
            * self.height
            * CAPACITY_CONSTANT
            * self.health
        )

    def take_damage(self, percent):
        # Multiplicative damage (10% twice → 0.9 × 0.9); never below 0.
        self.health = max(0.0, self.health * (1.0 - percent))

    def label(self):
        # Short text for demos / sidebar-style prints.
        return f"{self.material_name}:{self.height}m"
