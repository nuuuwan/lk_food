from lk_food import ReadMe, StoreFactory


def main():
    for store_class in StoreFactory.list_all():
        store = store_class()
        store.scrape()

    ReadMe().write()


if __name__ == '__main__':
    main()
