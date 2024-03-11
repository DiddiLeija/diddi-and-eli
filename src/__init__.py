"Extra code/tools for the game."

from . import menu, levels, scenes

__all__ = ("stages_list")

# TODO: fixme -- these objects should be Python classes
Three = None  # levels.Three
Four = None  # levels.Four
Five = None  # levels.Five
# NOTE: Below I have the already-linked objects
Menu = menu.Menu
Intro = scenes.Intro
One = levels.One
Two = levels.Two

# Below there's a dictionary with all the objects for further use
stages_list = {
    "intro": Intro,
    "one": One,
    "two": Two,
    "three": Three,
    "four": Four,
    "preboss": None,  # TODO: A non-playable pre-boss sequence
    "five": Five,
    "final": None,  # TODO: A non-playable closing sequence
    "menu": Menu,
}
