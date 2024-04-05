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
WALL_TILE_X = 5
TILES_FLOOR = [
    (5, 0),  # Grass - Up
    (5, 1),  # Grass - Down
    (6, 0),  # Ice - Up
    (6, 1),  # Ice - Down
    (7, 0),  # Purple bricks
    (7, 1),  # Red bricks
    (5, 2),  # Sand - Up
    (5, 3),  # Sand - Down
    (6, 2),  # Box - 1
    (6, 3),  # Box - 2
    (7, 2),  # Dirt - Up
    (7, 3),  # Dirt - Down
    (0, 8),  # Gate (L, 1)
    (0, 9),  # Gate (L, 2)
    (1, 8),  # Gate (R, 1)
    (1, 9),  # Gate (R, 2)
    (7, 8),  # Button support (h)
    (7, 9),  # Button support (v)
]
scroll_x = 0
TOTAL_COINS = 0

def adjust_x(real_x):
    return scroll_x + real_x

def get_tile(tile_x, tile_y):
    # print(tile_x, tile_y)
    return pyxel.tilemaps[1].pget(tile_x, tile_y)

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
    # TODO: We have to fix this function to make it work on
    #       level 2 and above, there's currently a bug with that.
    # (Update: arg 'yzero' should make this possible)
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
    already_jumping = False

    def __init__(self, x=0, y=0, yzero=0):
        self.x = x
        self.y = y
        self.yzero = yzero
        self.dx = 0
        self.dy = 0
        self.prev_x = self.x
        self.prev_y = self.y
        self.r_facing = True
        self.shoot = False
        self.is_falling = False
        self.jumping = False
        self.active = False
        self.bullets = list()
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
        if pyxel.btnp(self.key_up) and not self.is_falling and not self.already_jumping:
            # Jump (instead of the fly-ish mechanics from previous games)
            self.dy = -8  # TODO: Adjust this in order to achieve realistic jumps
            self.already_jumping = True
        # Now operate the movement
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < self.yzero:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > self.prev_y
        self.already_jumping = self.prev_y > self.y
        # And finally, move the screen forward if needed
        if self.x > scroll_x + SCROLL_BORDER_X:
            # The 'scroll_x' stuff is located here, but may also happen
            # in 'Player2.update' in either Eli-mode or multiplayer mode.
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)
        if self.y >= (self.yzero + 120):
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

    def __init__(self, x, y, yzero=0):
        self.x = x
        self.y = y
        self.yzero = yzero
        self.dx = 0
        self.dy = 0
        self.alive = True

    def update(self):
        pass

    def draw(self):
        if self.alive:
            self.draw_template()
    
    def draw_template(self):
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
        self.dy = min(self.dy + 1, 3)
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.y >= (self.yzero + 120):
            self.alive = False

    def draw_template(self):
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
        self.dy = min(self.dy + 1, 3)
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        # NOTE: Unlke Onions, here we are not adding a "pitfall detector" here, because
        # in theory Robots never fall from platforms and reach y >= 120.

    def draw_template(self):
        u = 0 if self.direction < 0 else 8
        v = random.choice([48, 56])
        pyxel.blt(self.x, self.y, 0, u, v, 8, 8, 0)

class SlimehornBase(BaseMob):
    "Base class for slimehorns (see below)."
    imgs = [tuple(), tuple()]

    def __init__(self, x, y, yzero=None, variant=False):
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
            return
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)

# === Clouds ===

class Cloud:
    "A sprite that's drawn in the background, usually representing clouds or smoke."
    alive = False

    def __init__(self, x, y, draw_x, draw_y):
        self.x = x
        self.y = y
        self.draw_x = draw_x
        self.draw_y = draw_y
        self.alive = True
        self.speed = random.randint(2, 3)
    
    def update(self):
        self.x -= self.speed
        if self.x <= 0:
            self.alive = False
    
    def draw(self):
        if not self.alive:
            return
        # NOTE: Clouds are all stored at resource image 1, take that in count!
        pyxel.blt(self.x, self.y, 1, self.draw_x, self.draw_y, 16, 16, 0)

# === Button ===

class Button:
    """
    Buttons are a special and invisible NPCs whose function is to "mark"
    the end of a level. Once a player touches a button, the level will end.

    NOTE: We don't draw buttons because they're already drawn at the tilemap!
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        pass

    def draw(self):
        pass


# === Base level (removed from troubled 'src.baseclasses') ===

class BaseLevel(ABC):
    "Base level."
    # tilemap = 0
    player_choice = 0  # 0 is Diddi, 1 is Eli, and 2 is multiplayer
    player = list()  # Amount of players involved
    finished = False  # Have we finished today? Can we go home now?
    nextlevel = ""  # Where should we go after finishing, previously named "BaseLevel.next"
    lost = False  # Did we die??
    enemy_template = dict()  # Coordinates to spawn enemies, unique for each subclass
    coin_template = list()  # Coordinates to spawn coins, unique for each subclass
    already_spawned = list()  # List of already-spawned coordinates (mobs, coins, npcs, etc)
    enemies = list()  # The list with enemies/mobs
    coins = list()  # The list of coins
    draw_v = 0  # The 'v' parameter used in 'pyxel.bltm', during level drawing
    music_vol = 0
    reset_coin_counter = False  # False by default, should be True for Menu instances
    bgcolor = 0  # Customizable background color, set to 0 by default
    gen_clouds = True  # Shall we add some clouds to the background?
    acceptable_clouds = list()  # A list of cloud coordinates that may be used (if gen_louds=True)
    clouds = list()  # list of clouds
    cloud_freq = 25  # the greater this number is, the less the chances to spawn a cloud
    already_spawned_cloud = 0
    button_location = ""  # a string representing the coordinates of the "ending button" location
    ending_button = None  # the ending button object
    finished_next = ""  # next sequence in case a level ends succesfully

    def __init__(self, player_choice):
        pyxel.camera(0, 0)
        self.player_choice = player_choice
        self.already_spawned = list()
        self.enemies = list()
        self.coins = list()
        self.clouds = list()
        self.already_spawned_cloud = 0
        self.generate_clouds(128)
        self.create_characters()
        global TOTAL_COINS
        if self.reset_coin_counter:
            TOTAL_COINS = 0
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
            self.nextlevel = "menu"
            return True
        return False

    def check_anyone_alive(self) -> bool:
        for p in self.player:
            if p.alive:
                return True
        return False

    def create_characters(self):
        if self.player_choice == 0:
            self.player = [Player1(0, self.draw_v, self.draw_v)]
        elif self.player_choice == 1:
            self.player = [Player2(0, self.draw_v, self.draw_v)]
        elif self.player_choice == 2:
            self.player = [
                Player1(0, self.draw_v, self.draw_v),
                Player2(0, self.draw_v + 10, self.draw_v)
            ]

    def spawn(self, left_x, right_x):
        left_x = math.ceil(left_x / 8)
        right_x = math.floor(right_x / 8)
        for x in range(left_x, right_x + 1):
            for y in range(16):
                key = f"{x*8} {y*8}"
                if key in self.already_spawned:
                    continue
                if key in self.enemy_template.keys():
                    mobclass = self.enemy_template[key]
                    self.enemies.append(mobclass(x * 8, y * 8, self.draw_v))
                    self.already_spawned.append(key)
                if key in self.coin_template:
                    self.coins.append(Coin(x * 8, y * 8))
                    self.already_spawned.append(key)
                if key == self.button_location:
                    self.ending_button = Button(x * 8, y * 8)

    def generate_clouds(self, right_x):
        # TODO: Group all the "if ...: return" blocks found here?
        if not self.gen_clouds:
            return
        if (right_x in range(self.already_spawned_cloud+1, self.already_spawned_cloud+16)):
            return
        if random.randint(0, self.cloud_freq) != 1:
            return
        draw_comb = random.choice(self.acceptable_clouds)
        self.clouds.append(Cloud(right_x, random.randint(0, 80), draw_comb[0], draw_comb[1]))
        self.already_spawned_cloud = right_x

    def update_template(self):
        "Some update actions that should happen in (almost) every instance."
        global TOTAL_COINS
        for i in self.clouds:
            # this is a rutinary task, so we don't need to give it conditions.
            i.update()
        for p in self.player:
            p.update()
            for c in self.coins:
                c.update()
                if c.x in range(p.x-4, p.x+8) and c.y in range(p.y-4, p.y+8) and c.alive:
                        TOTAL_COINS += 1
                        c.alive = False
            for b in p.bullets:
                b.update()
                for e in self.enemies:
                    if not e.alive:
                        continue
                    if b.x in range(e.x-4, e.x+8) and b.y in range(e.y-4, e.y+8):
                        e.alive = False
                        b.alive = False
                        break
            for e in self.enemies:
                if e.alive:
                    if e.x in range(p.x-4, p.x+8) and e.y in range(p.y-4, p.y+8):
                        p.alive = False
            if p.alive and self.ending_button is not None:
                if self.ending_button.x in range(p.x-4, p.x+8):
                    if self.ending_button.y in range(p.y-4, p.y+8):
                        self.finished = True
                        break
        if not self.check_anyone_alive():
            self.lost = True
            self.finished = True
            self.startup()
            pyxel.playm(6)
            self.nextlevel = "menu"
            return
        for e in self.enemies:
            e.update()
        self.spawn(scroll_x, scroll_x + 127)
        if self.gen_clouds:
            self.generate_clouds(scroll_x + 127)

    def draw_template(self):
        "Some drawing actions that should happen in (almost) every instance."
        pyxel.cls(self.bgcolor)
        if self.check_anyone_alive():
            pyxel.camera()
            for i in self.clouds:
                # we've put this block right before the bakground drawing, to avoid clouds
                # to be in front of the scenario, which would be catastrophic :)
                i.draw()
            pyxel.bltm(0, 0, 1, scroll_x, self.draw_v, 128, 128, 0)
            pyxel.camera(scroll_x, 0)
            for p in self.player:
                p.draw()
                for b in p.bullets:
                    b.draw()
            for i in self.enemies:
                i.draw()
            for i in self.coins:
                i.draw()

    def update(self):
        "Update function."
        # NOTE: some levels/scenes may override this function.
        self.check_quit()
        if self.check_reset():
            self.nextlevel = "menu"
            return
        if self.finished:
            self.nextlevel = self.finished_next
            return
        self.update_template()

    @abstractmethod
    def draw(self):
        pass
