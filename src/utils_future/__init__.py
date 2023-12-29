from utils import Log

log = Log('utils_future')


def parse_float(x) -> float:
    x = str(x)
    x = x.replace(',', '')
    try:
        return float(str(x))
    except Exception as e:
        log.error(f'parse_float({x}) failed: {e}')
        return None
