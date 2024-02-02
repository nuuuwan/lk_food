import os
from dataclasses import dataclass
from functools import cache, cached_property
from typing import Generator

from utils import TIME_FORMAT_TIME, JSONFile, Log, Time

from utils_future import parse_float

log = Log('Food')


@dataclass
class Food:
    # general
    ut_updated: int
    store_id: str

    # codes
    sku_code: str
    category_code: str

    # details
    name: str
    short_description: str
    description: str
    unit_of_measure: str
    unit_size: float
    price_of_unit: float

    DIR_DATA_FOOD = os.path.join('data', 'food')

    def to_dict(self) -> dict:
        return dict(
            ut_updated=self.ut_updated,
            time_updated=TIME_FORMAT_TIME.stringify(Time(self.ut_updated)),
            store_id=self.store_id,
            sku_code=self.sku_code,
            category_code=self.category_code,
            name=self.name,
            short_description=self.short_description,
            description=self.description,
            unit_of_measure=self.unit_of_measure,
            unit_size=self.unit_size,
            price_of_unit=self.price_of_unit,
        )

    def from_dict(d: dict) -> 'Food':
        return Food(
            ut_updated=int(d['ut_updated']),
            store_id=d['store_id'],
            sku_code=d['sku_code'],
            category_code=d['category_code'],
            name=d['name'],
            short_description=d['short_description'],
            description=d['description'],
            unit_of_measure=d['unit_of_measure'],
            unit_size=parse_float(d['unit_size']),
            price_of_unit=parse_float(d['price_of_unit']),
        )

    def from_file(path: str) -> 'Food':
        d = JSONFile(path).read()
        return Food.from_dict(d)

    def __str__(self) -> str:
        return (
            f'Food("{self.name}"'
            + f' {self.unit_size}{self.unit_of_measure}'
            + f' Rs.{self.price_of_unit})'
        )

    @cached_property
    def data_path(self) -> str:
        if not os.path.exists(Food.DIR_DATA_FOOD):
            os.makedirs(Food.DIR_DATA_FOOD)
        return os.path.join(
            Food.DIR_DATA_FOOD, f'{self.store_id}-{self.sku_code}.json'
        )

    def write(self):
        JSONFile(self.data_path).write(self.to_dict())

    @staticmethod
    @cache
    def list_all() -> list['Food']:
        food_list = []
        for file_only in os.listdir(Food.DIR_DATA_FOOD):
            if not file_only.endswith('.json'):
                continue
            file_path = os.path.join(Food.DIR_DATA_FOOD, file_only)
            food = Food.from_file(file_path)
            food_list.append(food)
        return food_list

    @staticmethod
    @cache
    def list_from_search_key(
        search_key: str,
    ) -> Generator['Food', None, None]:
        search_key_lower = search_key.lower()
        for food in Food.list_all():
            if search_key_lower in food.name.lower():
                yield food

    @staticmethod
    @cache
    def from_name(name: str) -> 'Food':
        for food in Food.list_all():
            if name == food.name:
                return food
        raise ValueError(f'Food not found: {name}')
