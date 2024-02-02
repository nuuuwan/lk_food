from functools import cache, cached_property

from utils import Log

from lk_food.core import Food, MenuItem
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
            if unit_of_measure == 'pcs':
                unit_of_measure = ''

            lines.append(
                ' | '.join(
                    [
                        Food.add_emojis(menu_item.food_name),
                        f'{actual_units:.1f} {unit_of_measure}',
                        f'{item_cost:.0f} LKR',
                    ]
                )
            )
        lines.append('')
        lines.append(f'TOTAL COST: **{cost:.0f} LKR**')
        lines.append('')
        return lines
