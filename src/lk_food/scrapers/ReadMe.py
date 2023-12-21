from utils import TIME_FORMAT_TIME, File, Log, Time

from lk_food.core.Food import Food

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
        return self.lines_food

    @property
    def lines_food(self) -> list[str]:
        food_list = Food.list_all()
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
