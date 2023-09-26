import asyncpg
from fastapi import Depends, HTTPException
from contextlib import asynccontextmanager
from src.db.database import Database
from src.core.config import settings

db = Database(settings.database_url)

@asynccontextmanager 
async def get_db():
    await db.connect()
    conn = await db.get_conn()
    try:
        yield conn
    finally:
        await db.release_conn(conn)

async def get_conn() -> asyncpg.Connection:
    async with get_db() as connection:
        if connection is None:
            raise HTTPException(status_code=500, detail="Could not connect to database.")
        yield connection

def get_repository(repository):
    def _get_repository(conn: asyncpg.Connection = Depends(get_conn)):
        return repository(conn)
    return _get_repository