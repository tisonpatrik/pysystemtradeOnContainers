-- Manual refresh for continuous aggregate views
CALL refresh_continuous_aggregate('daily_fx_prices', NULL, localtimestamp - INTERVAL '7 days');
