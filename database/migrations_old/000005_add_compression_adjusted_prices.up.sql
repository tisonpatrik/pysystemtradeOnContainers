-- Enable compression on adjusted_prices table
ALTER TABLE adjusted_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Manually compress any existing chunks in adjusted_prices
SELECT compress_chunk(c) FROM show_chunks('adjusted_prices') c;

-- Add compression policy to compress chunks older than 7 days for adjusted_prices
SELECT add_compression_policy('adjusted_prices', INTERVAL '7 days');
