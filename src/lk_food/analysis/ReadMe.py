from utils import TIME_FORMAT_TIME, File, Log, Time

from lk_food.analysis.BathPacket import BathPacket
from lk_food.core import Food
from lk_food.data import FoodDB

log = Log("ReadMe")


class ReadMe:
    PATH_STATIC_HEADER = "README.static.header.md"
    PATH_STATIC_FOOTER = "README.static.footer.md"
    PATH = "README.md"

    @staticmethod
    def clean_readme(path):
        lines = File(path).read_lines()
        lines = [line.strip() for line in lines]
        content = "\n".join(lines)
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        File(path).write(content)
        log.debug(f'Cleaned {path}')

    @property
    def lines(self) -> list[str]:
        return (
            self.lines_static_header
            + self.lines_dynamic
            + self.lines_static_footer
        )

    def write(self):
        ReadMe.clean_readme(ReadMe.PATH_STATIC_FOOTER)
        ReadMe.clean_readme(ReadMe.PATH_STATIC_HEADER)

        File(ReadMe.PATH).write_lines(self.lines)
        ReadMe.clean_readme(ReadMe.PATH)
        log.info(f"Wrote {ReadMe.PATH}.")

    @property
    def lines_static_header(self) -> list[str]:
        return File(ReadMe.PATH_STATIC_HEADER).read_lines()

    @property
    def lines_static_footer(self) -> list[str]:
        return File(ReadMe.PATH_STATIC_FOOTER).read_lines()

    @property
    def lines_dynamic(self) -> list[str]:
        return self.lines_food + self.lines_bath_packet

    @property
    def lines_food(self) -> list[str]:
        food_list = FoodDB.list_latest_date()
        n_foot_list = len(food_list)
        time_str = TIME_FORMAT_TIME.stringify(Time.now())
        return [
            '',
            '## Food Data',
            '',
            '> [!IMPORTANT]',
            f'> Scraped {n_foot_list:,} items as of {time_str}.',
            '',
        ]

    @property
    def lines_bath_packet(self) -> list[str]:
        bp = BathPacket.load()
        return (
            [
                '',
                '## Bath Packet Index (BPI)',
                '',
            ]
            + self.get_lines_menu(bp)
            + [
                '',
                '> [!IMPORTANT]',
                f'> For details on methodology, see [Bath (බත්) Packet 2.0]({bp.get_medium_url()}).',
                '',
            ]
        )

    @staticmethod
    def get_lines_menu(menu) -> list[str]:
        lines = ['', ' Item | Quantity | Cost (LKR) ', ' :--- | ---: | ---: ']
        cost = 0
        for menu_item in menu.menu_items:
            food = FoodDB.from_name(menu_item.food_name, date_id=None)
            price_of_unit = food.price_of_unit
            item_cost = price_of_unit * menu_item.units
            cost += item_cost

            actual_units = menu_item.units * food.unit_size
            unit_of_measure = food.unit_of_measure

            if unit_of_measure == 'kg':
                actual_units *= 1000
                unit_of_measure = 'g'
            if unit_of_measure == 'pcs':
                unit_of_measure = ''

            lines.append(
                ' | '.join(
                    [
                        Food.add_emojis(menu_item.food_name),
                        f'**{actual_units:.1f}** {unit_of_measure}',
                        f'**{item_cost:.2f}** LKR',
                    ]
                )
            )

        lines.append(f'**TOTAL** |   | **{cost:.2f}** LKR')
        lines.append('')
        return lines
