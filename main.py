"""
Diddi and Eli: A platformer game with scaling challenges.
"""

import pyxel

from src import stages_list
from src.tools import init_class, savedata_fix, get_savedata, draw_stats, POSSIBLE_LEVELS
from src.scenes import BaseScene
from src.menu import Menu


class Main:
    """
    Main object for the game, though most of the interface
    is operated by the src-stored objects.
    """

    situation = None

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.situation = init_class(stages_list["menu"], 0)
        self.situation.restore_coins(get_savedata()["saved_coins"])
        pyxel.run(self.update, self.draw)

    def update(self):
        self.situation.update()
        # If the situation "ends", jump into the next one
        # Also, keep memory of your player choice :)
        if self.situation.finished:
            coin_reset = 0
            tmp = self.situation.player_choice
            if self.situation.nextlevel not in ("menu", "death"):
                savedata_fix("level", self.situation.nextlevel)
                if type(self.situation).__name__.lower() in POSSIBLE_LEVELS and self.situation.check_anyone_alive:
                    savedata_fix("saved_coins", self.situation.get_coin_count())
            if not isinstance(self.situation, BaseScene):
                coin_reset = get_savedata()["saved_coins"]
            if isinstance(self.situation, Menu):
                if self.situation.stage == "start":
                    coin_reset = 0
            self.situation = init_class(stages_list[self.situation.nextlevel], tmp)
            self.situation.restore_coins(coin_reset)
            del tmp, coin_reset

    def draw(self):
        self.situation.draw()
        draw_stats(
            self.situation.get_scroll_x(),
            self.situation.draw_v,
            self.situation.player_choice,
            self.situation.get_coin_count(),
            str(type(self.situation)),
        )


if __name__ == "__main__":
    pyxel.init(128, 144, title="Diddi and Eli", capture_sec=120)
    # pyxel.fullscreen(True)
    Main()
