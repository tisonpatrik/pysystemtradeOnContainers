BEGIN;

SELECT create_hypertable(
    'daily_adjusted_prices',
    'time',
    'symbol',
    number_partitions => 8
);

SELECT create_hypertable(
    'daily_denominator_prices',
    'time',
    'symbol',
    number_partitions => 8
);

SELECT create_hypertable(
    'fx_prices',
    'time'
);

SELECT create_hypertable(
    'multiple_prices',
    'time',
    'symbol',
    number_partitions => 8
);

SELECT create_hypertable(
    'roll_calendars',
    'time'
);

COMMIT;
