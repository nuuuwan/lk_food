import os
from functools import cache
from typing import Generator

from utils import JSONFile, Log

from lk_food.core import Food, Store
from lk_food.scrapers import StoreFactory

log = Log('FoodDB')


class FoodDB:
    @staticmethod
    @cache
    def get_date_ids() -> list[str]:
        DIR_DATA_RAW = os.path.join('data', 'raw')
        date_ids = []
        for file_name in os.listdir(DIR_DATA_RAW):
            if not file_name.endswith('.json'):
                continue
            _, date_id = Store.parse_data_path(file_name)
            date_ids.append(date_id)
        log.debug(f'Found data for {len(date_ids):,} date_ids')
        return date_ids

    @staticmethod
    @cache
    def get_latest_date_id() -> str:
        return max(FoodDB.get_date_ids())

    @staticmethod
    @cache
    def list_latest_date() -> list['Food']:
        date_id = FoodDB.get_latest_date_id()
        return FoodDB.list_from_date(date_id)

    @staticmethod
    @cache
    def list_from_date(date_id: str = None) -> list['Food']:
        DIR_DATA_RAW = os.path.join('data', 'raw')
        food_list = []
        for file_name in os.listdir(DIR_DATA_RAW):
            if not file_name.endswith('.json'):
                continue
            store_id, file_date_id = Store.parse_data_path(file_name)
            if file_date_id != date_id:
                continue

            file_path = os.path.join(DIR_DATA_RAW, file_name)
            data_list = JSONFile(file_path).read()
            store_cls = StoreFactory.idx()[store_id]
            file_food_list = [
                store_cls.get_food_from_data(data, date_id)
                for data in data_list
            ]
            file_food_list = [f for f in file_food_list if f is not None]

            food_list.extend(file_food_list)

        return food_list

    @staticmethod
    @cache
    def list_from_search_key(
        search_key: str,
    ) -> Generator['Food', None, None]:
        search_key_lower = search_key.lower()
        for food in FoodDB.list_latest_date():
            if search_key_lower in food.name.lower():
                yield food

    @staticmethod
    @cache
    def from_name(name: str, date_id: str = None) -> 'Food':
        if date_id:
            food_list = FoodDB.list_from_date(date_id)
        else:
            food_list = FoodDB.list_latest_date()

        for food in food_list:
            if name == food.name:
                return food
        return None
