"""
Submodule containing all the characters and their physics,
including the main players (Diddi, Eli), the mobs (onions,
slimehorns, robots, etc), coins, and NPCs.
"""

import random

import pyxel

# === Tool functions (physics, data, etc)
# (Some of these were borrowed from another
# project of mine, 'abandon-the-ship')

# TODO: Verify these functions can be invoked
#       from the level classes. Otherwise, we'll
#       have to adapt the player's code or come
#       up with a different solution.

SCROLL_BORDER_X = 80
WALL_TILE_X = 4
TILES_FLOOR = [
    (40, 0),   # Grass - Up
    (40, 8),   # Grass - Down
    (48, 0),   # Ice - Up
    (48, 8),   # Ice - Down
    (56, 0),   # Purple bricks
    (56, 8),   # Red bricks
    (40, 16),  # Sand - Up
    (40, 24),  # Sand - Down
    (48, 16),  # White struct 1
    (48, 24),  # White struct 2
    (56, 16),  # Dirt - Up
    (56, 24),  # Dirt - Down
    (0, 64),   # Gate (L, 1)
    (0, 72),   # Gate (L, 2)
    (8, 64),   # Gate (R, 1)
    (8, 72),   # Gate (R, 2)
    (56, 64),  # Button support (H)
    (56, 72),  # Button support (v)
]
scroll_x = 0

def adjust_x(real_x):
    return scroll_x + real_x


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(1).pget(tile_x, tile_y)


def detect_collision(x, y, dy):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) in TILES_FLOOR:
                return True
    return False

# === Players ===


class Player1:
    """
    Diddi, Player 1, operated using WASD keys.
    """
    alive = True

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.prev_x = self.x
        self.prev_y = self.y
        self.r_facing = True
        self.shoot = False
        self.is_falling = False
        self.active = False
        self.initial_setup()

    def initial_setup(self):
        """
        Main variable configurations, which
        differentiate between Diddi and Eli.
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
    
    def get_image_combo(self):
        if self.r_facing:
            # Our player is facing to the right
            if self.is_falling or self.prev_y > self.y:
                # Jumping/falling
                return self.imagebank[3]
            if self.prev_x == self.x:
                # We're static
                return self.imagebank[0]
            # We're walking
            return random.choice(self.imagebank[1:3])
        else:
            # Our player is left-facing
            if self.is_falling or self.prev_y > self.y:
                # Jumping/falling
                return self.imagebank[7]
            if self.prev_x == self.x:
                # We're static
                return self.imagebank[4]
            # We're walking
            return random.choice(self.imagebank[5:7])

    def update(self):
        "Update and react to key controls."
        if pyxel.btnp(self.key_bullet):
            # TODO: fixme!
            pass
        if pyxel.btnp(self.key_left):
            # TODO: fixme!
            self.r_facing = False
        elif pyxel.btnp(self.key_right):
            # TODO: fixme!
            self.r_facing = True
    
    def draw(self):
        "Draw the character."
        combo = self.get_image_combo()
        pyxel.blt(self.x, self.y, 0, combo[0], combo[1], 8, 8, 0)


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
        differentiate between Diddi and Eli.
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
