from utils import Log 
log = Log('Float')

class Float:
    @staticmethod
    def parse(x):
        x = str(x).replace(',', '')
        try:
            return float(x)
        except Exception as e:
            log.error(f"Float.parse({x}) failed: {e}")
            return None
