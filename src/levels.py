"Library containing all the level classes, which honestly are pretty simple."


from .characters import (
    BaseLevel,
    Onion,
    Robot,
    Button
)


class TestLevel(BaseLevel):
    # Test level for checking world textures/behavior.
    gen_clouds = False
    draw_v = 640

    def update(self):
        self.check_quit()
        if self.check_reset():
            self.nextlevel = "menu"
        elif self.finished:
            self.nextlevel = "menu"
        self.update_template()
    
    def draw(self):
        if self.finished:
            return None
        self.draw_template()


class One(BaseLevel):
    """
    Level One: Onion Plateau

    A mostly plain, onion-filled plateau. It's the
    easiest level in the game, so it doesn't contain
    a lot of enemies or tricky spots.

    Mobs (9): Onions (7), Robots (2)
    """
    enemy_template = {
        "120 88": Onion,
        "264 80": Onion,
        "408 64": Onion,
        "424 48": Onion,
        "566 40": Onion,
        "604 40": Onion,
        "632 0": Onion,
        "696 56": Onion,
        "760 32": Robot,
        "912 48": Robot
    }
    coin_template = [
        "32 80",
        "40 80",
        "48 80",
        "80 72",
        "88 72",
        "96 72",
        "160 48",
        "160 56",
        "168 48",
        "168 56",
        "280 56",
        "288 48",
        "296 48",
        "304 56",
        "400 64",
        "408 56",
        "416 48",
        "424 40",
        "424 24",
        "432 48",
        "440 56",
        "448 64",
        "452 32",
        "528 32",
        "536 32",
        "544 32",
        "624 40",
        "632 40",
        "824 24",
        "832 32",
        "840 40",
        "848 48",
        "856 56"
    ]
    bgcolor = 12
    acceptable_clouds = [
        (0, 0),
        (0, 0),  # Augment the chances of getting a big cloud ;)
        (16, 0)
    ]
    ending_button = Button(1064, 96)
    finished_next = "two"
    # this is a workaround to <https://github.com/DiddiLeija/diddi-and-eli/issues/5>
    # NOTE: The same workaround is present in all the levels stored here...
    # TODO: Safely remove this workaround at some point?
    nextlevel = "two"
    
    def draw(self):
        "pyxel-like 'update' function."
        if self.finished:
            return None
        self.draw_template()


class Two(BaseLevel):
    """
    Level Two: Mud Caves

    A complex set of interconnected caves with trickier
    spots and a bit more enemies.

    Mobs (12): Onions (6), Robots (6).
    """
    draw_v = 128
    enemy_template = {
        "160 184": Onion,
        "184 184": Onion,
        "280 232": Robot,
        "320 232": Robot,
        "448 160": Robot,
        "544 200": Onion,
        "737 200": Robot,
        "872 176": Onion,
        "928 176": Robot,
        "952 176": Robot,
        "1072 216": Onion,
        "1088 216": Onion,
        "1104 216": Onion
    }
    coin_template = [
        "48 200",
        "64 208",
        "80 216",
        "96 224",
        "248 200",
        "256 200",
        "264 200",
        "280 176",
        "288 176",
        "196 176",
        "312 152",
        "320 152",
        "328 152",
        "448 152",
        "456 152",
        "464 152",
        "482 152",
        "490 152",
        "528 208",
        "536 200",
        "544 192",
        "552 200",
        "560 208",
        "720 184",
        "720 192",
        "728 184",
        "728 192",
        "784 168",
        "784 176",
        "792 168",
        "792 176",
        "984 168",
        "992 160",
        "1000 152",
        "1008 160"
    ]
    bgcolor = 12  # TODO: we want color 1, but that may conflict with Diddi and Eli's colors
    acceptable_clouds = [(16, 16)]  # Only one kind of clouds
    ending_button = Button(1192, 192)
    finished_next = "three"
    nextlevel = "three"
    
    def draw(self):
        "Pyxel-like 'update' function."
        if self.finished:
            return None
        self.draw_template()


class Three(BaseLevel):
    """
    Level Three: Dusty Desert

    A challenging desertic highlands, with a
    cave, harder jumps and more enemies.

    Mobs (): Onions (), Robots (), Desert Slimehorns ().
    """
    draw_v = 192
    enemy_template = {}  # TODO: fixme!
    coin_template = []  # TODO: fixme!
    bgcolor = 14
    acceptable_clouds = [(32, 0)]
    finished_next = "four"
    nextlevel = "four"

    def draw(self):
        "Pyxel-like 'update' function."
        if self.finished:
            return None
        self.draw_template()
