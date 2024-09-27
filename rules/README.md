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
)
SELECT
    s.symbol,
    bd.day AS day_bucket,
    sub.last_price
FROM
    symbols s
CROSS JOIN business_days bd
LEFT JOIN LATERAL (
    SELECT
        ap.price AS last_price
    FROM
        adjusted_prices ap
    WHERE
        ap.symbol = s.symbol
        AND ap.time::date = bd.day
        AND ap.price IS NOT NULL
    ORDER BY
        ap.time DESC
    LIMIT 1
) sub ON TRUE
ORDER BY
    s.symbol,
    bd.day;
