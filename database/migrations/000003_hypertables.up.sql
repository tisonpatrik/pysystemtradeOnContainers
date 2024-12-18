BEGIN;

SELECT create_hypertable(
    'daily_adjusted_prices',
    'time',
    'symbol',
    number_partitions => 166,
    chunk_time_interval => INTERVAL '6 months'
);

SELECT create_hypertable(
    'daily_denominator_prices',
    'time',
    'symbol',
    number_partitions => 166,
    chunk_time_interval => INTERVAL '6 months'
);

SELECT create_hypertable(
    'fx_prices',
    'time',
    chunk_time_interval => INTERVAL '6 months'
);

SELECT create_hypertable(
    'multiple_prices',
    'time',
    'symbol',
    number_partitions => 166,
    chunk_time_interval => INTERVAL '6 months'
);

COMMIT;
