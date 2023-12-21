import os
from dataclasses import dataclass
from functools import cached_property

from utils import TIME_FORMAT_TIME, JSONFile, Log, Time

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

    def __str__(self) -> str:
        return f'Food({self.sku_code} - {self.name})'

    @cached_property
    def data_path(self) -> str:
        if not os.path.exists(Food.DIR_DATA_FOOD):
            os.makedirs(Food.DIR_DATA_FOOD)
        return os.path.join(
            Food.DIR_DATA_FOOD, f'{self.store_id}-{self.sku_code}.json'
        )

    def write(self):
        JSONFile(self.data_path).write(self.to_dict())
