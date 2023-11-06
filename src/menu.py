import pyxel

from .baseclasses import BaseLevel
from .tools import draw_text

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
                self.stage = "start"
            elif pyxel.btnp(pyxel.KEY_2):
                self.stage = "players"

    def draw(self):
        "Pyxel-like 'draw' function."
        # Clear the screen
        pyxel.cls(0)
        # NOTE: Tilemap 0 is the menu tilemap, ok?
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        # Draw a "menu window"
        pyxel.rectb(20, 30, 88, 70, 7)
        # Main design
        if self.stage == "main":
            draw_text("== Diddi and Eli ==", 23, 33)
            draw_text("[1] Start", 23, 45)
            draw_text("[2] Player mode", 23, 53)
        # Always remind the users how to quit
        draw_text("- Press Q to quit -", 23, 90)
