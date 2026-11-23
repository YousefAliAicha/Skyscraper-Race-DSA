"""One player's state: list-tower + roll budget + personal challenge heap.

Why per-player heaps: each builder has their own upcoming events; peeking
heap[0] is O(1) for the sidebar “next challenge” without scanning.
"""

from logic.algorithms.challenges import make_challenge_heights, make_heap
from logic.algorithms.tower import Tower
from logic.data.constants import ROLLS_PER_TURN


class Player:
    def __init__(self, name, rolls_per_turn=ROLLS_PER_TURN):
        self.name = name
        self.tower = Tower()
        self.rolls_per_turn = rolls_per_turn
        self.rolls_left = rolls_per_turn
        self.pending_roll = None
        # Keep the raw list for debugging; heap is what gameplay uses.
        self.challenge_heights = make_challenge_heights()
        self.challenge_heap = make_heap(list(self.challenge_heights))
        self.won = False

    def reset_rolls(self):
        # Called at the start of this player's turn.
        self.rolls_left = self.rolls_per_turn
        self.pending_roll = None

    def tower_height(self):
        return self.tower.get_height()

    def floor_count(self):
        return self.tower.floor_count()

    def next_challenge(self):
        # ALGORITHM #2 peek: min-heap root is the next (smallest) height.
        if self.challenge_heap:
            return self.challenge_heap[0]
        return None
