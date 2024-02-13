import datetime
from functools import cache

from utils import TIME_FORMAT_DATE_ID, Log

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
            try:
                food = FoodDB.from_name(menu_item.food_name, date_id)
            except Exception:
                log.error(f'No food found for {menu_item.food_name} ({date_id})')
                return None
            price_of_unit = food.price_of_unit
            item_cost = price_of_unit * menu_item.units
            cost += item_cost

        return cost

    @cache
    def get_cost_components(self, date_id: str = None) -> dict:
        cost_components = {}
        for menu_item in self.menu_items:
            try:
                food = FoodDB.from_name(menu_item.food_name, date_id)
            except Exception:
                log.error(f'No food found for {menu_item.food_name} ({date_id})')
                return None
            price_of_unit = food.price_of_unit
            item_cost = price_of_unit * menu_item.units
            cost_components[menu_item.food_name] = item_cost

        return cost_components

    @cache
    def get_cost_time_series(self) -> list[dict]:
        d_list = []
        for date_id in FoodDB.get_date_ids():
            cost_components = self.get_cost_components(date_id)
            if cost_components is None:
                continue
            t = TIME_FORMAT_DATE_ID.parse(date_id)
            date = datetime.datetime.fromtimestamp(t.ut)

            d = dict(
                date=date,
                cost_components=cost_components,
            )
            d_list.append(d)
        log.debug(f'Loaded {len(d_list):,} cost time series')
        return d_list
