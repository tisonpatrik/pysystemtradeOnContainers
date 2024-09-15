-- Remove compression policy from adjusted_prices
SELECT remove_compression_policy('adjusted_prices');

-- Disable compression on adjusted_prices table
ALTER TABLE adjusted_prices
SET (
    timescaledb.compress = false
);
