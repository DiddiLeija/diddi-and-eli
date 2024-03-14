"Physics/graphics tools used across the source code."

import io
import json
import pyxel

POSSIBLE_LEVELS = (
    # a list of allowed level names.
    # NOTE: apparently "menu" should not be allowed as a saved level.
    "intro",
    "one",
    "two",
    "three",
    "four",
    "preboss",
    "five",
    "final"
)

def check_savedata(data):
    "Internal function to avoid warped/incorrect save data."
    if data["level"] not in POSSIBLE_LEVELS:
        data["level"] = "intro"
    return data

def draw_text(text, x, y):
    "Draw a pretty text on the screen."
    pyxel.text(x, y, text, 1)
    pyxel.text(x+1, y, text, 7)

def init_class(obj, popt):
    "Initialize a class and return the object."
    return obj(popt)

def get_savedata():
    "Read and return the save data."
    with io.open("savedata.json", "r") as js:
        load = json.loads(js.read())
        return check_savedata(load)

def write_savedata(data):
    "Write the save data from scratch."
    with io.open("savedata.json", "w") as js:
        new_data = check_savedata(data)
        js.write(json.dumps(new_data, sort_keys=True))
