CREATE TABLE roll_config (
                    symbol VARCHAR(50) PRIMARY KEY,
                    hold_roll_cycle VARCHAR(50),
                    roll_offset_days INTEGER,
                    carry_offset INTEGER,
                    priced_roll_cycle VARCHAR(50),
                    expiry_offset INTEGER
                )