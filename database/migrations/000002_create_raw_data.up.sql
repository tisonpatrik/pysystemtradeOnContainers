BEGIN;

CREATE TABLE daily_adjusted_prices (
    time TIMESTAMPTZ NOT NULL,
    price NUMERIC(14, 5) NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

CREATE TABLE fx_prices (
    time TIMESTAMPTZ NOT NULL,
    price NUMERIC(14, 5) NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol)
);

CREATE TABLE daily_denominator_prices (
    time TIMESTAMPTZ NOT NULL,
    price NUMERIC(14, 5) NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

CREATE TABLE multiple_prices (
    time TIMESTAMPTZ NOT NULL,
    carry NUMERIC(14, 5) NULL,
    carry_contract INTEGER NOT NULL,
    price NUMERIC(14, 5) NULL,
    price_contract INTEGER NOT NULL,
    forward NUMERIC(14, 5) NULL,
    forward_contract INTEGER NOT NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

CREATE TABLE roll_calendars (
    time TIMESTAMPTZ NOT NULL,
    current_contract INTEGER NOT NULL,
    next_contract INTEGER NOT NULL,
    carry_contract INTEGER NOT NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

COMMIT;
