BEGIN;

-- Create adjusted_prices table with foreign key reference
CREATE TABLE adjusted_prices (
    time TIMESTAMPTZ NOT NULL,
    price NUMERIC(14, 3) NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

-- Create fx_prices table with foreign key reference
CREATE TABLE fx_prices (
    time TIMESTAMPTZ NOT NULL,
    price NUMERIC(14, 3) NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

-- Create multiple_prices table with foreign key reference
CREATE TABLE multiple_prices (
    time TIMESTAMPTZ NOT NULL,
    carry NUMERIC(14, 3) NULL,
    carry_contract INTEGER NOT NULL,
    price NUMERIC(14, 3) NULL,
    price_contract INTEGER NOT NULL,
    forward NUMERIC(14, 3) NULL,
    forward_contract INTEGER NOT NULL,
    symbol VARCHAR NOT NULL,
    PRIMARY KEY (time, symbol),
    FOREIGN KEY (symbol) REFERENCES instrument_config(symbol)
);

-- Create roll_calendars table with foreign key reference
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
