from functools import cached_property
from lk_food.analysis.Menu import Menu
from lk_food.core import MenuItem


class BathPacket(Menu):
    @staticmethod
    def load() -> Menu:
        return BathPacket.load_v2_1()

    @staticmethod
    def load_v2_1() -> Menu:
        return Menu(
            MenuItem('Red Raw Rice', 0.073),
            MenuItem('Lankasoy Regular Soya', 0.054 / 0.09),
            MenuItem('Red Dhal', 0.016),
            MenuItem('Happy Hen Eggs XL', 0.5 / 10.0),
            MenuItem('Brinjal', 0.04 / 0.35),
            MenuItem('Pumpkin', 0.04 / 0.5),
            MenuItem('Carrot', 0.04 / 0.5),
            MenuItem('Big Onion', 0.04 / 0.5),
            MenuItem('Coconut', 0.029 / (0.283 * 3)),
            MenuItem('Marina Coconut Oil', 2.5 / 350),
            MenuItem('Green Chillies', 0.008 / 0.1),
            MenuItem('Lime', 0.004 / 0.25),
        )

 