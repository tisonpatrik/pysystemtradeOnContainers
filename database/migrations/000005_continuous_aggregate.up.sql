BEGIN;

CREATE MATERIALIZED VIEW daily_adjusted_prices AS
WITH date_range AS (
    SELECT
        MIN(time::date) AS start_date,
        MAX(time::date) AS end_date
    FROM
        adjusted_prices
),
business_days AS (
    SELECT
        date::date AS day
    FROM generate_series(
        (SELECT start_date FROM date_range),
        (SELECT end_date FROM date_range),
        INTERVAL '1 day'
    ) AS date
    WHERE EXTRACT(ISODOW FROM date) BETWEEN 1 AND 5  -- Filters Monday to Friday
),
symbols AS (
    SELECT DISTINCT symbol FROM adjusted_prices
),
symbol_dates AS (
    SELECT
        s.symbol,
        bd.day AS day
    FROM
        symbols s
    CROSS JOIN business_days bd
)
SELECT
    sd.symbol,
    sd.day AS day_bucket,
    (
        SELECT
            ap.price
        FROM
            adjusted_prices ap
        WHERE
            ap.symbol = sd.symbol
            AND ap.time::date = sd.day
            AND ap.price IS NOT NULL
        ORDER BY
            ap.time DESC
        LIMIT 1
    ) AS last_price
FROM
    symbol_dates sd
ORDER BY
    sd.symbol,
    sd.day
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_denom_prices AS
WITH date_range AS (
    SELECT
        MIN(time::date) AS start_date,
        MAX(time::date) AS end_date
    FROM
        multiple_prices
),
business_days AS (
    SELECT
        date::date AS day
    FROM generate_series(
        (SELECT start_date FROM date_range),
        (SELECT end_date FROM date_range),
        INTERVAL '1 day'
    ) AS date
    WHERE EXTRACT(ISODOW FROM date) BETWEEN 1 AND 5  -- Filters Monday to Friday
),
symbols AS (
    SELECT DISTINCT symbol FROM multiple_prices
),
symbol_dates AS (
    SELECT
        s.symbol,
        bd.day AS day
    FROM
        symbols s
    CROSS JOIN business_days bd
)
SELECT
    sd.symbol,
    sd.day AS day_bucket,
    (
        SELECT
            ap.price
        FROM
            multiple_prices ap
        WHERE
            ap.symbol = sd.symbol
            AND ap.time::date = sd.day
            AND ap.price IS NOT NULL
        ORDER BY
            ap.time DESC
        LIMIT 1
    ) AS last_price
FROM
    symbol_dates sd
ORDER BY
    sd.symbol,
    sd.day
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_fx_prices AS
WITH date_range AS (
    SELECT
        MIN(time::date) AS start_date,
        MAX(time::date) AS end_date
    FROM
        fx_prices
),
business_days AS (
    SELECT
        date::date AS day
    FROM generate_series(
        (SELECT start_date FROM date_range),
        (SELECT end_date FROM date_range),
        INTERVAL '1 day'
    ) AS date
    WHERE EXTRACT(ISODOW FROM date) BETWEEN 1 AND 5  -- Filters Monday to Friday
),
symbols AS (
    SELECT DISTINCT symbol FROM fx_prices
),
symbol_dates AS (
    SELECT
        s.symbol,
        bd.day AS day
    FROM
        symbols s
    CROSS JOIN business_days bd
)
SELECT
    sd.symbol,
    sd.day AS day_bucket,
    (
        SELECT
            ap.price
        FROM
            fx_prices ap
        WHERE
            ap.symbol = sd.symbol
            AND ap.time::date = sd.day
            AND ap.price IS NOT NULL
        ORDER BY
            ap.time DESC
        LIMIT 1
    ) AS last_price
FROM
    symbol_dates sd
ORDER BY
    sd.symbol,
    sd.day
WITH NO DATA;

CREATE MATERIALIZED VIEW daily_roll_calendars
WITH (timescaledb.continuous) AS
SELECT
    symbol,
    time_bucket(INTERVAL '1 day', time) AS day_bucket,
    last(current_contract, time) AS last_current_contract,
    last(next_contract, time) AS last_next_contract,
    last(carry_contract, time) AS last_carry_contract
FROM
    roll_calendars
GROUP BY
    symbol,
    day_bucket
WITH NO DATA;

COMMIT;
