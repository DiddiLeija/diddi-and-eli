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
from .tools import draw_text


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
        BaseLevel.__init__(self, player_choice)

    def create_characters(self):
        # NOTE: No Player classes, please!
        pass

    def update(self):
        "Pyxel-like 'update' function."
        self.check_quit()
        if self.check_reset():
            self.next = "menu"
        elif self.finished:
            self.next = self.nextseq
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sno += 1
            if self.sno >= len(self.scenes):
                self.finished = True
                self.next = self.nextseq
    
    def draw(self):
        "draw function."
        pyxel.cls(self.bgcolor)  # TODO: Should we respect self.bgcolor??
        st = self.scenes[self.sno]
        pyxel.bltm(0, 0, 2, st[0], st[1], 128, 128, 0)
        pyxel.rect(0, 80, 128, 50, self.boxcol1)
        pyxel.rect(0, 79, 128, 1, self.boxcol2)
        draw_text(st[2], 1, 81)
        draw_text(">>", 120, 120)


class Intro(BaseScene):
    "Intro sequence."
    scenes = [
        (0, 0, "Diddi and Eli are chatting\nwith Lady Alix, their boss..."),
        (0, 0, "Lady Alix: Hi, Diddi and Eli!\n\nDiddi and Eli: Hi!"),
        (0, 0, "Lady Alix: I need your help,\nfolks. Our enemy, THE SCALER,\nis coming to invade us."),
        (0, 0, "Lady Alix: If the Scaler finds\nus, we'll be doomed to total\ndestruction!"),
        (0, 0, "Diddi: We'll stop him!"),
        (0, 0, "Eli: Yeah! Let's go!"),
        (128, 0, "And now, the adventure begins...\n\n\nCLICK SPACE TO START LEVEL 1!")
    ]
    nextseq = "one"
    bgcolor = 12
    boxcol1 = 5
    boxcol2 = 13
