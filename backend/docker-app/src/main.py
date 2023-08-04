from fastapi import FastAPI, BackgroundTasks, status
from src.api.router import router
from src.core.config import settings
from src.db.sessions import create_tables_async, seed_grayfox_db_async, init_db_async, reset_db_async

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

@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    logging.info("Table initialization process started.")
    await create_tables_async()
    await seed_grayfox_db_async()
    logging.info("Table initialization process completed.")
    return {"status": "Initialization completed"}


@app.get("/init_db", status_code=status.HTTP_200_OK, name="init_db")
async def initialize_db():
    logging.info("Soft database initialization process started.")
    await init_db_async()
    logging.info("Soft database initialization process completed.")
    return {"status": "Database softly initialized"}

@app.get("/reset_db", status_code=status.HTTP_200_OK, name="reset_db")
async def hard_reset_db():
    logging.info("Hard reset of database started.")
    await reset_db_async()
    logging.info("Hard reset of database completed.")
    return {"status": "Database hard reset completed"}
