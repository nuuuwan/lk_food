from dataclasses import dataclass

from utils import Log

log = Log('Food')


@dataclass
class Food:
    # general
    date_id: str
    store_id: str

    # codes
    sku_code: str  # noqa
    category_code: str  # noqa

    # details
    name: str
    short_description: str  # noqa
    description: str  # noqa
    unit_of_measure: str
    unit_size: float
    price_of_unit: float

    def __str__(self) -> str:
        return (
            f'Food("{self.name}"'
            + f' {self.unit_size}{self.unit_of_measure}'
            + f' Rs.{self.price_of_unit})'
        )
