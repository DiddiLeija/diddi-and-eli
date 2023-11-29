"Base classes used across the source code."

import pyxel

import math

from abc import ABC, abstractmethod
from .characters import *


# TODO: Only use the variables stored at "src/characters",
#       or only use variables from here.
SCROLL_BORDER_X = 80
scroll_x = 0


def update_scroll_x(player):
    # FIXME: We should get rid of this func
    scroll_x = player.get_scroll_x()


class BaseLevel(ABC):
    "Base level."
    tilemap = 0  # Tilemap used by the level
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    players = None  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    next = ""  # Where should we go after finishing
    lost = False  # Did we die??
    enemy_templates = dict()  # Coordinates to spawn enemies, unique for each subclass
    enemies = list()  # The list with enemies/mobs

    def __init__(self):
        # NOTE: is this safe to do here, or should we run these per instance?
        pyxel.camera()
        self.create_characters()

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
    
    def spawn(self):
        left_x = math.ceil(left_x / 8)
        right_x = math.floor(right_x / 8)
        for x in range(left_x, right_x + 1):
            for y in range(16):
                if (x*8, y*8) in self.enemy_template:
                    mobclass = self.enemy_templates[(x*8, y*8)]
                    self.enemies.append(mobclass(x * 8, y * 8))
    
    def update_template(self):
        "Some update actions that should happen in (almost) every instance."
        anyone_here = False
        for p in self.player:
            p.update()
            for b in p.bullets:
                b.update()
                for e in self.enemies:
                    # TODO: Check if a bullet hit a mob.
                    pass
            for e in self.enemies:
                    # TODO: Check if a mob hit the player.
                    pass
            if p.alive:
                anyone_here = True
        if not anyone_here:
            self.lost = True
            return
        for e in self.enemies:
            e.update()
        # NOTE: Only player 1 (Diddi, when multiplayer) will move the screen
        # TODO: On multiplayer mode, allow both players to move the screen??
        update_scroll_x(self.player[0])
        player_x = self.player[0].x
        if player_x > scroll_x + SCROLL_BORDER_X:
            # Move the screen if needed
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)
            self.spawn(last_scroll_x + 128, scroll_x + 127)
    
    def draw_template(self):
        "Some drawing actions that should happen in (almost) every instance."
        pyxel.cls(0)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def create_characters(self):
        pass
