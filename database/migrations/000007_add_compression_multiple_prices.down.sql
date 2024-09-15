-- Remove compression policy from multiple_prices
SELECT remove_compression_policy('multiple_prices');

-- Disable compression on multiple_prices table
ALTER TABLE multiple_prices
SET (
    timescaledb.compress = false
);
