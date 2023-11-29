"Base classes used across the source code."

import pyxel

import math

from abc import ABC, abstractmethod
from .characters import *


class BaseLevel(ABC):
    "Base level."
    tilemap = 0  # Tilemap used by the level
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    player = list()  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    next = ""  # Where should we go after finishing
    lost = False  # Did we die??
    enemy_templates = dict()  # Coordinates to spawn enemies, unique for each subclass
    enemies = list()  # The list with enemies/mobs
    draw_v = 0  # The 'v' parameter used in 'pyxel.bltm', during level drawing
    music_vol = 0
    SCROLL_BORDER_X = 80
    scroll_x = 0

    def __init__(self, player_choice):
        # pyxel.camera()
        self.player_choice = player_choice
        self.create_characters()
        pyxel.playm(self.music_vol, loop=True)
    
    def startup(self):
        # FIXME: Only use the variables stored at "src/characters",
        #       or only use variables from here.
        self.SCROLL_BORDER_X = 80
        self.scroll_x = 0
        self.create_characters()
        pyxel.playm(self.music_vol, loop=True)

    def check_quit(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def check_reset(self) -> bool:
        if pyxel.btnp(pyxel.KEY_R):
            self.finished = True
            self.next = "menu"
            return True
        return False
    
    def check_anyone_alive(self) -> bool:
        for p in self.player:
            if p.alive:
                return True
        return False
    
    def update_scroll_x(self, player):
        # FIXME: We should get rid of this func
        self.scroll_x = player.get_scroll_x()
    
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
        if not self.check_anyone_alive():
            self.lost = True
            pyxel.playm(6)
            self.startup()
            return
        for e in self.enemies:
            e.update()
        # NOTE: Only player 1 (Diddi, when multiplayer) will move the screen
        # TODO: On multiplayer mode, allow both players to move the screen??
        self.update_scroll_x(self.player[0])
        player_x = self.player[0].x
        if player_x > self.scroll_x + self.SCROLL_BORDER_X:
            # Move the screen if needed
            last_scroll_x = self.scroll_x
            self.scroll_x = min(self.x - self.SCROLL_BORDER_X, 240 * 8)
            self.spawn(last_scroll_x + 128, self.scroll_x + 127)
    
    def draw_template(self):
        "Some drawing actions that should happen in (almost) every instance."
        pyxel.cls(0)
        if self.check_anyone_alive():
            pyxel.camera()
            pyxel.bltm(0, 0, 1, self.scroll_x, self.draw_v, 128, 128, 0)
            pyxel.camera(self.scroll_x, self.draw_v)  # test: self.draw_v or 0?
            for p in self.player:
                p.draw()
            for i in self.enemies:
                i.draw()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
