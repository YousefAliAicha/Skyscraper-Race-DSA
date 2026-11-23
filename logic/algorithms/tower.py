"""DATA STRUCTURE #2 — Python list (dynamic array) of floors.
  index 0 = ground, last index = top.

Why a list: place-by-slot is natural with indices; insert/pop are simple.
Better here than a linked list: no pointer bugs, and we never need O(1) splice mid-node.

ALGORITHMS in this file:
  #1 Recursion         — load_above(index)
  #3 Sequential search — find_weakest_floor_index()
"""

from logic.data.floor import Floor  # noqa: F401


class Tower:
    def __init__(self):
        # Contiguous list of Floor objects; [0] is always the ground floor.
        self.floors = []

    def is_empty(self):
        return len(self.floors) == 0

    def floor_count(self):
        return len(self.floors)

    def get_height(self):
        # O(n) sum — n is tiny (board shows ~11 floors); clearer than caching.
        total = 0.0
        for floor in self.floors:
            total += floor.height
        return total

    def floors_from_ground(self):
        # Shallow copy so UI/tests can iterate without mutating the tower.
        return list(self.floors)

    def insert_at(self, position, new_floor):
        # List.insert is O(n) shifts — fine for small n; index = place slot.
        if position < 0 or position > len(self.floors):
            raise IndexError("bad position")
        self.floors.insert(position, new_floor)

    def remove_at(self, index):
        # O(n) pop by index; used when tests delete a single floor.
        return self.floors.pop(index)

    # --- ALGORITHM #1: recursion ---

    def load_above(self, index):
        """Total weight resting on floors[index].

        Why recursion: load(i) is defined as weight(i+1) + load(i+1); base = top → 0.
        O(n) time / O(n) stack — matches the lower bound (must see each floor above).
        Better than search/sort here: those do not sum a chain.
        """
        if index >= len(self.floors) - 1:
            return 0.0

        next_index = index + 1
        next_floor = self.floors[next_index]
        return next_floor.get_weight() + self.load_above(next_index)

    def hold_ratio(self, index):
        # capacity / load. Under 1.0 means this floor fails.
        load = self.load_above(index)
        if load == 0:
            return 999.0
        return self.floors[index].get_max_load() / load

    # --- ALGORITHM #3: sequential search ---

    def find_weakest_floor_index(self):
        """Return the index with the worst hold_ratio.

        Why sequential search: any floor can be weakest; no sorted key to binary-search.
        Walk once, keep the minimum ratio — O(n) calls to hold_ratio (simple and correct).
        Better than sorting first: we only need the min, not a full order.
        """
        if self.is_empty():
            return None

        weakest_index = 0
        worst_ratio = self.hold_ratio(0)

        index = 1
        while index < len(self.floors):
            ratio = self.hold_ratio(index)
            if ratio < worst_ratio:
                worst_ratio = ratio
                weakest_index = index
            index += 1

        return weakest_index

    def check_stable(self):
        # Thin wrapper: ratio + index for the place/collapse flow.
        if self.is_empty():
            return 999.0, None

        weakest_index = self.find_weakest_floor_index()
        return self.hold_ratio(weakest_index), weakest_index

    def collapse(self, broken_index=None):
        """Drop the broken floor and everything above it.

        Why a slice: in a list, “this index and above” is floors[i:], O(k) copy.
        Simpler than a stack story; still removes top-down correctly.
        """
        if broken_index is None:
            ratio, broken_index = self.check_stable()
            if broken_index is None or ratio >= 1.0:
                return [], 0.0

        if broken_index < 0 or broken_index >= len(self.floors):
            return [], 0.0

        fallen = self.floors[broken_index:]
        self.floors = self.floors[:broken_index]

        meters_lost = 0.0
        for floor in fallen:
            meters_lost += floor.height

        # Cascade: after a cut, another floor may now be overloaded.
        ratio, weakest_index = self.check_stable()
        if weakest_index is not None and ratio < 1.0:
            more_fallen, more_meters = self.collapse(weakest_index)
            fallen.extend(more_fallen)
            meters_lost += more_meters

        return fallen, meters_lost
