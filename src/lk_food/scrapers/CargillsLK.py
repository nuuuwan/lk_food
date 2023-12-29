from functools import cache, cached_property

import requests
from utils import Log, Time

from lk_food.core.Food import Food
from lk_food.scrapers.Store import Store
from utils_future import parse_float

log = Log('CargillsLK')


class CargillsLK(Store):
    # Scrapes information about food available at Cargills Online.

    def __init__(self):
        self.name = "CargillsLK"
        self.url_base = "https://cargillsonline.com"
        self.ut_updated = int(Time.now().ut)

    HEADERS = dict(
        Cookie='ASP.NET_SessionId=zowqqyzzyqyxcehlf3utdfzg',
    )

    @cached_property
    def category_ids(self) -> list[str]:
        url = self.url_base + '/Web/GetCategoriesV1/'

        response = requests.post(
            url=url,
            headers=CargillsLK.HEADERS,
        )
        data_list = response.json()
        category_ids = [d['EnId'] for d in data_list]
        log.info(f'Found {len(category_ids)} category ids')
        return category_ids

    @cache
    def get_data_list_for_category(self, category_id: str) -> list[dict]:
        url = self.url_base + '/Web/GetMenuCategoryItemsPagingV3/'

        data = dict(
            BannerId='',
            CategoryId=category_id,
            CollectionId='',
            DataType='',
            Filter='',
            PageIndex=1,
            PageSize=10000,
            PromoId='',
            Search='',
            SectionId='',
            SectionType='',
            SubCatId='-1',
        )

        response = requests.post(
            url=url,
            json=data,
            headers=CargillsLK.HEADERS,
        )
        data_list = response.json()
        log.debug(f'Found {len(data_list)} foods for category {category_id}')
        return data_list

    @cached_property
    def data_list(self) -> list[dict]:
        all_data_list = []
        for category_id in self.category_ids:
            data_list = self.get_data_list_for_category(category_id)
            all_data_list.extend(data_list)
        return all_data_list

    def data_to_food(self, d: dict) -> Food:
        return Food(
            ut_updated=int(self.ut_updated),
            store_id=self.id,
            sku_code=d['SKUCODE'],
            category_code=d['CategoryCode'],
            name=d['ItemName'],
            short_description=d['ShortDescription'],
            description=d['Description'],
            unit_of_measure=d['UOM'],
            unit_size=parse_float(d['UnitSize']),
            price_of_unit=parse_float(d['Price']),
        )
