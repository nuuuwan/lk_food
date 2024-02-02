# See https://medium.com/on-economics
# /bath-%E0%B6%B6%E0%B6%AD%E0%B7%8A-packet-2-0-f3e999c54bf5

from functools import cached_property

from lk_food.core.MenuItem import MenuItem


class BathPacket:
    @cached_property
    def menu(self) -> list[MenuItem]:
        return []
