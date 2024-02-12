"Extra code/tools for the game."

from . import menu, levels

__all__ = ("stages_list")

# TODO: fixme -- these objects should be Python classes
Two = None  # two.Two
Three = None  # three.Three
Four = None  # four.Four
Five = None  # five.Five
# NOTE: Below I have the already-linked objects
Menu = menu.Menu
One = levels.One

# Below there's a dictionary with all the objects for further use
stages_list = {
    "intro": None,  # TODO: A non-playable intro sequence
    "one": One,
    "two": Two,
    "three": Three,
    "four": Four,
    "preboss": None,  # TODO: A non-playable pre-boss sequence
    "five": Five,
    "final": None,  # TODO: A non-playable closing sequence
    "menu": Menu,
}
