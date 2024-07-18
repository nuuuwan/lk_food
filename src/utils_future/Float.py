class Float:
    @staticmethod
    def parse(x):
        try:
            return float(x)
        except ValueError:
            return None
