from fastapi import APIRouter

from src.api.routes.route_data import router as data_router
from src.api.routes.config_files_route import router as config_files_router
router = APIRouter()

router.include_router(data_router, prefix="/data")
router.include_router(config_files_router, prefix="/config_files")