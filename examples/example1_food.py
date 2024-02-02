from lk_food import Food

if __name__ == '__main__':
    for food in  Food.from_search_key('Rice'):
        print(food)
