"""
Diddi and Eli: A platformer game with scaling challenges.
"""

import pyxel

from src import stages_list


class Main:
    """
    Main object for the game, though most of the interface
    is operated by the src-stored objects.
    """
    situation = None

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.situation = stages_list["menu"]
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.situation.update()
        # If the situation "ends", jump into the next one
        if self.situation.finished:
            self.situation = stages_list[self.situation.next]
    
    def draw(self):
        self.situation.draw()


if __name__ == "__main__":
    pyxel.init(128, 128, "Diddi and Eli")
    Main()
