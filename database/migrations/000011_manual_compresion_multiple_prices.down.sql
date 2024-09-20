-- Decompress chunks for the table 'multiple_prices'
SELECT decompress_chunk(c)
FROM show_chunks('multiple_prices') c;
