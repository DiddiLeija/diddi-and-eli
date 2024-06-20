"Physics/graphics tools used across the source code."

import io
import json
import pyxel

POSSIBLE_LEVELS = (
    # a list of allowed level names.
    # NOTE: "menu" or "death" should not be allowed as a saved level.
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

def draw_text(text, x, y, *, maincol=7, subcol=1):
    "Draw a pretty text on the screen."
    pyxel.text(x, y, text, subcol)
    pyxel.text(x+1, y, text, maincol)

def init_class(obj, popt):
    "Initialize a class and return the object."
    # TODO: Find a better way to do this?
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

class InternalOperationCrash(Exception):
    """
    custom exception for internal errors with internal stuff
    that could only crash under testing circumstances.
    """

def report_crash(opname, original):
    raise InternalOperationCrash(
        f"Error: Internal operation '{opname}' showed unexpected behavior. "
        f"If you are not testing this operation, please report this error. ('{original}')"
    )

def gradient(height, skips):
    "Generate a list-of-lists needed to draw a gradient on the background."
    final = dict()
    for i in range(height):
        if i in skips:
            # this row should be skipped
            continue
        if i % 2 == 0:
            # variant 1
            final[128-i] = [0 + (2*op) for op in range(0, 65)]
        else:
            # variant 2
            final[128-i] = [1 + (2*op) for op in range(0, 65)]
    return final

def draw_gradient(grad, ini_x, ini_y, col):
    # draw a given gradient data.
    for k, v in grad.items():
        for vv in v:
            try:
                pyxel.pset((ini_x-1) + vv, ini_y + k, col)
            except Exception:
                pass  # this shouldn't happen anyway

def get_player_names(choice):
        "Get a proper text to refer to the player pack."
        ideas = ["Diddi", "Eli", "Diddi & Eli"]
        try:
            return ideas[choice]
        except (TypeError, IndexError, ValueError) as exc:
            report_crash(
                f"tools.get_player_names (player_choice = {choice})",
                str(exc)
            )

def draw_stats(x, y, player_selection, coins, level):
    "Draw a stats bar in the bottom of the screen."
    play_stats = False
    correct_s = ""
    for s in POSSIBLE_LEVELS:
        if s in level.lower():
            play_stats = True
            correct_s = s
            break
    pyxel.camera()
    pyxel.rect(0, 128, 128, 16, 0)
    pyxel.rect(0, 128, 128, 1, 7)
    if play_stats:
        draw_text(get_player_names(player_selection), 1, 129)
        draw_text(f"COINS {coins}  LEVEL {correct_s}", 1, 137)
    else:
        draw_text("... nothing to show by now...", 0, 137, maincol=13, subcol=1)
    pyxel.camera(x, y)
