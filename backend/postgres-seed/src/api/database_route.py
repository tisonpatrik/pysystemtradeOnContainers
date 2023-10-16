"""
This module defines the reset_database API route for a FastAPI application.
It includes a POST endpoint that resets all database tables to their initial state.
"""

# FastAPI and SQLAlchemy dependencies
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Application-specific dependencies
from src.database import get_db
from src.handlers.database_handler import DatabaseHandler

# Create a FastAPI router instance
router = APIRouter()


@router.post("/reset_db/", status_code=status.HTTP_201_CREATED, name="Reset Database")
async def reset_database(db_session: AsyncSession = Depends(get_db)):
    """
    Resets all tables in the database to their initial state.
    """
    try:
        db_handler = DatabaseHandler(db_session)
        await db_handler.reset_tables_async()
        return {"status": "success", "message": "Database was reset."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
