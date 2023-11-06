import pyxel

from .baseclasses import BaseLevel

class Menu(BaseLevel):
    "Menu window."
    stage = "main"
    player_choice = 0

    def __init__(self):
        pass

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.stage == "main":
            if pyxel.btnp(pyxel.KEY_1):
                self.stage = "level"
            elif pyxel.btnp(pyxel.KEY_2):
                self.stage = "players"

    def draw(self):
        "Pyxel-like 'draw' function."
        pyxel.cls(0)
        # NOTE: Tilemap 0 is the menu tilemap, ok?
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
