import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.utils.ewmac import ewmac

logger = AppLogger.get_instance().get_logger()


def accel(price: pd.Series, vol: pd.Series, Lfast: int) -> pd.Series:
    try:
        Lslow = Lfast * 4
        logger.info(f"Calculating EWMAC signal with Lfast={Lfast}, Lslow={Lslow}")
        ewmac_signal = ewmac(price, vol, Lfast, Lslow)

        logger.info("Calculating acceleration")
        accel = ewmac_signal - ewmac_signal.shift(Lfast)

        logger.info("Calculation successful")
        return accel

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
