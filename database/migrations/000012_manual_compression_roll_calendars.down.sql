-- Decompress chunks for the table 'roll_calendars'
SELECT decompress_chunk(c)
FROM show_chunks('roll_calendars') c;
