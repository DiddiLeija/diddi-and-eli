"""
Submodule containing all the characters and their physics,
including the main players (Diddi, Eli), the mobs (onions,
slimehorns, robots, etc), coins, and NPCs.
"""

import pyxel

# === Tool functions (physics, data, etc)
# TODO: fixme!

# === Players ===


class Player1:
    """
    Diddi, Player 1, operated using WASD keys.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.initial_setup()
    
    def initial_setup(self):
        """
        Main variable configurations, which
        differentiate from Diddi and Eli.
        """
        self.key_up = pyxel.KEY_W
        self.key_left = pyxel.KEY_A
        self.key_bullet = pyxel.KEY_S
        self.key_right = pyxel.KEY_D
        self.imagebank = [
            (8, 0),   # Right, normal
            (16, 0),  # Right, walking (1)
            (24, 0),  # Right, walikng (2)
            (32, 0),  # Right, jumping
            (8, 8),   # Left, normal
            (16, 8),  # Left, walking (1)
            (24, 8),  # Left, walikng (2)
            (32, 8),  # Left, jumping
        ]
        self.icon = (0, 16)


class Player2(Player1):
    """
    Eli, Player 2, operated with arrow keys.
    
    NOTE: this class is inherited from Diddi
    (Player1) as it uses most of its structure.
    However, some variables have changed (see
    'Player2.initial_setup').
    """

    def initial_setup(self):
        """
        Main variable configurations, which
        differentiate from Diddi and Eli.
        """
        self.key_up = pyxel.KEY_UP
        self.key_left = pyxel.KEY_LEFT
        self.key_bullet = pyxel.KEY_DOWN
        self.key_right = pyxel.KEY_UP
        self.imagebank = [
            (8, 16),    # Right, normal
            (16, 16),   # Right, walking (1)
            (24, 16),   # Right, walikng (2)
            (32, 16),   # Right, jumping
            (8, 24),    # Left, normal
            (16, 24),   # Left, walking (1)
            (24, 24),   # Left, walikng (2)
            (32, 24),   # Left, jumping
        ]
        self.icon = (0, 24)


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
