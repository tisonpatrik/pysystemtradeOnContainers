import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Limit the number of threads with a semaphore
max_threads = 8  # Adjust as per your system capability
semaphore = threading.Semaphore(max_threads)


# Function to resample, modify headers, and save data
def process_file(file_path, out_dir):
    with semaphore:
        try:
            # Read the CSV, selecting only the 'DATETIME' and 'PRICE' columns, and set 'DATETIME' as the index
            data_series = pd.read_csv(
                str(file_path),
                usecols=["DATETIME", "PRICE"],  # Only use relevant columns
                index_col="DATETIME",  # Set 'DATETIME' as the index
                parse_dates=True  # Parse 'DATETIME' as datetime
            )

            # Resample the data to business days frequency
            resampled = data_series.resample("1B").last()

            # Rename columns to match the new format: 'time', 'price'
            resampled.columns = ["price"]
            resampled.index.name = "time"

            # Convert 'price' column to decimal and round it to 3 decimal places
            resampled["price"] = resampled["price"].astype(float).round(3)

            # Add a new column 'symbol' with the filename (without the extension)
            symbol_name = file_path.stem
            resampled["symbol"] = symbol_name

            # Construct output file path and save the resampled data with the new format
            out_file = out_dir / file_path.name
            resampled.to_csv(out_file)

            logging.info("Resampled series saved to %s", out_file)
        except Exception:
            logging.exception("Failed to process %s", file_path.name)


def load_tradable_instruments(file_path):
    return pd.read_csv(str(file_path), header=None)[0].str.strip().tolist()


def process_multiple_prices(csv_dir, out_dir, tradable_instruments_path):
    # Ensure the output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)

    tradable_instruments = load_tradable_instruments(tradable_instruments_path)

    if not csv_dir.exists():
        logging.error("Directory does not exist: %s", csv_dir)
        return

    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(process_file, file_path, out_dir)
            for file_path in csv_dir.glob("*.csv")
            if file_path.stem in tradable_instruments  # Filter files based on tradable instruments
        ]

        # Optionally wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  # Will raise an exception if the task failed
