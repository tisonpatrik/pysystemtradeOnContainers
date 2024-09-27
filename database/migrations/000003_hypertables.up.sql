BEGIN;
-- Convert adjusted_prices table to hypertable
SELECT create_hypertable('adjusted_prices', 'time', 'symbol', number_partitions => 32);

-- Convert fx_prices table to hypertable
SELECT create_hypertable('fx_prices', 'time', 'symbol', number_partitions => 32);

-- Convert multiple_prices table to hypertable
SELECT create_hypertable('multiple_prices', 'time', 'symbol', number_partitions => 32);

-- Convert roll_calendars table to hypertable
SELECT create_hypertable('roll_calendars', 'time', 'symbol', number_partitions => 32);

COMMIT;
