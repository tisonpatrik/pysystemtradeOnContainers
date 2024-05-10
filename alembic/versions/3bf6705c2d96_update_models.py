"""Update models

Revision ID: 3bf6705c2d96
Revises: 48c8e2b32491
Create Date: 2024-05-09 22:57:37.669477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3bf6705c2d96'
down_revision: Union[str, None] = '48c8e2b32491'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rules',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('name', 'speed')
    )
    op.drop_table('instrument_currency_volatility')
    op.drop_index('ix_daily_returns_volatility_date_time', table_name='daily_returns_volatility')
    op.drop_table('daily_returns_volatility')
    op.drop_table('daily_vol_normalised_price_for_asset_class')
    op.drop_table('daily_vol_normalized_returns')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('daily_vol_normalized_returns',
    sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('vol_normalized_returns', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='daily_vol_normalized_returns_symbol_fkey'),
    sa.PrimaryKeyConstraint('date_time', 'symbol', name='daily_vol_normalized_returns_pkey')
    )
    op.create_table('daily_vol_normalised_price_for_asset_class',
    sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('asset_class', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('vol_normalized_price_for_asset', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('date_time', 'asset_class', name='daily_vol_normalised_price_for_asset_class_pkey')
    )
    op.create_table('daily_returns_volatility',
    sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('vol_returns', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='daily_returns_volatility_symbol_fkey'),
    sa.PrimaryKeyConstraint('date_time', 'symbol', name='daily_returns_volatility_pkey')
    )
    op.create_index('ix_daily_returns_volatility_date_time', 'daily_returns_volatility', ['date_time'], unique=False)
    op.create_table('instrument_currency_volatility',
    sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('instrument_volatility', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='instrument_currency_volatility_symbol_fkey'),
    sa.PrimaryKeyConstraint('date_time', 'symbol', name='instrument_currency_volatility_pkey')
    )
    op.drop_table('rules')
    # ### end Alembic commands ###
