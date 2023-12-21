from lk_food.scrapers.CargillsLK import CargillsLK


class StoreFactory:
    @staticmethod
    def list_all() -> list:
        return [CargillsLK]
