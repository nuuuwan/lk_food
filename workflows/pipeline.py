from lk_food.scrapers.StoreFactory import StoreFactory


def main():
    for store_class in StoreFactory.list_all():
        store = store_class()
        store.scrape()


if __name__ == '__main__':
    main()
