from lk_food.scrapers.ReadMe import ReadMe
from lk_food.scrapers.StoreFactory import StoreFactory

def main():
    for store_class in StoreFactory.list_all():
        store = store_class()
        store.scrape()

    ReadMe().write()


if __name__ == '__main__':
    main()
