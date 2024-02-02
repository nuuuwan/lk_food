import os

from utils import Log

log = Log('utils_future')


def parse_float(x) -> float:
    if x is None:
        return None

    x = str(x)
    x = x.replace(',', '')
    try:
        return float(str(x))
    except Exception as e:
        log.error(f'parse_float({x}) failed: {e}')
        return None


class SysMode:
    TEST = os.name == 'nt'
    DEV = not TEST
    log.debug(f'{TEST=}')
