from dataclasses import dataclass

from lk_food.core.Food import Food


@dataclass
class MenuItem:
    food: Food
    units: float
