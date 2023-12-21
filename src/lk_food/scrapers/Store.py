import os
from functools import cached_property

from utils import JSONFile, Log

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

    @cached_property
    def data_list_cache(self) -> list[dict]:
        if os.path.exists(self.data_path):
            data_list = JSONFile(self.data_path).read()
            log.info(f'Read {len(data_list):,} foods from {self.data_path}')
            return data_list
        JSONFile(self.data_path).write(self.data_list)
        log.info(f'Wrote {len(self.data_list):,} foods to {self.data_path}')
        return self.data_list

    def scrape(self) -> list[Food]:
        n = len(self.data_list_cache)
        for i, data in enumerate(self.data_list_cache):
            food = self.data_to_food(data)
            food.write()
            if i % 1_000 == 0:
                log.debug(f'Processed {i:,}/{n:,} foods ({food})')
