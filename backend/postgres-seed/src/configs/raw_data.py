"""Handle app configurations."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Map environment variables."""

    csv_config: str = "/path/in/container/csvconfig"
    adjusted_prices: str = "/path/in/container/adjusted_prices_csv"
    fx_prices: str = "/path/in/container/fx_prices_csv"
    multiple_prices: str = "/path/in/container/multiple_prices_csv"
    roll_calendars: str = "/path/in/container/roll_calendars_csv"

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
