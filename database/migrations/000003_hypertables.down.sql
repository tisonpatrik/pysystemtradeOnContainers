-- Drop hypertable and recreate as regular PostgreSQL table for adjusted_prices
DROP TABLE IF EXISTS adjusted_prices;
CREATE TABLE adjusted_prices (
    time TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Drop hypertable and recreate as regular PostgreSQL table for fx_prices
DROP TABLE IF EXISTS fx_prices;
CREATE TABLE fx_prices (
    time TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Drop hypertable and recreate as regular PostgreSQL table for multiple_prices
DROP TABLE IF EXISTS multiple_prices;
CREATE TABLE multiple_prices (
    time TIMESTAMPTZ NOT NULL,
    carry DOUBLE PRECISION NULL,
    carry_contract INTEGER NOT NULL,
    price DOUBLE PRECISION NULL,
    price_contract INTEGER NOT NULL,
    forward DOUBLE PRECISION NULL,
    forward_contract INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Drop hypertable and recreate as regular PostgreSQL table for roll_calendars
DROP TABLE IF EXISTS roll_calendars;
CREATE TABLE roll_calendars (
    time TIMESTAMPTZ NOT NULL,
    current_contract INTEGER NOT NULL,
    next_contract INTEGER NOT NULL,
    carry_contract INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (time, symbol)
);
