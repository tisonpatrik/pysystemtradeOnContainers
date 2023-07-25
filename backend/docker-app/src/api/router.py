from fastapi import APIRouter

from src.api.routes.transactions import router as transactions_router

router = APIRouter()

router.include_router(transactions_router, prefix="/transactions")
