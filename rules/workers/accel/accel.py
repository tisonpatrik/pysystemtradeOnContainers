import pandas as pd
from celery import Celery
from kombu import Queue
from shared.ewmac import ewmac

from common.src.logging.logger import AppLogger

app = Celery("rules", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

app.conf.task_queues = (Queue("accel"),)

app.conf.task_routes = {
    "rules.accel": {"queue": "accel"},
}

logger = AppLogger.get_instance().get_logger()


@app.task(name="rules.accel")
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
