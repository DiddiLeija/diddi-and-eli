"""
Unlike levels, scenes are dialog-focused stages in the game,
to enrich the gameplay and the storyline of Diddi and Eli.

===========================================
How to set up a [BaseScene instance].scenes
===========================================

BaseScene.scenes is the main property to be customized
on each subclass of BaseScene (in other words, each 'scene').

The property itself is a list, where each item is a tuple, which
represents each 'moment' of the scene, and will be switched to the
next one once the user press SPACE. Each tuple element should have these
items:

('x in tilemap', 'y in tilemap', 'dialog text')

'x' and 'y' are integers, and together they represent the spot where the
scene can be found in tilemap 2 (a tilemap dedicated to scenes). 'dialog text'
is just a string with all the text to be displayed.
"""

import pyxel

from .characters import BaseLevel
from .tools import draw_text, get_savedata, report_crash


class BaseScene(BaseLevel):
    "A subclass of levels, that focus on dialogs rather than real gameplay"
    music_vol = 5  # TODO: Don't use the same music than the Menu, compose a new track instead!
    scenes = list()  # list of elements to show for each "click" in the story
    sno = 0  # scene number, increases on each click
    boxcol1 = 0  # Color of the dialog box (interior)
    boxcol2 = 0  # Color of the dialog box (separator)
    nextseq = ""  # Next sequence

    def __init__(self, player_choice):
        self.sno = 0  # for a reason, we'll have to reset this manually?
        self.gen_clouds = False
        BaseLevel.__init__(self, player_choice)

    def create_characters(self):
        # NOTE: No Player classes, please!
        pass

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.check_reset():
            self.nextlevel = "menu"
        elif self.finished:
            self.nextlevel = self.nextseq
        if pyxel.btnp(pyxel.KEY_DELETE):
            self.finished = True
            self.nextlevel = self.nextseq
            return
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sno += 1
            if self.sno >= len(self.scenes):
                self.finished = True
                self.nextlevel = self.nextseq
    
    def draw(self):
        "draw function."
        pyxel.cls(self.bgcolor)
        st = self.scenes[self.sno]
        pyxel.bltm(0, 0, 2, st[0], st[1], 128, 128, 0)
        pyxel.rect(0, 80, 128, 50, self.boxcol1)
        pyxel.rect(0, 79, 128, 1, self.boxcol2)
        draw_text(st[2], 1, 81)
        draw_text("DELETE: skip\nSPACE: continue", 1, 112)
        draw_text(">>", 120, 120)


class DeathSequence(BaseLevel):
    """
    A former scene (though not inherited from BaseScene, nor
    behaving much like BaseLevel) to use when losing the game.
    """
    player_selection = None

    def __init__(self, player_choice):
        self.player_selection = player_choice
    
    def update(self):
        self.check_quit()
        if self.check_reset():
            self.nextlevel = "menu"
        elif pyxel.btnp(pyxel.KEY_ENTER):
            self.finished = True
            self.nextlevel = get_savedata()["level"]
    
    def draw(self):
        pyxel.cls(0)
        draw_text(
            "Oh no! :(\n"
            f"You ({self.get_player_names()}) died.\n"
            "Press R to return to the menu, or\n"
            "ENTER to retry the level you lost."
        )
    
    def get_player_names(self):
        "Get a proper text to refer to the player pack."
        ideas = ["Diddi", "Eli", "Diddi & Eli"]
        try:
            return ideas[self.player_selection]
        except (TypeError, IndexError, ValueError) as exc:
            report_crash(
                f"DeathSequence.get_player_names (player_selection = {self.player_selection})",
                str(exc)
            )


class Intro(BaseScene):
    "Intro sequence."
    scenes = [
        (0, 0, "Diddi and Eli are chatting\nwith Lady Alix, their boss..."),
        (0, 0, "Lady Alix: Hi, Diddi and Eli!\n\nDiddi and Eli: Hi!"),
        (0, 0, "Lady Alix: I need your help,\nfolks. Our enemy, THE SCALER,\nis coming to invade us."),
        (0, 0, "Lady Alix: The Scaler is\nwidely know to be a formidable\nenemy, a destroyer!"),
        (256, 0, "Lady Alix: If the Scaler finds\nus, we'll be doomed to TOTAL\nDESTRUCTION! Forever!"),
        (384, 0, "Diddi: We'll stop him!\n\nEli: Yeah!! Let's go!"),
        (0, 0, "Lady Alix: Great! I'll see you\nlater. Be careful!"),
        (128, 0, "And now, the adventure begins...\n\n\nCLICK SPACE TO START LEVEL 1!")
    ]
    nextseq = "one"
    bgcolor = 12
    boxcol1 = 5
    boxcol2 = 13


class PreBoss(BaseScene):
    "A scene where Diddi and Eli first meet the Scaler, who challenges them."
    scenes = [
        (0, 128, "After many challenges, Diddi\nand Eli have arrived to\nthe Scaler's fortress..."),
        (0, 128, "Eli: Oof! This has been tough!"),
        (0, 128, "Diddi: Shh! Someone's coming."),
        (128, 128, "... IT'S THE SCALER!!"),
        (256, 128, "Scaler: So... are you the\nlittle pesky bugs who wanted to\nchallenge me?"),
        (256, 128, "Scaler: If so, I'm sure you\ncould defeat my unlimited\npower in a battle..."),
        (256, 128, "Scaler: ... IF YOU DARE!"),
        (128, 128, "Diddi: We'll stop you!\n\nEli: Sure! You'll see!"),
        (256, 128, "Scaler: Ok then, try to\ncatch me and we'll fight!\n\nCLICK SPACE TO START LEVEL 5!")
    ]
    nextseq = "five"
    bgcolor = 0
    boxcol1 = 5
    boxcol2 = 6


class Final(BaseScene):
    "The ending scene of Diddi and Eli."
    scenes = [
        (0, 256, "At last, our heroes defeated\nthe Scaler and saved the\nplanet!"),
        (
            0,
            256,
            "Lady Alix: You did it, the\nScaler and his troops are now\n"
            "gone, and we're totally safe\nagain, thanks!"
        ),
        (0, 256, "Diddi and Eli: It's been a\npleasure to help..."),
        (
            128,
            256,
            "Lady Alix: Anyway, this will\ndeserve a day-long celebration!\n\nEli: Yeah!"),
        (256, 256, "=== THE END ===\nThanks for playing! <3\n\nPRESS SPACE TO SEE THE MENU")
    ]
    nextseq = "menu"
    bgcolor = 12
    boxcol1 = 5
    boxcol2 = 13
