from utils import Log

log = Log('Float')


class Float:
    @staticmethod
    def parse(x):
        assert x is not None
        x = str(x).replace(',', '')
        try:
            return float(x)
        except Exception as e:
            return 0
