"""Handle app configurations."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Map environment variables."""

    csv_config: str = os.environ.get("CSV_CONFIG", "")
    adjusted_prices: str = os.environ.get("ADJUSTED_PRICES", "")
    fx_prices: str = os.environ.get("FX_PRICES", "")
    multiple_prices: str = os.environ.get("MULTIPLE_PRICES", "")
    roll_calendars: str = os.environ.get("ROLL_CALENDARS", "")

    @property
    def file_to_table_mapping(self):
        """Map files to tables."""
        return {
            "csv_config": self.csv_config,
            "adjusted_prices": self.adjusted_prices,
            "fx_prices": self.fx_prices,
            "multiple_prices": self.multiple_prices,
            "roll_calendars": self.roll_calendars,
        }


settings = Settings()
