import os
from functools import cached_property

from utils import JSONFile, Log, get_date_id

from lk_food.core.Food import Food

log = Log('Store')


class Store:
    DIR_RAW_DATA = os.path.join('data', 'raw')

    @cached_property
    def id(self):
        return self.name.lower()

    @property
    def data_path(self) -> str:
        if not os.path.exists(Store.DIR_RAW_DATA):
            os.makedirs(Store.DIR_RAW_DATA)
        return os.path.join(Store.DIR_RAW_DATA, f'{self.id}.json')

    @property
    def timed_data_path(self) -> str:
        if not os.path.exists(Store.DIR_RAW_DATA):
            os.makedirs(Store.DIR_RAW_DATA)
        return os.path.join(
            Store.DIR_RAW_DATA, f'{self.id}-{get_date_id()}.json'
        )

    def scrape(self) -> list[Food]:
        data_list = self.data_list

        data_list = self.data_list
        JSONFile(self.data_path).write(data_list)
        log.info(f'Wrote {len(data_list):,} foods to {self.data_path}')

        JSONFile(self.timed_data_path).write(data_list)
        log.info(f'Wrote {len(data_list):,} foods to {self.timed_data_path}')

        n = len(data_list)
        for i, data in enumerate(data_list):
            food = self.data_to_food(data)
            food.write()
            if i % 1_000 == 0:
                log.debug(f'Processed {i:,}/{n:,} foods ({food})')
