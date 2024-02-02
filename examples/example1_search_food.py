import sys

from lk_food import Food

if __name__ == '__main__':
    search_key = sys.argv[1]
    for food in Food.list_from_search_key(search_key):
        print(food)
