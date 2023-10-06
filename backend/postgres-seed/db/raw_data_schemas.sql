CREATE TABLE adjusted_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    );

CREATE TABLE fx_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    );

CREATE TABLE multiple_prices (
                    unix_date_time INTEGER,
                    symbol VARCHAR(50),
                    carry FLOAT, 
                    carry_contract INTEGER, 
                    price FLOAT, 
                    price_contract INTEGER, 
                    forward FLOAT, 
                    forward_contract INTEGER,
                    PRIMARY KEY (unix_date_time, symbol)
                );

CREATE TABLE roll_calendars (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        current_contract INTEGER,
                        next_contract INTEGER,
                        carry_contract INTEGER,
                        PRIMARY KEY (unix_date_time, symbol)
                    );