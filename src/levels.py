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

    def __init__(self):
        BaseLevel.__init__(self)
        pyxel.playm(0, loop=True)

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.check_reset():
            return None
        self.update_template()
    
    def draw(self):
        "pyxel-like 'update' function."
        self.draw_template()
