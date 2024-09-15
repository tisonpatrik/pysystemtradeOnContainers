-- Enable compression on multiple_prices table
ALTER TABLE multiple_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Manually compress any existing chunks in multiple_prices
SELECT compress_chunk(c) FROM show_chunks('multiple_prices') c;

-- Add compression policy to compress chunks older than 7 days for multiple_prices
SELECT add_compression_policy('multiple_prices', INTERVAL '7 days');
