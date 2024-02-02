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

from functools import cache, cached_property

from utils import Log

from lk_food.core import MenuItem
from lk_food.data import FoodDB

log = Log('Menu')


class Menu:
    def __init__(self, *menu_items: list[MenuItem]):
        self.menu_items = menu_items

    @cache
    def get_cost(self, date_id: str = None) -> float:
        cost = 0
        for menu_item in self.menu_items:
            food = FoodDB.from_name(menu_item.food_name, date_id)
            price_of_unit = food.price_of_unit
            item_cost = price_of_unit * menu_item.units
            cost += item_cost

        return cost
    
    @cached_property 
    def lines_readme(self) -> list[str]:
        lines = ['', ' Item | Quantity | Cost (LKR) ', ' :--- | ---: | ---: ']
        cost = 0
        for menu_item in self.menu_items:
            food = FoodDB.from_name(menu_item.food_name, date_id=None)
            price_of_unit = food.price_of_unit
            item_cost = price_of_unit * menu_item.units
            cost += item_cost

            actual_units = menu_item.units * food.unit_size
            unit_of_measure = food.unit_of_measure

            if unit_of_measure == 'kg':
                actual_units *= 1000
                unit_of_measure = 'g'

            lines.append(' | '.join([
                menu_item.food_name,
                f'{actual_units:.1f} {unit_of_measure}',
                f'{item_cost:.0f} LKR'
            ]))
        lines.append('')
        lines.append(f'TOTAL COST: **{cost:.0f} LKR**')
        lines.append('')
        return lines