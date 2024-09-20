-- Remove compression policy from fx_prices
SELECT remove_compression_policy('fx_prices');
SELECT remove_compression_policy('adjusted_prices');
SELECT remove_compression_policy('multiple_prices');
SELECT remove_compression_policy('roll_calendars');

-- Disable compression on hypertables
ALTER TABLE fx_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE adjusted_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE multiple_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE roll_calendars
SET (
    timescaledb.compress = false
);
