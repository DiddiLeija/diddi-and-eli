"""
Diddi and Eli: A platformer game with scaling challenges.
"""

import pyxel

from src import One, Two, Three, Four, Menu


class Main:
    """
    Main object for the game, though most of the interface
    is operated by the src-stored objects.
    """
    situation = None

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.situation = Menu()
    
    def update(self):
        self.situation.update()
    
    def draw(self):
        self.situation.draw()


if __name__ == "__main__":
    pyxel.init(128, 128, "Diddi and Eli")
    Main()
