-- Convert adjusted_prices table to hypertable
SELECT create_hypertable('adjusted_prices', by_range('time'));

-- Convert fx_prices table to hypertable
SELECT create_hypertable('fx_prices', by_range('time'));

-- Convert multiple_prices table to hypertable
SELECT create_hypertable('multiple_prices', by_range('time'));

-- Convert roll_calendars table to hypertable
SELECT create_hypertable('roll_calendars', by_range('time'));
