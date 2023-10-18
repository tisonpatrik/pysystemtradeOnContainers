from fastapi import APIRouter, status

from src.api.utils import execute_with_logging_async
from src.db.settings.config import settings
from src.handlers.risk_handler import RiskHandler

router = APIRouter()
seed_db_handler = RiskHandler(settings.database_url)


@router.post(
    "/risk_calculator/", status_code=status.HTTP_200_OK, name="risk_calculator"
)
async def fill_database():
    await execute_with_logging_async(
        seed_db_handler.calculate_and_insert_risk_for_all_dataset_async,
        start_msg="Database table filling started.",
        end_msg="Database table filling completed.",
    )
    return {"status": "Table was filled with data from temp folder"}
