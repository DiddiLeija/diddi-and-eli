"Base classes used across the source code."

import pyxel

from abc import ABC, abstractmethod

class BaseLevel(ABC):
    "Base level."
    tilemap = 0
    players = None

    def __init__(self):
        pass

    def check_quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
