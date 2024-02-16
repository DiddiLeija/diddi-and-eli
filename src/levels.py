"Library containing all the level classes, which honestly are pretty simple."

import pyxel

from .characters import *


class One(BaseLevel):
    """
    Level One: Onion Plateau

    A mostly plain, onion-filled plateau. It's the
    easiest level in the game, so it doesn't contain
    a lot of enemies or tricky spots.

    Mobs: Onions (4), Robot (1)
    """
    enemy_template = {
        "168 64": Onion,
        "264 80": Onion,
        "408 64": Onion,
        "424 48": Onion,
        "566 40": Onion,
        "604 40": Onion,
        "632 0": Onion,
        "696 56": Onion,
        "760 32": Robot,
        "912 48": Robot
    }
    coin_template = [
        "32 80",
        "40 80",
        "48 80",
        "80 72",
        "88 72",
        "96 72",
        "200 64",
        "160 48",
        "160 56",
        "168 48",
        "168 56",
        "208 56",
        "216 56",
        "224 64",
        "280 56",
        "288 56",
        "400 64",
        "408 56",
        "416 48",
        "424 40",
        "424 24",
        "432 48",
        "440 56",
        "448 64",
        "528 24",
        "536 32",
        "544 24",
        "452 32",
        "624 40",
        "632 40"
    ]

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.check_reset():
            self.next = "menu"
        elif self.finished:
            self.next = "two"
        self.update_template()
    
    def draw(self):
        "pyxel-like 'update' function."
        if self.finished:
            return None
        self.draw_template()
