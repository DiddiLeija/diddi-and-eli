"Extra code/tools for the game."

from . import menu, levels, scenes

__all__ = ("stages_list")

# Below there's a dictionary with all the objects for further use
stages_list = {
    "intro": scenes.Intro,
    "one": levels.One,
    "two": levels.Two,
    "three": None,  # TODO - level 3
    "four": None,  # TODO - level 4
    "preboss": scenes.PreBoss,
    "five": None,  # TODO - level 5/final
    "final": scenes.Final,
    "menu": menu.Menu,
}
