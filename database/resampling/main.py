from pathlib import Path

from daily_adjusted_prices import process_adjusted_prices
from daily_multiple_prices import process_multiple_prices


def main():
    # Set your default paths here
    adjusted_prices_source = Path.cwd() / "data" / "temp" / "adjusted_prices_csv"
    adjusted_prices_target = Path.cwd() / "data" / "daily_adjusted_prices"
    path_to_list_of_instruments = Path.cwd() / "data_processing" / "configs" / "tradable_instruments.csv"

    multiple_prices_source = Path.cwd() / "data" / "temp" / "multiple_prices_csv"
    multiple_prices_target = Path.cwd() / "data" / "daily_multiple_prices"

    process_adjusted_prices(adjusted_prices_source, adjusted_prices_target, path_to_list_of_instruments)
    process_multiple_prices(multiple_prices_source, multiple_prices_target, path_to_list_of_instruments)


if __name__ == "__main__":
    main()
