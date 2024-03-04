"""
Diddi and Eli: A platformer game with scaling challenges.
"""

import pyxel

from src import stages_list
from src.tools import init_class, write_savedata


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
            if self.situation.next != "menu":
                write_savedata({"level": self.situation.next})
            self.situation = init_class(stages_list[self.situation.next], tmp)
            del(tmp)  # we have to remove 'tmp' ASAP
    
    def draw(self):
        self.situation.draw()


if __name__ == "__main__":
    pyxel.init(128, 128, "Diddi and Eli", capture_sec=120)
    Main()
