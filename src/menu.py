import pyxel

from .characters import BaseLevel
from .tools import draw_text, get_savedata

class Menu(BaseLevel):
    "Menu window."
    saved_stage = ""
    stage = "main"
    player_choice = 0
    enemy_template = dict()
    player_choice_text = {0: "[1] Single (Diddi)", 1: "[2] Single (Eli)", 2: "[3] Multiplayer"}
    music_vol = 5
    reset_coin_counter = True
    gen_clouds = False
    saved_available = False

    def __init__(self, player_choice=None):
        BaseLevel.__init__(self, player_choice)
        # and here comes the funny part: get and save level data
        self.update_saved_stage()
    
    def update_saved_stage(self):
        self.saved_stage = get_savedata()

    def create_characters(self):
        pass

    def update(self):
        "Pyxel-like 'update' function."
        self.update_saved_stage()
        self.saved_available = True
        if self.saved_stage["level"] == "intro":
            self.saved_available = False
        self.check_quit()
        if self.stage == "main":
            if pyxel.btnp(pyxel.KEY_1):
                self.stage = "start"
            elif pyxel.btnp(pyxel.KEY_2):
                self.stage = "startsaved"
            elif pyxel.btnp(pyxel.KEY_3):
                self.stage = "players"
        elif self.stage == "start":
            # Just get into the next window
            self.finished = True
            self.next = "intro"
        elif self.stage == "startsaved":
            # Move to the saved window
            self.finished = True
            self.next = self.saved_stage["level"]
        elif self.stage == "players":
            if pyxel.btnp(pyxel.KEY_1):
                # Option 1 - singleplayer, Diddi
                self.player_choice = 0
            elif pyxel.btnp(pyxel.KEY_2):
                # Option 2 - singleplayer, Eli
                self.player_choice = 1
            elif pyxel.btnp(pyxel.KEY_3):
                # Option 3 - local co-op (Diddi and Eli)
                self.player_choice = 2
            elif pyxel.btnp(pyxel.KEY_R):
                # Return to menu
                self.stage = "main"

    def draw(self):
        "Pyxel-like 'draw' function."
        # Clear the screen
        pyxel.cls(0)
        pyxel.camera(0, self.draw_v)  # TODO: Is this a good idea?
        # NOTE: Tilemap 0 is the menu tilemap, ok?
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        # Draw a "menu window"
        pyxel.rectb(20, 30, 88, 70, 7)
        # Main design
        if self.stage == "main":
            draw_text("== Diddi and Eli ==", 23, 33)
            draw_text("[1] Start new", 23, 45)
            draw_text("[2] Start checkpoint", 23, 53)
            draw_text("[3] Select players", 23, 61)
        # Players selection
        if self.stage == "players":
            draw_text("== Select mode ==", 23, 33)
            for k, v in self.player_choice_text.items():
                if k == self.player_choice:
                    draw_text(v + " <-", 23, 45+(8*k))
                else:
                    draw_text(v, 23, 45+(8*k))
            draw_text("- Press R to return -", 23, 82)
        # Always remind the users how to quit
        draw_text("- Press Q to quit -", 23, 90)

