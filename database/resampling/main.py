import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

csv_dir = Path.cwd() / "data" / "temp" / "adjusted_prices_csv"
out_dir = Path.cwd() / "data" / "daily_adjusted_prices"

path_to_list_of_instruments = Path.cwd() / "data_processing" / "configs" / "tradable_instruments.csv"
tradable_instruments = pd.read_csv(str(path_to_list_of_instruments), header=None)[0].str.strip().tolist()

# Ensure the output directory exists
out_dir.mkdir(parents=True, exist_ok=True)

# Limit the number of threads with a semaphore
max_threads = 8  # Adjust as per your system capability
semaphore = threading.Semaphore(max_threads)


# Function to resample, modify headers, and save data
def process_file(file_path):
    with semaphore:
        logging.info("Processing file: %s", file_path.name)
        try:
            # Read and resample the data
            data_series = pd.read_csv(str(file_path), index_col=0, parse_dates=True)
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


if not csv_dir.exists():
    logging.error("Directory does not exist: %s", csv_dir)
else:
    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(process_file, file_path)
            for file_path in csv_dir.glob("*.csv")
            if file_path.stem in tradable_instruments  # Filter files based on tradable instruments
        ]

        # Optionally wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  # Will raise an exception if the task failed
