-- Remove compression policy from adjusted_prices
SELECT remove_compression_policy('adjusted_prices');

-- Remove compression policy from fx_prices
SELECT remove_compression_policy('fx_prices');

-- Remove compression policy from multiple_prices
SELECT remove_compression_policy('multiple_prices');

-- Remove compression policy from roll_calendars
SELECT remove_compression_policy('roll_calendars');

-- Disable compression on adjusted_prices table
ALTER TABLE adjusted_prices
SET (
    timescaledb.compress = false
);

-- Disable compression on fx_prices table
ALTER TABLE fx_prices
SET (
    timescaledb.compress = false
);

-- Disable compression on multiple_prices table
ALTER TABLE multiple_prices
SET (
    timescaledb.compress = false
);

-- Disable compression on roll_calendars table
ALTER TABLE roll_calendars
SET (
    timescaledb.compress = false
);
