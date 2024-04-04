import os

from utils import JSONFile, Log, TimeFormat

log = Log('Store')


class Store:
    DIR_RAW_DATA = os.path.join('data', 'raw')

    @classmethod
    def get_id(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_timed_data_path(cls) -> str:
        if not os.path.exists(Store.DIR_RAW_DATA):
            os.makedirs(Store.DIR_RAW_DATA)
        return Store.build_data_path(cls.get_id(), TimeFormat.DATE_ID.formatNow)

    @staticmethod
    def build_data_path(store_id: str, date_id: str) -> str:
        return os.path.join(Store.DIR_RAW_DATA, f'{store_id}-{date_id}.json')

    @staticmethod
    def parse_data_path(data_path: str) -> str:
        store_id, date_id = (
            os.path.basename(data_path).split('.')[-2].split('-')
        )
        return store_id, date_id

    @classmethod
    def scrape(cls) -> list:
        log.debug(f'Scraping {cls.get_id()}...')
        data_list = cls.get_data_list()
        path = cls.get_timed_data_path()
        JSONFile(path).write(data_list)
        log.info(f'Wrote {len(data_list):,} foods to {path}')
