from fastapi import FastAPI, status
from src.api.router import router
from src.core.config import settings
from src.db.sessions import init_db_async, drop_db_async

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {"Say": "Hello!"}

@app.get("/init_db", status_code=status.HTTP_200_OK, name="init_db")
async def initialize_db():
    logging.info("Soft database initialization process started.")
    await init_db_async()
    logging.info("Soft database initialization process completed.")
    return {"status": "Database softly initialized"}

@app.get("/drop_db", status_code=status.HTTP_200_OK, name="drop_db")
async def drop_db():
    logging.info("Drop of database started.")
    await drop_db_async()
    logging.info("Drop of database completed.")
    return {"status": "Database drop completed"}

