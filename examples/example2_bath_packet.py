from lk_food import BathPacket

if __name__ == '__main__':
    bp = BathPacket()
    cost = 0
    for item in bp.menu:
        print(item)
        cost += item.cost
    print('-' * 32)
    print(f'{bp.cost:.2f}: (TOTAL)')
    print('-' * 32)
