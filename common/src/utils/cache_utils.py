def get_series_key(name: str, instrument_code: str)->str:
    parts = ["series", name, "of", instrument_code]
    return ":".join(parts)
