import pyxel

from .baseclasses import BaseLevel
from .characters import *
from .tools import draw_text


class One(BaseLevel):
    """
    Level One: Onion Plateau

    A mostly plain, onion-filled plateau. It's the
    easiest level in the game, so it doesn't contain
    a lot of enemies or tricky spots.
    """

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.check_reset():
            return None
    
    def draw(self):
        "pyxel-like 'update' function."
        pyxel.cls(0)
