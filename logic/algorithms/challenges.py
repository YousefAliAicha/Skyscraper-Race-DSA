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
    left = NUM_CHALLENGES

    while left > 0:
        highest_allowed = CHALLENGE_MAX_HEIGHT - CHALLENGE_MIN_GAP * (left - 1)
        if lowest_allowed > highest_allowed:
            break

        height = random.randint(lowest_allowed, highest_allowed)
        heights.append(height)
        lowest_allowed = height + CHALLENGE_MIN_GAP
        left = left - 1

    return heights


def make_heap(heights=None):
    # heapify is O(n) — cheaper than n inserts — and leaves min at index 0.
    if heights is None:
        heights = make_challenge_heights()

    heap = []
    index = 0
    while index < len(heights):
        heap.append(heights[index])
        index = index + 1

    heapq.heapify(heap)
    return heap


def apply_event(tower, event_name):
    # Apply one disaster. Ground hit uses index 0 — no search needed.
    floors = tower.floors_from_ground()
    if len(floors) == 0:
        return event_name + ": empty tower"

    damage = DAMAGE[event_name]
    percent = int(damage * 100)

    if event_name == "earthquake":
        index = 0
        while index < len(floors):
            floors[index].take_damage(damage)
            index = index + 1
        return "Earthquake -" + str(percent) + "% all floors"

    if event_name == "windstorm":
        # Hit up to the top 3 floors.
        start = len(floors) - 3
        if start < 0:
            start = 0
        index = start
        while index < len(floors):
            floors[index].take_damage(damage)
            index = index + 1
        return "Windstorm -" + str(percent) + "% top floors"

    # drunk_driver: always the ground floor
    floors[0].take_damage(damage)
    return "Drunk driver -" + str(percent) + "% ground"


def run_challenges(tower, challenge_heap):
    """While tower height ≥ next heap root, pop and apply.

    Why peek/pop: the heap root is the soonest challenge; after pop, the new
    root is the next soonest — classic priority-queue extract-min loop.
    """
    messages = []
    fired = []

    while len(challenge_heap) > 0:
        next_height = challenge_heap[0]  # peek: O(1)
        if next_height > tower.get_height():
            break

        height = heapq.heappop(challenge_heap)  # pop: O(log n)
        event_name = random.choice(EVENT_NAMES)
        message = "@" + str(height) + "m " + apply_event(tower, event_name)
        messages.append(message)
        fired.append(height)

    return messages, fired
