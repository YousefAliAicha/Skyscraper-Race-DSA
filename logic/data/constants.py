"""Balance knobs in one place so tuning does not require hunting the algorithms."""

# Win / turn length — raise TARGET_HEIGHT for longer games.
TARGET_HEIGHT = 150
ROLLS_PER_TURN = 3

# 5-digit roll range (inclusive).
ROLL_MIN = 10000
ROLL_MAX = 99999

# Digit 1 → tier. A dict maps digits in O(1); clearer than a long if/elif chain.
TIER_RANGES = {
    1: "junk", 2: "junk", 3: "junk",
    4: "common", 5: "common", 6: "common", 7: "common",
    8: "strong", 9: "strong",
}

# amount digit × this = material units used in weight/capacity.
UNITS_PER_AMOUNT = 150

# max_load = strength × height × CAPACITY_CONSTANT × health
CAPACITY_CONSTANT = 1200

# Challenge schedule: three spaced heights in this band.
NUM_CHALLENGES = 3
CHALLENGE_MIN_HEIGHT = 50
CHALLENGE_MAX_HEIGHT = 130
CHALLENGE_MIN_GAP = 25
EARTHQUAKE_DAMAGE = 0.06
WINDSTORM_DAMAGE = 0.10
DRUNK_DRIVER_DAMAGE = 0.15

# UI board size (read by game/ only; kept here so one constants file exists).
BOARD_ROWS = 14
BOARD_COLS = 10
CELL_SIZE = 64
P1_COLS = (0, 1, 2)
P2_COLS = (7, 8, 9)
TOWER_TOP_ROW = 2
TOWER_BOTTOM_ROW = 12
GROUND_ROW = 13
MAX_VISIBLE_FLOORS = TOWER_BOTTOM_ROW - TOWER_TOP_ROW + 1
