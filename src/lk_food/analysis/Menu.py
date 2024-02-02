from functools import cache

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
