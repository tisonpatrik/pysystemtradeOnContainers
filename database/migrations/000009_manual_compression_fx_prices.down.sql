-- Down migration script for decompressing chunks

-- Decompress chunks for the table 'fx_prices'
SELECT decompress_chunk(c)
FROM show_chunks('fx_prices') c;
