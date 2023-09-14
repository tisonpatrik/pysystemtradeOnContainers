from fastapi import APIRouter

from src.api.routes.route_data import router as data_router
router = APIRouter()

router.include_router(data_router, prefix="/data")