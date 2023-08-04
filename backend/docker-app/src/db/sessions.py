from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.db.tables.transactions import Transaction
from src.db.tables.multiple_prices import MultiplePrices

import pandas as pd
import os
import logging

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def create_tables_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    await create_transaction_async()

async def create_transaction_async():
    transaction = Transaction(amount=10, description="First transaction")
    async with async_session() as session:
        session.add(transaction)
        await session.commit()


def transform_csv_to_schema(file_path, symbol):
    """Transforms a given CSV file to match the MultiplePrices schema."""
    df = pd.read_csv(file_path)

    # Transforming the DATETIME column into UNIX timestamp
    df["UNIX_TIMESTAMP"] = pd.to_datetime(df["DATETIME"]).astype(int) // 10**9
    
    # Adding the SYMBOL column
    df["SYMBOL"] = symbol

    # Dropping the original DATETIME column
    df.drop(columns=["DATETIME"], inplace=True)

    # Reordering the columns to match the MultiplePrices schema
    df = df[["UNIX_TIMESTAMP", "SYMBOL", "CARRY", "CARRY_CONTRACT", "PRICE", "PRICE_CONTRACT", "FORWARD", "FORWARD_CONTRACT"]]

    return df

async def seed_grayfox_db_async():
    directory_path = "/path/in/container" + "/multiple_prices_csv"
    logging.info("Seeding of multiple_prices table started.")
    async with async_session() as session:
        logging.info("Checking files in the directory.")
        for file in os.listdir(directory_path):
            if file.endswith(".csv"):
                symbol = file.split(".")[0]
                logging.info(f"Processing file: {file}")
                transformed_data = transform_csv_to_schema(f"{directory_path}/{file}", symbol)
                logging.info(f"Number of rows processed from {file}: {len(transformed_data)}")
                
                for _, row in transformed_data.iterrows():
                    multiple_price = MultiplePrices(**row.to_dict())
                    session.add(multiple_price)
                
                await session.commit()
                logging.info(f"Committing data from file {file}")
                logging.info(f"Data from file {file} has been successfully written to the database.")
        logging.info("Finished processing all files.")

async def init_db_async():
    # Check if tables exist
    tables_exist = await check_tables_exist()
    
    # If tables don't exist, create them
    if not tables_exist:
        await create_tables_async()
        await seed_grayfox_db_async()
    else:
        # Check if tables are empty
        multiple_prices_empty = await check_table_empty(MultiplePrices)
        transactions_empty = await check_table_empty(Transaction)
        
        # If tables are empty, seed them
        if multiple_prices_empty:
            await seed_grayfox_db_async()
        if transactions_empty:
            await create_transaction_async()

async def reset_db_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await create_tables_async()
    await seed_grayfox_db_async()

async def check_tables_exist():
    async with async_engine.begin() as conn:
        try:
            # Try to fetch one row from the table to check its existence
            await conn.execute(select(MultiplePrices).limit(1))
            return True
        except Exception:
            return False
        
async def check_table_empty(table):
    async with async_session() as session:
        count = await session.execute(select(func.count()).select_from(table))
        return count.scalar() == 0
