"Extra code/tools for the game."

from . import menu, levels, scenes

__all__ = "stages_list"

# Below there's a dictionary with all the objects for further use
stages_list = {
    "intro": scenes.Intro,
    "one": levels.One,
    "two": levels.Two,
    "three": levels.Three,
    "four": levels.Four,
    "preboss": scenes.PreBoss,
    "five": levels.Five,
    "final": scenes.Final,
    "menu": menu.Menu,
    "death": scenes.DeathSequence,
}
