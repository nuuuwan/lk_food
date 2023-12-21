def parse_float(x) -> float:
    try:
        return float(str(x))
    except Exception as e:
        return None
