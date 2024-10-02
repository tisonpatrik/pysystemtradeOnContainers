BEGIN;
-- Enable compression for hypertables
ALTER TABLE fx_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

ALTER TABLE adjusted_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

ALTER TABLE daily_adjusted_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

ALTER TABLE multiple_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

ALTER TABLE roll_calendars
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Add compression policy to compress chunks older than 7 days
SELECT add_compression_policy('fx_prices', INTERVAL '7 days');
SELECT add_compression_policy('adjusted_prices', INTERVAL '7 days');
SELECT add_compression_policy('daily_adjusted_prices', INTERVAL '7 days');
SELECT add_compression_policy('multiple_prices', INTERVAL '7 days');
SELECT add_compression_policy('roll_calendars', INTERVAL '7 days');

COMMIT;
