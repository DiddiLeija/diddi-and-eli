"""
Diddi and Eli: A platformer game with scaling challenges.
"""

import pyxel

from src import stages_list
from src.tools import init_class, write_savedata, draw_stats


class Main:
    """
    Main object for the game, though most of the interface
    is operated by the src-stored objects.
    """

    situation = None

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.situation = init_class(stages_list["menu"], 0)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.situation.update()
        # If the situation "ends", jump into the next one
        # Also, keep memory of your player choice :)
        if self.situation.finished:
            tmp = self.situation.player_choice
            if self.situation.nextlevel not in ("menu", "death"):
                write_savedata({"level": self.situation.nextlevel})
            self.situation = init_class(stages_list[self.situation.nextlevel], tmp)
            del tmp  # we have to remove 'tmp' ASAP

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
    pyxel.fullscreen(True)  # why not? :P
    Main()
