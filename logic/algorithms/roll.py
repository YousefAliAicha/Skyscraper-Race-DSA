"""Decode a 5-digit roll into a floor recipe.

Why one number: easy to print, test, and replay — better than four separate
random draws that are hard to reproduce in unit tests. Decoding is O(1).
"""

import random

from logic.data.constants import ROLL_MAX, ROLL_MIN
from logic.data.materials import (
    get_material,
    tier_for_digit,
    units_from_amount,
)


def generate_roll():
    # Uniform 5-digit int; full_decode turns it into material + height.
    roll = random.randint(ROLL_MIN, ROLL_MAX)
    return roll


def decode_roll(roll):
    # Split digits: tier, amount, material pick, height (d4+d5, min 2).
    text = str(roll)
    if len(text) != 5:
        raise ValueError("roll must be 5 digits")

    digit1 = int(text[0])
    digit2 = int(text[1])
    digit3 = int(text[2])
    digit4 = int(text[3])
    digit5 = int(text[4])

    if digit2 == 0:
        amount = 10
    else:
        amount = digit2

    height = digit4 + digit5
    if height < 2:
        height = 2

    result = {
        "roll": roll,
        "tier": tier_for_digit(digit1),
        "amount": amount,
        "material_digit": digit3,
        "height": height,
    }
    return result


def full_decode(roll):
    # Attach hash-table material stats so Floor(...) is ready in one step.
    parts = decode_roll(roll)
    material = get_material(parts["tier"], parts["material_digit"])
    units = units_from_amount(parts["amount"])

    result = {
        "roll": roll,
        "tier": parts["tier"],
        "material_name": material["name"],
        "weight_per_unit": material["weight"],
        "capacity_mult": material["strength"],
        "units": units,
        "height": parts["height"],
        "image": material["name"],
    }
    return result
