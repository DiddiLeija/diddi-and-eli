"Physics/graphics tools used across the source code."

import pyxel

def draw_text(text, x, y):
    pyxel.text(x, y, text, 1)
    pyxel.text(x+1, y, text, 7)
