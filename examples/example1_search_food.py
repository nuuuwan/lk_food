import sys

from lk_food import FoodDB

if __name__ == '__main__':
    search_key = sys.argv[1]
    for food in FoodDB.list_from_search_key(search_key):
        print(food)
