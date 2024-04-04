import pandas as pd


class CumulativeVolNormalisedReturns:

    # SELECT id, hodnota, SUM(hodnota) OVER (ORDER BY id) AS cumsum FROM   tabulka;

    def get_cumulative_daily_vol_normalised_returns(
        self,   
        daily_vol_normalised_returns: pd.Series,
    ) -> pd.Series:
        """
        Returns a cumulative normalised return. This is like a price, but with equal expected vol
        Used for a few different trading rules
        """
        cum_norm_returns = daily_vol_normalised_returns.cumsum()

        return cum_norm_returns
