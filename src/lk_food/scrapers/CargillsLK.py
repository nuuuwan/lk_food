from functools import cache

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import Log

from lk_food.core import Food, Store
from utils_future import SysMode, Float

log = Log('CargillsLK')


class CargillsLK(Store):
    # Scrapes information about food available at Cargills Online.

    @classmethod
    @cache
    def get_url_base(cls) -> str:
        return 'https://cargillsonline.com'

    @classmethod
    @cache
    def get_session_id(cls) -> str:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(cls.get_url_base())
        session_id = driver.get_cookie('ASP.NET_SessionId')['value']
        driver.quit()
        log.debug(f'{session_id=}')
        return session_id

    @classmethod
    @cache
    def get_headers(cls) -> str:
        return dict(
            Cookie=f'ASP.NET_SessionId={cls.get_session_id()}',
        )

    @classmethod
    @cache
    def get_category_ids(cls) -> list[str]:
        url = cls.get_url_base() + '/Web/GetCategoriesV1/'

        response = requests.post(
            url=url,
            headers=cls.get_headers(),
        )
        data_list = response.json()
        category_ids = [d['EnId'] for d in data_list]
        log.info(f'Found {len(category_ids)} category ids')
        return category_ids

    @classmethod
    @cache
    def get_data_list_for_category(cls, category_id: str) -> list[dict]:
        url = cls.get_url_base() + '/Web/GetMenuCategoryItemsPagingV3/'

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
            headers=cls.get_headers(),
        )
        data_list = response.json()
        log.debug(f'Found {len(data_list)} foods for category {category_id}')
        return data_list

    @classmethod
    @cache
    def get_data_list(cls) -> list[dict]:
        all_data_list = []
        for category_id in cls.get_category_ids():
            data_list = cls.get_data_list_for_category(category_id)
            all_data_list.extend(data_list)
            if SysMode.TEST:
                log.warning('[SysMode.TEST] Breaking after first category')
                break
        return all_data_list

    @classmethod
    def get_food_from_data(cls, d: dict, date_id: str) -> Food:
        return Food(
            date_id=date_id,
            store_id=cls.get_id(),
            sku_code=d['SKUCODE'],
            category_code=d['CategoryCode'],
            name=d['ItemName'],
            short_description=d['ShortDescription'],
            description=d['Description'],
            unit_of_measure=d['UOM'],
            unit_size=Float.parse(d['UnitSize']),
            price_of_unit=Float.parse(d['Price']),
        )
