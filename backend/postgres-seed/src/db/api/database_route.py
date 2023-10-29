"""
This module defines the reset_database API route for a FastAPI application.
It includes a POST endpoint that resets all database tables to their initial state.
"""

# FastAPI and SQLAlchemy dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.handlers.database_handler import DatabaseHandler

# Application-specific dependencies
from src.db.settings.database import get_db

# Create a FastAPI router instance
router = APIRouter()


@router.post("/reset_db/", status_code=status.HTTP_201_CREATED, name="Reset Database")
async def reset_database(db_session: AsyncSession = Depends(get_db)):
    """
    Resets all tables in the database to their initial state.
    """
    try:
        db_handler = DatabaseHandler(db_session)
        await db_handler.truncate_tables_async()
        return {"status": "success", "message": "Database was reset."}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc


@router.get("/list_tables/", status_code=status.HTTP_200_OK, name="List Tables")
async def list_tables(db_session: AsyncSession = Depends(get_db)):
    """
    Returns a list of all table names in the database.
    """
    try:
        db_handler = DatabaseHandler(db_session)
        tables = await db_handler.list_tables_async()
        return {"tables": tables}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc
