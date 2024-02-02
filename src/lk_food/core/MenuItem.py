from dataclasses import dataclass


@dataclass
class MenuItem:
    food_name: str
    units: float

    def __str__(self) -> str:
        return +f'{self.food_name}' + f'\t{self.units:.2f}'
