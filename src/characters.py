"""
Submodule containing all the characters and their physics,
including the main players (Diddi, Eli), the mobs (onions,
slimehorns, robots, etc), coins, and NPCs.
"""
# (Some of the functions/protocols were borrowed from
#  another project of mine, 'abandon-the-ship')
#
# TODO: Get sure everything here can be invoked
#       from the level classes. Otherwise, will we
#       have to adapt the player's code, or even come
#       up with a different solution???

import random

import pyxel

# === Tool functions (physics, data, etc)

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

def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile in TILES_FLOOR or tile[0] >= WALL_TILE_X

def push_back(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
    return x, y, dx, dy

# === Players ===


class Player1:
    """
    Diddi, Player 1, operated using WASD keys.
    """
    alive = True
    bullets = []

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
    
    def get_scroll_x(self):
        """
        This is just a 'bridge' between a player class and a
        level class, where 'scroll_x' is vital but not directly present.
        """
        return scroll_x
    
    def check_bullets(self):
        for i in self.bullets:
            if not i.alive:
                # TODO: Kill this object
                pass

    def update(self):
        "Update and react to key controls."
        self.check_bullets()
        if not self.alive:
            # NOTE: Why not putting 'self.check_bullets' after this block?
            #       Well, what if, during multiplayer mode, one of the character
            #       shoots a bullet and dies before such bullets finish their journey?
            return
        global scroll_x
        self.prev_y = self.y
        if pyxel.btnp(self.key_bullet):
            if self.r_facing:
                # Send a bullet to the right
                self.bullets.append(Bullet(self.x, self.y))
            else:
                # Send a bullet to the left
                self.bullets.append(Bullet(self.x, self.y, False))
        if pyxel.btnp(self.key_left):
            # Move to the left
            self.dx = -2
            self.r_facing = False
        elif pyxel.btnp(self.key_right):
            # Move to the right
            self.dx = 2
            self.r_facing = True
        self.dy = min(self.dy + 1, 3)
        if pyxel.btnp(self.key_up) and not self.is_falling:
            # Jump (instead of the fly-ish mechanics from previous games)
            self.dy = -8  # TODO: Adjust this in order to achieve realistic jumps
        # Now operate the movement
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > self.prev_y
        # And finally, move the screen forward if needed
        if self.x > scroll_x + SCROLL_BORDER_X:
            # The 'scroll_x' stuff is located here, but may also happen
            # in 'Player2.update' in either Eli-mode or multiplayer mode.
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)
    
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


class BaseMob:
    "Simple base for all the mobs."
    alive = False

class Onion(BaseMob):
    "Mobs who just walk but can fall from cliffs."

class Robot(Onion):
    "Mobs who walk, without falling from cliffs, making then harder to defeat."

class Slimehorn1(BaseMob):
    "Mobs that stick to a surface (Down)."
    variant = False

class Slimehorn2(BaseMob):
    "Mobs that stick to a surface (Up)."
    variant = False

class Slimehorn3(BaseMob):
    "Mobs that stick to a surface (Left)."
    variant = False

class Slimehorn4(BaseMob):
    "Mobs that stick to a surface (Right)."
    variant = False


# === Coins/bullets ===


class Bullet:
    "A bullet send by either Diddi or Eli and may damage enemies."
    alive = False

class Coin:
    "A coin that gives you points to brag about."
    alive = False
