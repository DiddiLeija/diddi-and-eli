"Library containing all the level classes, which honestly are pretty simple."

import pyxel

from .baseclasses import BaseLevel
from .characters import *


class One(BaseLevel):
    """
    Level One: Onion Plateau

    A mostly plain, onion-filled plateau. It's the
    easiest level in the game, so it doesn't contain
    a lot of enemies or tricky spots.
    """
    enemy_template = {(21*8, 8*8): Onion}

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
