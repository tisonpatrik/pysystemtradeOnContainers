-- Remove compression policy from fx_prices
SELECT remove_compression_policy('fx_prices');

-- Disable compression on fx_prices table
ALTER TABLE fx_prices
SET (
    timescaledb.compress = false
);
