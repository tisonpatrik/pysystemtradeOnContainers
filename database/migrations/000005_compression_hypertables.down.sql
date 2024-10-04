BEGIN;

SELECT remove_compression_policy('fx_prices');
SELECT remove_compression_policy('daily_adjusted_prices');
SELECT remove_compression_policy('daily_denominator_prices');
SELECT remove_compression_policy('multiple_prices');
SELECT remove_compression_policy('roll_calendars');


ALTER TABLE fx_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE daily_denominator_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE daily_adjusted_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE multiple_prices
SET (
    timescaledb.compress = false
);

ALTER TABLE roll_calendars
SET (
    timescaledb.compress = false
);
COMMIT;
