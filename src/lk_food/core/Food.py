from dataclasses import dataclass

from utils import Log

log = Log('Food')

# Rice (73 g uncooked, about ⅓ cups or hundus)
# Soya Meat (54 g)
# Dhal (16 g)
# Egg (half an egg)
# Brinjal (40 g)
# Pumpkin (40 g)
# Carrot (40 g)
# Onion (40 g)
# Coconut (29 g)
# Coconut Oil (7 g, or one and a half teaspoons)
# Green Chilli (8 g)
# Lime (4 g, or about a teaspoon)

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


    @staticmethod
    def add_emojis(food_name: str):
        for key, emoji in [
            ('Rice', '🍚'),
            ('Soya Meat', ''),
            ('Dhal', ''),
            ('Egg', '🥚'),
            ('Brinjal', '🍆'),
            ('Pumpkin', '🎃'),
            ('Carrot', '🥕'),
            ('Onion', '🧅'),
            ('Coconut', '🥥'),
            ('Coconut Oil', '🥥'),
            ('Green Chilli', '🌶️'),
            ('Lime', '🍋'),
            
        ]:
            if key in food_name:
                return f'{emoji} {food_name}'
        return food_name     