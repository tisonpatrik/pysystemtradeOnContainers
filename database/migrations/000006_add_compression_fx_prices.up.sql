-- Enable compression on fx_prices table
ALTER TABLE fx_prices
SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Manually compress any existing chunks in fx_prices
SELECT compress_chunk(c) FROM show_chunks('fx_prices') c;

-- Add compression policy to compress chunks older than 7 days for fx_prices
SELECT add_compression_policy('fx_prices', INTERVAL '7 days');
