"""
Submodule containing all the characters and their physics,
including the main players (Diddi, Eli), the mobs (onions,
slimehorns, robots, etc), coins, and NPCs.
"""

import pyxel

# === Players ===


class Player1:
    "Diddi, Player 1, operated using WASD keys."


class Player2:
    "Eli, Player 2, operated with arrow keys."


# === Mobs ===


class Onion:
    "Mobs who just walk but can fall from cliffs."

class Robot(Onion):
    "Mobs who walk, without falling from cliffs, making then harder to defeat."

class Slimehorn1:
    "Mobs that stick to a surface (Down)."
    variant = False

class Slimehorn2:
    "Mobs that stick to a surface (Up)."
    variant = False

class Slimehorn3:
    "Mobs that stick to a surface (Left)."
    variant = False

class Slimehorn4:
    "Mobs that stick to a surface (Right)."
    variant = False
