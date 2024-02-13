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


class Protein(Menu):
    # How many units of the item are needed to get 50g of protein?

    @staticmethod
    def load() -> 'Protein':
        return Protein(
            MenuItem('Red Dhal', 200 / 1_000.0),
            MenuItem('Lankasoy Regular Soya', 50 / 90.0),
            MenuItem('Red Raw Rice', 562 / 1_000.0),
            MenuItem('Imported White Eggs', (50 / 13.0) / 10.0),
        )
