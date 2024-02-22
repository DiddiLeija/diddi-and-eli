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

    def create_characters(self):
        # NOTE: No Player classes, please!
        pass

    def update_template(self):
        "update template function (called by 'any_subclass.update()')."
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sno += 1
            if self.sno >= len(self.scenes):
                self.finished = True
                return None
    
    def draw(self):
        "draw function."
        pyxel.cls(self.bgcolor)  # TODO: Should we respect self.bgcolor??
        st = self.scenes[self.sno]
        pyxel.bltm(0, 0, 2, st[0], st[1], 128, 128, 0)
        pyxel.rect(70, 0, 50, 128, self.boxcol1)
        pyxel.rect(69, 0, 1, 128, self.boxcol2)
        draw_text(st[2], 71, 1)
        draw_text(">>", 112, 120)
