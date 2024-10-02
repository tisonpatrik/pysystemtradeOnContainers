BEGIN;

-- Convert adjusted_prices table to hypertable
SELECT create_hypertable(
    'adjusted_prices',
    'time',
    'symbol',
    number_partitions => 4
);

-- Convert daily_adjusted_prices table to hypertable
SELECT create_hypertable(
    'daily_adjusted_prices',
    'time',
    'symbol',
    number_partitions => 4
);

-- Convert fx_prices table to hypertable
SELECT create_hypertable(
    'fx_prices',
    'time'
);

-- Convert multiple_prices table to hypertable
SELECT create_hypertable(
    'multiple_prices',
    'time',
    'symbol',
    number_partitions => 4
);

-- Convert roll_calendars table to hypertable
SELECT create_hypertable(
    'roll_calendars',
    'time'
);

COMMIT;
