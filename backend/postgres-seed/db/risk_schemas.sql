CREATE TABLE robust_volatility (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        volatility FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )