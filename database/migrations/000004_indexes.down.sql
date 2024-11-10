BEGIN;

DROP INDEX IF EXISTS ix_daily_adjusted_prices_symbol_time;

DROP INDEX IF EXISTS ix_daily_denominator_prices_symbol_time;

DROP INDEX IF EXISTS ix_fx_prices_symbol_time;

DROP INDEX IF EXISTS ix_multiple_prices_symbol_time;

COMMIT;
