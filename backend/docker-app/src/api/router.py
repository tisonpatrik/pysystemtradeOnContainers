from fastapi import APIRouter

from src.api.routes.route_transactions import router as transactions_router
from src.api.routes.route_data import router as data_router
router = APIRouter()

router.include_router(transactions_router, prefix="/transactions")
router.include_router(data_router, prefix="/data")