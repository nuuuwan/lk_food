# See https://medium.com/on-economics
# /bath-%E0%B6%B6%E0%B6%AD%E0%B7%8A-packet-2-0-f3e999c54bf5

# Rice (73 g uncooked, about ⅓ cups or hundus)
# Soya Meat (54 g)
# Dhal (16 g)
# Egg (half an egg)
# Brinjal (40 g)
# Pumpkin (40 g)
# Carrot (40 g)
# Onion (40 g)
# Coconut (29 g)
# Coconut Oil (7 g, or one and a half teaspoons)
# Green Chilli (8 g)
# Lime (4 g, or about a teaspoon)

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
