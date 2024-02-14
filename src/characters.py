"""
Submodule containing all the characters and their physics,
including the main players (Diddi, Eli), the mobs (onions,
slimehorns, robots, etc), coins, and NPCs.
"""

# Some of the functions/protocols were borrowed from
# another project of mine, "Abandon the ship!", which
# is based in Pyxel example #10, "Platformer".
# 
# To be honest, "Diddi and Eli" can be considered a spiritual
# successor to "Abandon the ship!"...
#
# TODO: Get sure everything here can be invoked
#       from the level classes. Otherwise, will we
#       have to adapt the player's code, or even come
#       up with a different solution???

import random
import math

from abc import ABC, abstractmethod

import pyxel

# === Tool functions (physics, data, etc) ===

__all__ = (
    "Player1",
    "Player2",
    "Onion",
    "Robot",
    "Slimehorn1",
    "Slimehorn2",
    "Slimehorn3",
    "Slimehorn4",
    "Bullet",
    "Coin",
    "BaseLevel"
)

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
    (48, 16),  # Box 1
    (48, 24),  # Box 2
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
Y_LEVEL = 0

def adjust_x(real_x):
    return scroll_x + real_x

def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[1].pget(tile_x, Y_LEVEL + tile_y)

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
        self.jumping = False
        self.active = False
        global scroll_x
        scroll_x = 0
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

    def check_bullets(self):
        "Control bullets."
        kills = list()
        for i in range(len(self.bullets)):
            if not self.bullets[i].alive:
                kills.append(i)
        try:
            for k in kills.sort(reverse=True):
                self.bullets.pop(k)
        except TypeError:
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
                self.bullets.append(Bullet(self.x+6, self.y+3))
            else:
                # Send a bullet to the left
                self.bullets.append(Bullet(self.x, self.y+3, False))
        if pyxel.btn(self.key_left):
            # Move to the left
            self.dx = -2
            self.r_facing = False
        elif pyxel.btn(self.key_right):
            # Move to the right
            self.dx = 2
            self.r_facing = True
        self.dy = min(self.dy + 1, 3)
        if pyxel.btnp(self.key_up) and not self.is_falling and self.dy != -8:
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
        if self.y >= 120:
            # We fell down!
            self.alive = False
        if not self.alive:
            pyxel.playm(6)

    def draw(self):
        "Draw the character."
        if self.alive:
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
        self.key_right = pyxel.KEY_RIGHT
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

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.alive = True

    def update(self):
        pass

    def draw(self):
        pass

class Onion(BaseMob):
    "Mobs that just walk but can fall from cliffs."
    direction = -1

    def update(self):
        self.dx = self.direction
        if self.direction < 0 and is_wall(self.x - 1, self.y + 4):
            self.direction = 1
        elif self.direction > 0 and is_wall(self.x + 8, self.y + 4):
            self.direction = -1
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)

    def draw(self):
        u = 16 if self.direction < 0 else 24
        v = random.choice([48, 56])
        pyxel.blt(self.x, self.y, 0, u, v, 8, 8, 0)

class Robot(BaseMob):
    "Mobs that walk, without falling from cliffs, making then harder to defeat."
    direction = -1

    def update(self):
        self.dx = self.direction
        if is_wall(self.x, self.y + 8) or is_wall(self.x + 7, self.y + 8):
            if self.direction < 0 and (
                is_wall(self.x - 1, self.y + 4) or not is_wall(self.x - 1, self.y + 8)
            ):
                self.direction = 1
            elif self.direction > 0 and (
                is_wall(self.x + 8, self.y + 4) or not is_wall(self.x + 7, self.y + 8)
            ):
                self.direction = -1
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)

    def draw(self):
        u = 0 if self.direction < 0 else 8
        v = random.choice([48, 56])
        pyxel.blt(self.x, self.y, 0, u, v, 8, 8, 0)

class SlimehornBase(BaseMob):
    "Base class for slimehorns (see below)."
    imgs = [tuple(), tuple()]

    def __init__(self, x, y, variant=False):
        self.x = self.x
        self.y = y
        self.variant = variant

    def update(self):
        # TODO: By now, Slimehorns won't move.
        #       Let's try to give them some action
        #       in a future version!
        pass

    def draw(self):
        if not self.alive:
            return
        combo = self.imgs[0] if self.variant else self.imgs[1]
        pyxel.blt(self.x, self.y, 0, combo[0], combo[2], 8, 8, 0)

class Slimehorn1(SlimehornBase):
    "Mobs that stick to a surface (Down)."
    imgs = [(32, 48), (48, 48)]

class Slimehorn2(SlimehornBase):
    "Mobs that stick to a surface (Up)."
    imgs = [(32, 56), (48, 56)]

class Slimehorn3(SlimehornBase):
    "Mobs that stick to a surface (Left)."
    imgs = [(40, 48), (56, 48)]

class Slimehorn4(SlimehornBase):
    "Mobs that stick to a surface (Right)."
    imgs = [(40, 56), (56, 56)]


# === Coins/bullets ===


class Bullet:
    "A bullet sent by either Diddi or Eli, which may damage enemies."
    alive = False

    def __init__(self, x, y, r_facing=True):
        self.x = x
        self.y = y
        self.r_facing = r_facing
        self.alive = True

    def update(self):
        if not self.alive:
            return
        if self.r_facing:
            self.x += 3
        else:
            self.x -= 3

    def draw(self):
        if not self.alive:
            return
        pyxel.rect(self.x, self.y, 4, 2, 11)


class Coin:
    "A coin that gives you points to brag about."
    alive = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def update(self):
        # We won't do anything at all here!
        pass

    def draw(self):
        if not self.alive:
            pass
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)


# === Base level (removed from troubled 'src.baseclasses') ===

class BaseLevel(ABC):
    "Base level."
    # tilemap = 0
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    player = list()  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    next = ""  # Where should we go after finishing
    lost = False  # Did we die??
    enemy_templates = dict()  # Coordinates to spawn enemies, unique for each subclass
    enemies = list()  # The list with enemies/mobs
    draw_v = 0  # The 'v' parameter used in 'pyxel.bltm', during level drawing
    music_vol = 0

    def __init__(self, player_choice):
        pyxel.camera(0, 0)
        self.player_choice = player_choice
        self.create_characters()
        global Y_LEVEL
        Y_LEVEL = self.draw_v
        self.spawn(0, 128)
        pyxel.playm(self.music_vol, loop=True)

    def startup(self):
        self.create_characters()
        pyxel.playm(self.music_vol, loop=True)

    def check_quit(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def check_reset(self) -> bool:
        if pyxel.btnp(pyxel.KEY_R):
            self.finished = True
            self.next = "menu"
            return True
        return False

    def check_anyone_alive(self) -> bool:
        for p in self.player:
            if p.alive:
                return True
        return False

    def create_characters(self):
        if self.player_choice == 0:
            self.player = [Player1(0, 0)]
        elif self.player_choice == 1:
            self.player = [Player2(0, 0)]
        elif self.player_choice == 2:
            self.player = [Player1(0, 0), Player2(0, 10)]

    def spawn(self, left_x, right_x):
        left_x = math.ceil(left_x / 8)
        right_x = math.floor(right_x / 8)
        for x in range(left_x, right_x + 1):
            for y in range(16):
                key = f"{x*8} {y*8}"
                if key in self.enemy_template.keys():
                    mobclass = self.enemy_template[key]
                    self.enemies.append(mobclass(x * 8, y * 8))
                    # print(f"Added {mobclass}")

    def update_template(self):
        "Some update actions that should happen in (almost) every instance."
        for p in self.player:
            p.update()
            for b in p.bullets:
                b.update()
                for e in self.enemies:
                    if b.x in range(e.x, e.x+9) and b.y in range(e.y, e.y+9):
                        e.alive = False
            for e in self.enemies:
                if e.alive:
                    if e.x in range(p.x, p.x+9) and e.y in range(p.y, p.y+9):
                        p.alive = False
        if not self.check_anyone_alive():
            self.lost = True
            self.finished = True
            self.startup()
            pyxel.playm(6)
            self.next = "menu"
            return
        for e in self.enemies:
            e.update()
        player_x = self.player[0].x
        # NOTE: turns out this portion of code is never executed!?
        #if player_x > scroll_x + SCROLL_BORDER_X:
        #    # Move the screen if needed
        #    last_scroll_x = scroll_x
        #    self.scroll_x = min(self.x - self.SCROLL_BORDER_X, 240 * 8)
        #    self.spawn(last_scroll_x + 128, scroll_x + 127)
        self.spawn(scroll_x, scroll_x + 127)

    def draw_template(self):
        "Some drawing actions that should happen in (almost) every instance."
        pyxel.cls(0)
        if self.check_anyone_alive():
            pyxel.camera()
            pyxel.bltm(0, 0, 1, scroll_x, self.draw_v, 128, 128, 0)
            pyxel.camera(scroll_x, 0)  # test: self.draw_v or 0?
            for p in self.player:
                p.draw()
                for b in p.bullets:
                    b.draw()
            for i in self.enemies:
                i.draw()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
