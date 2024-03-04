"Physics/graphics tools used across the source code."

import io
import json
import pyxel

def draw_text(text, x, y):
    pyxel.text(x, y, text, 1)
    pyxel.text(x+1, y, text, 7)

def init_class(obj, popt):
    return obj(popt)

def get_savedata():
    with io.open("savedata.json", "r") as js:
        return json.loads(js.read())

def write_savedata(data):
    with io.open("savedata.json", "w") as js:
        js.write(json.dumps(data, sort_keys=True, indent=4))
