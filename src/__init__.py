"Extra code/tools for the game."

from . import menu  # , one, two, three, four, five, six

__all__ = ("stages_list")

# TODO: fixme -- these objects should be Python classes
One = None  # one.One
Two = None  # two.Two
Three = None  # three.Three
Four = None  # four.Four
Five = None  # five.Five
Six = None  # six.Six
# NOTE: Below I have the already-linked objects
Menu = menu.Menu

# Below there's a dictionary with all the objects for further use
stages_list = {
    "one": One,
    "two": Two,
    "three": Three,
    "four": Four,
    "five": Five,
    "six": Six,
    "menu": Menu,
}
