"""DATA STRUCTURE #1 — Hash table (Python dict).

Why: each roll needs material stats by (tier, group). A dict gives average O(1) lookup.
Better than if/elif or scanning a list: one key → one row, and adding materials is one entry.
"""

from logic.data.constants import TIER_RANGES, UNITS_PER_AMOUNT

# Key = (tier, group). Digit 3 of the roll picks group "a" (0–4) or "b" (5–9).
MATERIALS = {
    ("junk", "a"): {
        "name": "toothpicks",
        "weight": 0.5,
        "strength": 0.3,
    },
    ("junk", "b"): {
        "name": "rotten_wood",
        "weight": 0.8,
        "strength": 0.2,
    },
    ("common", "a"): {
        "name": "wood",
        "weight": 1.0,
        "strength": 1.0,
    },
    ("common", "b"): {
        "name": "brick",
        "weight": 2.0,
        "strength": 1.6,
    },
    ("strong", "a"): {
        "name": "steel",
        "weight": 2.5,
        "strength": 4.5,
    },
    ("strong", "b"): {
        "name": "concrete",
        "weight": 3.0,
        "strength": 3.0,
    },
}


def tier_for_digit(digit):
    # O(1) dict read — same idea as MATERIALS.
    return TIER_RANGES[digit]


def get_material(tier, material_digit):
    # Map digit → group, then one hash-table lookup for the stats row.
    if material_digit <= 4:
        group = "a"
    else:
        group = "b"

    key = (tier, group)
    material = MATERIALS[key]
    return material


def units_from_amount(amount):
    # Linear scale: keeps roll decoding separate from the MATERIALS table.
    units = amount * UNITS_PER_AMOUNT
    return units
