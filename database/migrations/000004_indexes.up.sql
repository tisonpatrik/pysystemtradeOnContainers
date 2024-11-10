BEGIN;

CREATE UNIQUE INDEX ix_daily_adjusted_prices_symbol_time
    ON daily_adjusted_prices (symbol, time);

CREATE UNIQUE INDEX ix_daily_denominator_prices_symbol_time
    ON daily_denominator_prices (symbol, time);

CREATE UNIQUE INDEX ix_fx_prices_symbol_time
    ON fx_prices (symbol, time);

CREATE UNIQUE INDEX ix_multiple_prices_symbol_time
    ON multiple_prices (symbol, time);
COMMIT;
