"Base classes used across the source code."

import pyxel

from abc import ABC, abstractmethod

class BaseLevel(ABC):
    "Base level."
    tilemap = 0  # Tilemap used by the level
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    players = None  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    next = ""  # Where should we go after finishing

    def __init__(self):
        pyxel.camera()  # TODO: is this safe to do here??

    def check_quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def check_reset(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.finished = True
            self.next = "menu"
            return True
        return False

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
