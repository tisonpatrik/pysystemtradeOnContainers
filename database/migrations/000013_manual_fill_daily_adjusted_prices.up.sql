-- Manual refresh for continuous aggregate views

CALL refresh_continuous_aggregate('daily_adjusted_prices', NULL, localtimestamp - INTERVAL '7 days');
