"Base classes used across the source code."

import pyxel

from abc import ABC, abstractmethod
from .characters import *

class BaseLevel(ABC):
    "Base level."
    tilemap = 0  # Tilemap used by the level
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    players = None  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    next = ""  # Where should we go after finishing

    def __init__(self):
        pyxel.camera()  # TODO: is this safe to do here??
        # self.create_characters()

    def check_quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def check_reset(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.finished = True
            self.next = "menu"
            return True
        return False
    
    def create_characters(self):
        if self.player_choice == 0:
            self.player = [Player1(0, 0)]
        elif self.player_choice == 1:
            self.player = [Player2(0, 0)]
        elif self.player_choice == 2:
            self.player = [Player1(0, 0), Player2(0, 10)]
    
    def update_template(self):
        "Some update actions that should happen in (almost) every instance."
        for p in self.player:
            p.update()
            for b in p.bullets:
                b.update()
    
    def draw_template(self):
        "Some drawing actions that should happen in (almost) every instance."
        pyxel.cls(0)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
