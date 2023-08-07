from fastapi import APIRouter, status

from src.db.sessions import init_db_async, drop_db_async

import logging

router = APIRouter()

@router.get("/init_db", status_code=status.HTTP_200_OK, name="init_db")
async def initialize_db():
    logging.info("Soft database initialization process started.")
    await init_db_async()  # Assuming you have this function defined somewhere
    logging.info("Soft database initialization process completed.")
    return {"status": "Database softly initialized"}

@router.get("/drop_db", status_code=status.HTTP_200_OK, name="drop_db")
async def drop_db():
    logging.info("Drop of database started.")
    await drop_db_async()  # Assuming you have this function defined somewhere
    logging.info("Drop of database completed.")
    return {"status": "Database drop completed"}
