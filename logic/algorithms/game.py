"""Turn engine only — no GUI.

Why separate from game/: UI can be swapped without touching DSA code.
Flow: roll → place/scrap → heap challenges → sequential stability → win.
"""

from logic.algorithms.challenges import run_challenges
from logic.algorithms.player import Player
from logic.algorithms.roll import full_decode, generate_roll
from logic.data.constants import ROLLS_PER_TURN, TARGET_HEIGHT
from logic.data.floor import Floor


class Game:
    def __init__(self, name1="P1", name2="P2", enable_challenges=True):
        # Two players; index 0 starts. feed{} is for the sidebar UI.
        self.players = []
        self.players.append(Player(name1, ROLLS_PER_TURN))
        self.players.append(Player(name2, ROLLS_PER_TURN))

        self.current_index = 0
        self.phase = "roll"
        self.winner = None
        self.last_collapse = None
        self.enable_challenges = enable_challenges
        self.message = ""
        self.feed = {
            "headline": name1 + "'s turn",
            "detail": "Press R or click ROLL",
            "result": "Waiting",
            "result_ok": True,
            "events": [],
        }
        self.message = self._prompt_roll()

    def current_player(self):
        player = self.players[self.current_index]
        return player

    def side_hint(self):
        if self.current_index == 0:
            return "LEFT"
        return "RIGHT"

    def _prompt_roll(self):
        player = self.current_player()
        text = player.name + "'s turn — roll a floor"
        return text

    def _set_feed(self, headline, detail, result="OK", result_ok=True, events=None):
        # Structured status so the UI does not parse free-text messages.
        if events is None:
            events = []

        self.feed = {
            "headline": headline,
            "detail": detail,
            "result": result,
            "result_ok": result_ok,
            "events": events,
        }

    def roll(self):
        # O(1) decode + hash-table material lookup via full_decode.
        if self.phase == "game_over":
            raise RuntimeError("Game over")
        if self.phase != "roll":
            raise RuntimeError("Place or scrap first")

        player = self.current_player()
        if player.rolls_left <= 0:
            raise RuntimeError("No rolls left")

        recipe = full_decode(generate_roll())
        player.pending_roll = recipe
        player.rolls_left = player.rolls_left - 1
        self.phase = "place"

        if recipe["tier"] == "junk":
            tip = "Weak — put on top or scrap"
        elif recipe["tier"] == "strong":
            tip = "Strong — good at the bottom"
        else:
            tip = "Move the arrow, then press Enter"

        self.message = (
            "Rolled "
            + recipe["material_name"]
            + " "
            + str(recipe["height"])
            + "m"
        )
        self._set_feed(
            "Rolled " + recipe["material_name"],
            str(recipe["height"]) + " m — " + tip,
            "Choose a height",
        )
        return recipe

    def scrap_roll(self):
        # Discard pending recipe; end turn if no rolls left.
        player = self.current_player()
        if self.phase != "place":
            raise RuntimeError("Nothing to scrap")
        if player.pending_roll is None:
            raise RuntimeError("Nothing to scrap")

        player.pending_roll = None
        self._set_feed("Scrapped", "That roll was discarded", "OK")

        if player.rolls_left > 0:
            self.phase = "roll"
            self.message = self._prompt_roll()
        else:
            self.end_turn()

    def place_floor(self, position):
        # Uses list insert, heap challenges, recursion+scan stability, then win.
        player = self.current_player()
        if self.phase != "place":
            raise RuntimeError("Roll first")
        if player.pending_roll is None:
            raise RuntimeError("Roll first")

        recipe = player.pending_roll

        slot = position
        if slot < 0:
            slot = 0
        if slot > player.tower.floor_count():
            slot = player.tower.floor_count()

        player.tower.insert_at(slot, Floor(recipe))
        player.pending_roll = None
        self.last_collapse = None

        events = []
        if self.enable_challenges is True:
            # ALGORITHM #2: peek/pop challenges whose height ≤ tower height.
            events, _fired = run_challenges(
                player.tower,
                player.challenge_heap,
            )

        collapsed = False
        # ALGORITHM #1 + #3: recursive loads inside sequential weakest search.
        ratio, weakest_index = player.tower.check_stable()
        if weakest_index is not None:
            if ratio < 1.0:
                self.last_collapse = player.tower.collapse(weakest_index)
                collapsed = True

        height = player.tower_height()
        if collapsed is True:
            fallen_floors, meters_lost = self.last_collapse
            self._set_feed(
                "Placed "
                + recipe["material_name"]
                + " ("
                + str(recipe["height"])
                + " m)",
                "Slot " + str(slot) + " → tower " + str(int(height)) + " m",
                "Collapsed — lost "
                + str(len(fallen_floors))
                + " floors ("
                + str(int(meters_lost))
                + " m)",
                False,
                events,
            )
            self.message = "Collapse! " + str(int(height)) + " m left"
        else:
            self._set_feed(
                "Placed "
                + recipe["material_name"]
                + " ("
                + str(recipe["height"])
                + " m)",
                "Slot " + str(slot) + " → tower " + str(int(height)) + " m",
                "Stable",
                True,
                events,
            )
            self.message = "Placed — " + str(int(height)) + " m"

        if self.check_win() is True:
            result = {"collapsed": collapsed, "won": True}
            return result

        if player.rolls_left > 0:
            self.phase = "roll"
        else:
            self.end_turn()

        result = {"collapsed": collapsed, "won": False}
        return result

    def place_on_top(self):
        # Convenience for demos/tests: append at len(floors).
        player = self.current_player()
        top_slot = player.tower.floor_count()
        result = self.place_floor(top_slot)
        return result

    def check_win(self):
        player = self.current_player()
        if player.tower_height() >= TARGET_HEIGHT:
            self.winner = player
            self.phase = "game_over"
            player.won = True
            self.message = player.name + " wins!"
            self._set_feed(
                player.name + " wins",
                "Reached " + str(int(player.tower_height())) + " m",
                "Victory",
            )
            return True
        return False

    def end_turn(self):
        # Flip 0↔1 and refresh the other player's roll budget.
        if self.phase == "game_over":
            return

        if self.current_index == 0:
            self.current_index = 1
        else:
            self.current_index = 0

        player = self.current_player()
        player.reset_rolls()
        self.phase = "roll"
        self.message = self._prompt_roll()
        self._set_feed(
            player.name + "'s turn",
            "Build on the " + self.side_hint() + " side",
            str(player.rolls_left) + " rolls ready",
        )
