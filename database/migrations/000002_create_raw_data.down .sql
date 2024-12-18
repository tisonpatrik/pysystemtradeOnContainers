BEGIN;

-- Drop the tables in reverse order to avoid foreign key issues
DROP TABLE IF EXISTS multiple_prices;
DROP TABLE IF EXISTS fx_prices;
DROP TABLE IF EXISTS daily_adjusted_prices;
DROP TABLE IF EXISTS daily_denominator_prices;
COMMIT;
