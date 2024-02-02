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

from functools import cached_property

from lk_food.core import MenuItem
from lk_food.data import FoodDB


class BathPacket:
    @cached_property
    def menu(self) -> list[MenuItem]:
        return [
            MenuItem(FoodDB.from_name('Red Raw Rice'), 0.073),
            MenuItem(FoodDB.from_name('Lankasoy Regular Soya'), 0.054 / 0.09),
            MenuItem(FoodDB.from_name('Red Dhal'), 0.016),
            MenuItem(FoodDB.from_name('Happy Hen Eggs XL'), 0.5 / 10.0),
            MenuItem(FoodDB.from_name('Brinjal'), 0.04 / 0.35),
            MenuItem(FoodDB.from_name('Pumpkin'), 0.04 / 0.5),
            MenuItem(FoodDB.from_name('Carrot'), 0.04 / 0.5),
            MenuItem(FoodDB.from_name('Big Onion'), 0.04 / 0.5),
            MenuItem(FoodDB.from_name('Coconut'), 0.029 / (0.283 * 3)),
            MenuItem(FoodDB.from_name('Marina Coconut Oil'), 2.5 / 350),
            MenuItem(FoodDB.from_name('Green Chillies'), 0.008 / 0.1),
            MenuItem(FoodDB.from_name('Lime'), 0.004 / 0.25),
        ]

    @cached_property
    def cost(self) -> float:
        return sum([item.cost for item in self.menu])
