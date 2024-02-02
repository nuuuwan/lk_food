from lk_food.core import Store
from lk_food.scrapers.CargillsLK import CargillsLK


class StoreFactory:
    @staticmethod
    def list_all() -> list:
        return [CargillsLK]

    @staticmethod
    def idx() -> dict[str, Store]:
        return {
            store_cls.get_id(): store_cls
            for store_cls in StoreFactory.list_all()
        }
