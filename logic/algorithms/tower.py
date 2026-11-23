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
        if len(self.floors) == 0:
            return True
        return False

    def floor_count(self):
        count = len(self.floors)
        return count

    def get_height(self):
        # O(n) sum — n is tiny (board shows ~11 floors); clearer than caching.
        total = 0.0
        index = 0
        while index < len(self.floors):
            floor = self.floors[index]
            total = total + floor.height
            index = index + 1
        return total

    def floors_from_ground(self):
        # Copy so UI/tests can iterate without mutating the tower.
        result = []
        index = 0
        while index < len(self.floors):
            result.append(self.floors[index])
            index = index + 1
        return result

    def insert_at(self, position, new_floor):
        # List.insert is O(n) shifts — fine for small n; index = place slot.
        if position < 0:
            raise IndexError("bad position")
        if position > len(self.floors):
            raise IndexError("bad position")
        self.floors.insert(position, new_floor)

    def remove_at(self, index):
        # O(n) pop by index; used when tests delete a single floor.
        removed = self.floors.pop(index)
        return removed

    # --- ALGORITHM #1: recursion ---

    def load_above(self, index):
        """Total weight resting on floors[index].

        Why recursion: load(i) is defined as weight(i+1) + load(i+1); base = top → 0.
        O(n) time / O(n) stack — matches the lower bound (must see each floor above).
        Better than search/sort here: those do not sum a chain.
        """
        # Base case: this is the top floor (nothing above it).
        if index >= len(self.floors) - 1:
            return 0.0

        next_index = index + 1
        next_floor = self.floors[next_index]
        weight_of_next = next_floor.get_weight()
        weight_above_next = self.load_above(next_index)
        total = weight_of_next + weight_above_next
        return total

    def hold_ratio(self, index):
        # capacity / load. Under 1.0 means this floor fails.
        load = self.load_above(index)
        if load == 0:
            return 999.0

        floor = self.floors[index]
        max_load = floor.get_max_load()
        ratio = max_load / load
        return ratio

    # --- ALGORITHM #3: sequential search ---

    def find_weakest_floor_index(self):
        """Return the index with the worst hold_ratio.

        Why sequential search: any floor can be weakest; no sorted key to binary-search.
        Walk once, keep the minimum ratio — O(n) calls to hold_ratio (simple and correct).
        Better than sorting first: we only need the min, not a full order.
        """
        if self.is_empty() is True:
            return None

        # Start by assuming floor 0 is the weakest.
        weakest_index = 0
        worst_ratio = self.hold_ratio(0)

        # Check every other floor one by one.
        index = 1
        while index < len(self.floors):
            ratio = self.hold_ratio(index)
            if ratio < worst_ratio:
                worst_ratio = ratio
                weakest_index = index
            index = index + 1

        return weakest_index

    def check_stable(self):
        # Thin wrapper: ratio + index for the place/collapse flow.
        if self.is_empty() is True:
            return 999.0, None

        weakest_index = self.find_weakest_floor_index()
        ratio = self.hold_ratio(weakest_index)
        return ratio, weakest_index

    def collapse(self, broken_index=None):
        """Drop the broken floor and everything above it.

        Why a slice: in a list, “this index and above” is floors[i:], O(k) copy.
        Simpler than a stack story; still removes top-down correctly.
        """
        if broken_index is None:
            ratio, broken_index = self.check_stable()
            if broken_index is None:
                return [], 0.0
            if ratio >= 1.0:
                return [], 0.0

        if broken_index < 0:
            return [], 0.0
        if broken_index >= len(self.floors):
            return [], 0.0

        # Keep everything below the break; drop the rest.
        fallen = []
        index = broken_index
        while index < len(self.floors):
            fallen.append(self.floors[index])
            index = index + 1

        kept = []
        index = 0
        while index < broken_index:
            kept.append(self.floors[index])
            index = index + 1
        self.floors = kept

        meters_lost = 0.0
        index = 0
        while index < len(fallen):
            meters_lost = meters_lost + fallen[index].height
            index = index + 1

        # Cascade: after a cut, another floor may now be overloaded.
        ratio, weakest_index = self.check_stable()
        if weakest_index is not None:
            if ratio < 1.0:
                more_fallen, more_meters = self.collapse(weakest_index)
                index = 0
                while index < len(more_fallen):
                    fallen.append(more_fallen[index])
                    index = index + 1
                meters_lost = meters_lost + more_meters

        return fallen, meters_lost
