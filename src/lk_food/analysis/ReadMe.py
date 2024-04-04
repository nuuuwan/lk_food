import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from utils import TimeFormat, File, Log, Time

from lk_food.analysis.BathPacket import BathPacket
from lk_food.analysis.Protein import Protein
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
        return self.lines_food + self.lines_analysis

    @property
    def lines_food(self) -> list[str]:
        food_list = FoodDB.list_latest_date()
        n_foot_list = len(food_list)
        time_str = TimeFormat.TIME.stringify(Time.now())
        return [
            '',
            '## Food Data',
            '',
            '> [!IMPORTANT]',
            f'> Scraped {n_foot_list:,} items as of {time_str}.',
            '',
        ]

    def build_bpi_chart(self, bp):
        plt.close()
        time_series = bp.get_cost_time_series()
        x = [d['date'] for d in time_series]

        labels = time_series[0]['cost_components'].keys()
        ys = []
        for label in labels:
            y = [d['cost_components'][label] for d in time_series]
            ys.append(y)
        [np.var(y) for y in ys]
        labels, ys = zip(*sorted(zip(labels, ys), key=lambda x: np.var(x[1])))

        y = np.vstack(ys)

        plt.title('Bath Packet Index (BPI)')

        fig, ax = plt.subplots()
        ax.stackplot(
            x,
            y,
            labels=labels,
            colors=plt.cm.tab20b(
                (4.0 / 3 * np.arange(20 * 3 / 4)).astype(int)
            ),
        )

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        plt.title('Bath Packet Index (BPI) - Components')
        plt.xlabel('Date')
        plt.ylabel('Cost (LKR)')

        fig.set_size_inches(8, 4.5)

        box = ax.get_position()
        ax.set_position(
            [box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7]
        )

        # Put a legend below current axis
        ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, -0.2),
            ncol=3,
        )

        image_path = os.path.join('images', 'bpi.png')
        log.debug(f'Wrote {image_path}')
        plt.savefig(image_path)
        plt.close()
        return image_path

    @property
    def lines_analysis(self) -> list[str]:
        bp = BathPacket.load()
        protein = Protein.load()
        image_path = self.build_bpi_chart(bp).replace('\\', '/')
        return (
            [
                '',
                '## 50g of Protein',
                '',
            ]
            + ['', '<div id="table_protein">', '']
            + self.get_lines_menu(protein, show_total=False)
            + ['', '</div>', '']
            + [
                '',
                '## Bath Packet Index (BPI)',
                '',
            ]
            + ['', '<div id="table_bp">', '']
            + self.get_lines_menu(bp)
            + ['', '</div>', '']
            + [
                '',
                '### Daily Trend',
                '',
                f'![BPI]({image_path})',
            ]
            + [
                '',
                '> [!IMPORTANT]',
                '> For details on methodology,'
                + f' see [Bath (බත්) Packet 2.0]({bp.get_medium_url()}).',
                '',
            ]
        )

    @staticmethod
    def get_lines_menu(menu, show_total: bool = True) -> list[str]:
        lines = ['', ' Item | Quantity | Cost (LKR) ', ' :--- | ---: | ---: ']
        cost = 0

        sorted_menu_items = sorted(
            menu.menu_items,
            key=lambda x: FoodDB.from_name(
                x.food_name, date_id=None
            ).price_of_unit
            * x.units,
        )

        for menu_item in sorted_menu_items:
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
        if show_total:
            lines.append(f'**TOTAL** |   | **{cost:.2f}** LKR')
        lines.append('')
        return lines
