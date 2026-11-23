"""DATA STRUCTURE #3 — Min-heap of challenge heights.

ALGORITHM #2 — heap peek / pop for “next event by smallest height.”
Why a heap: next challenge is always the minimum remaining height.
Peek O(1), pop O(log n) — better than scanning an unsorted list each place (O(n)).
"""

import heapq
import random

from logic.data.constants import (
    CHALLENGE_MAX_HEIGHT,
    CHALLENGE_MIN_GAP,
    CHALLENGE_MIN_HEIGHT,
    DRUNK_DRIVER_DAMAGE,
    EARTHQUAKE_DAMAGE,
    NUM_CHALLENGES,
    WINDSTORM_DAMAGE,
)

# Event names + damage percents (looked up in O(1) via dict).
EVENT_NAMES = ("earthquake", "windstorm", "drunk_driver")
DAMAGE = {
    "earthquake": EARTHQUAKE_DAMAGE,
    "windstorm": WINDSTORM_DAMAGE,
    "drunk_driver": DRUNK_DRIVER_DAMAGE,
}


def make_challenge_heights():
    # Place heights low→high with a minimum gap so events are not stacked.
    heights = []
    lowest_allowed = CHALLENGE_MIN_HEIGHT

    for left in range(NUM_CHALLENGES, 0, -1):
        highest_allowed = CHALLENGE_MAX_HEIGHT - CHALLENGE_MIN_GAP * (left - 1)
        if lowest_allowed > highest_allowed:
            break
        height = random.randint(lowest_allowed, highest_allowed)
        heights.append(height)
        lowest_allowed = height + CHALLENGE_MIN_GAP

    return heights


def make_heap(heights=None):
    # heapify is O(n) — cheaper than n inserts — and leaves min at index 0.
    if heights is None:
        heights = make_challenge_heights()
    heap = list(heights)
    heapq.heapify(heap)
    return heap


def apply_event(tower, event_name):
    # Apply one disaster. Ground hit uses index 0 — no search needed.
    floors = tower.floors_from_ground()
    if not floors:
        return event_name + ": empty tower"

    damage = DAMAGE[event_name]
    percent = int(damage * 100)

    if event_name == "earthquake":
        for floor in floors:
            floor.take_damage(damage)
        return f"Earthquake -{percent}% all floors"

    if event_name == "windstorm":
        for floor in floors[-3:]:
            floor.take_damage(damage)
        return f"Windstorm -{percent}% top floors"

    floors[0].take_damage(damage)
    return f"Drunk driver -{percent}% ground"


def run_challenges(tower, challenge_heap):
    """While tower height ≥ next heap root, pop and apply.

    Why peek/pop: the heap root is the soonest challenge; after pop, the new
    root is the next soonest — classic priority-queue extract-min loop.
    """
    messages = []
    fired = []

    while challenge_heap and challenge_heap[0] <= tower.get_height():
        height = heapq.heappop(challenge_heap)
        event_name = random.choice(EVENT_NAMES)
        messages.append(f"@{height}m {apply_event(tower, event_name)}")
        fired.append(height)

    return messages, fired
