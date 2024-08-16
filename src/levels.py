"Library containing all the level classes, which honestly are pretty simple."

from .characters import BaseLevel, Onion, Robot, Button, Slimehorn1, Slimehorn2


class TestLevel(BaseLevel):
    # Test level for checking full world textures/behavior.
    gen_clouds = False
    draw_v = 640

    def update(self):
        self.check_quit()
        if self.check_reset():
            self.nextlevel = "menu"
        elif self.finished:
            self.nextlevel = "menu"
        self.update_template()


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
        "912 48": Robot,
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
        "856 56",
    ]
    bgcolor = 12
    acceptable_clouds = [
        (0, 0),
        (0, 0),  # Augment the chances of getting a big cloud ;)
        (16, 0),
    ]
    ending_button = Button(1064, 96)
    finished_next = "two"
    # this is a workaround to <https://github.com/DiddiLeija/diddi-and-eli/issues/5>
    # NOTE: The same workaround is present in all the levels stored here...
    # TODO: Safely remove this workaround at some point?
    nextlevel = "two"
    use_gradient = True
    gradient_height = 16
    gradient_color = 6
    gradient_skips = [15, 14, 12, 11, 9, 8, 6, 5, 3, 2]


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
        "1104 216": Onion,
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
        "296 176",
        "312 152",
        "320 152",
        "328 152",
        "448 152",
        "456 152",
        "464 152",
        "472 152",
        "480 152",
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
        "1008 160",
    ]
    bgcolor = 5
    acceptable_clouds = [(16, 16)]  # Only one kind of clouds
    ending_button = Button(1192, 192)
    finished_next = "three"
    nextlevel = "three"
    use_gradient = True
    gradient_color = 1
    gradient_height = 129


class Three(BaseLevel):
    """
    Level Three: Dusty Desert

    A challenging desertic highlands, with a
    cave, harder jumps and more enemies.

    Mobs (16): Onions (6), Robots (3), Desert Slimehorns (7).
    """

    draw_v = 256
    enemy_template = {
        "104 320": Onion,
        "120 304": Onion,
        "176 288": Onion,
        "232 288": Slimehorn2,
        "368 312": Robot,
        "456 280": Slimehorn1,
        "456 296": Robot,
        "544 272": Slimehorn1,
        "616 320": Robot,
        "656 272": Slimehorn1,
        "664 272": Slimehorn1,
        "752 352": Onion,
        "968 328": Onion,
        "1120 312": Slimehorn1,
        "1144 328": Slimehorn1,
        "1360 312": Onion,
    }
    coin_template = [
        "168 336",
        "168 344",
        "176 336",
        "176 344",
        "192 272",
        "208 272",
        "224 272",
        "240 272",
        "272 296",
        "288 304",
        "304 312",
        "328 304",
        "336 296",
        "344 288",
        "456 288",
        "504 280",
        "504 288",
        "512 280",
        "512 288",
        "568 280",
        "568 288",
        "576 280",
        "576 288",
        "616 304",
        "616 312",
        "624 304",
        "624 312",
        "712 336",
        "712 344",
        "720 336",
        "720 344",
        "728 336",
        "728 344",
        "736 336",
        "736 344",
        "848 344",
        "856 336",
        "864 344",
        "1024 344",
        "1032 336",
        "1040 344",
        "1104 264",
        "1104 280",
        "1128 296",
        "1128 328",
        "1136 256",
        "1136 304",
        "1136 320",
        "1160 256",
        "1176 256",
        "1272 304",
        "1280 296",
        "1288 296",
        "1296 304",
    ]
    bgcolor = 14
    acceptable_clouds = [(32, 0)]
    ending_button = Button(1480, 360)
    finished_next = "four"
    nextlevel = "four"
    slimehorn_variant = True
    use_gradient = True
    gradient_color = 9
    gradient_height = 60
    gradient_skips = [58, 57, 56, 54, 53, 52, 50, 49, 47, 46, 44, 43, 41, 40]


class Four(BaseLevel):
    """
    Level Four: Icy Peaks

    An icy mountain with increasing challenges,
    including some hard-to-reach jumps and
    conveniently-placed mobs.

    Mobs (21): Onions (3), Robots (9), Icy Slimehorns (9).
    """

    draw_v = 384
    enemy_template = {
        "72 424": Robot,
        "152 416": Robot,
        "208 456": Slimehorn1,
        "208 480": Slimehorn2,
        "264 456": Onion,
        "280 432": Onion,
        "280 440": Slimehorn2,
        "376 456": Robot,
        "496 424": Slimehorn2,
        "560 424": Robot,
        "592 424": Robot,
        "672 432": Slimehorn1,
        "672 448": Slimehorn2,
        "696 448": Robot,
        "840 440": Robot,
        "856 416": Robot,
        "896 440": Slimehorn2,
        "1104 432": Robot,
        "1344 424": Slimehorn1,
    }
    coin_template = [
        "40 408",
        "48 400",
        "56 408",
        "88 408",
        "96 400",
        "104 400",
        "128 400",
        "136 392",
        "144 400",
        "192 456",
        "200 456",
        "208 456",
        "272 424",
        "280 416",
        "280 424",
        "280 432",
        "288 424",
        "440 416",
        "440 424",
        "448 416",
        "448 424",
        "560 400",
        "560 416",
        "568 408",
        "576 400",
        "576 416",
        "584 408",
        "592 400",
        "592 416",
        "648 448",
        "664 448",
        "672 448",
        "688 448",
        "832 432",
        "832 440",
        "840 432",
        "840 440",
        "1040 416",
        "1048 424",
        "1056 432",
        "1064 440",
        "1072 448",
        "1080 456",
        "1096 408",
        "1096 416",
        "1104 408",
        "1104 416",
        "1120 456",
        "1128 448",
        "1136 440",
        "1144 432",
        "1152 424",
        "1336 432",
        "1344 432",
        "1352 432",
    ]
    bgcolor = 5
    acceptable_clouds = [(0, 32), (16, 32)]
    ending_button = Button(1512, 472)
    finished_next = "preboss"
    nextlevel = "preboss"
    use_gradient = True
    gradient_color = 12
    gradient_height = 129


class Five(BaseLevel):
    """
    Level Five: Bricklot Fortress

    The home fortress of the Scaler. Diddi and Eli
    must face the monster before it fully begins with
    his conquest plans.

    Mobs (): Robots (), Onions ().
    """

    draw_v = 512
    enemy_template = dict()
    coin_template = []
    bgcolor = 0  # Using black just once
    acceptable_clouds = [(32, 0)]  # indeed, we don't want clouds here
    finished_next = "final"
    nextlevel = "final"
    use_gradient = True
    gradient_color = 13
    gradient_height = 30
