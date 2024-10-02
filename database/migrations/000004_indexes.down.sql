BEGIN;
-- Drop index for adjusted_prices on symbol and time
DROP INDEX IF EXISTS ix_adjusted_prices_symbol_time;

-- Drop index for daily_adjusted_prices on symbol and time
DROP INDEX IF EXISTS ix_daily_adjusted_prices_symbol_time;

-- Drop index for fx_prices on symbol and time
DROP INDEX IF EXISTS ix_fx_prices_symbol_time;

-- Drop index for multiple_prices on symbol and time
DROP INDEX IF EXISTS ix_multiple_prices_symbol_time;

-- Drop index for roll_calendars on symbol and time
DROP INDEX IF EXISTS ix_roll_calendars_symbol_time;
COMMIT;
