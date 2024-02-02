from lk_food import BathPacket

if __name__ == '__main__':
    bp = BathPacket.load()
    print(bp.get_cost())
