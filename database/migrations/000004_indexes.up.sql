BEGIN;
-- Create index for adjusted_prices on symbol and time
CREATE INDEX ix_adjusted_prices_symbol_time ON adjusted_prices (symbol, time DESC);

-- Create index for fx_prices on symbol and time
CREATE INDEX ix_fx_prices_symbol_time ON fx_prices (symbol, time DESC);

-- Create index for multiple_prices on symbol and time
CREATE INDEX ix_multiple_prices_symbol_time ON multiple_prices (symbol, time DESC);

-- Create index for roll_calendars on symbol and time
CREATE INDEX ix_roll_calendars_symbol_time ON roll_calendars (symbol, time DESC);
COMMIT;
