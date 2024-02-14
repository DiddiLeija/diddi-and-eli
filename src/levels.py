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
        "264 80": Onion,
        "424 48": Onion,
        "566 40": Onion,
        "604 40": Onion,
        "696 56": Onion,
        "912 48": Robot
    }

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
