from dataclasses import dataclass
from functools import cached_property

from lk_food.core.Food import Food


@dataclass
class MenuItem:
    food: Food
    units: float

    @cached_property
    def cost(self) -> float:
        return self.food.price_of_unit * self.units

    def __str__(self) -> str:
        actual_units = self.units * self.food.unit_size
        return (
            f'{self.cost:.2f}:'
            + f' {self.food.name}'
            + f' ({actual_units:.2f}{self.food.unit_of_measure})'
        )
