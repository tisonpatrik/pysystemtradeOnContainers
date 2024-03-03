"""Update models

Revision ID: 35f1f0bbf609
Revises: dd32d513232c
Create Date: 2024-03-03 14:24:04.855708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35f1f0bbf609'
down_revision: Union[str, None] = 'dd32d513232c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fx_prices')
    op.drop_table('instrument_metadata')
    op.drop_table('roll_calendars')
    op.drop_table('roll_config')
    op.drop_table('daily_vol_normalised_price_for_asset_class')
    op.drop_table('tradable_instruments')
    op.drop_table('daily_returns_volatility')
    op.drop_table('spread_costs')
    op.drop_table('daily_vol_normalized_returns')
    op.drop_table('multiple_prices')
    op.drop_table('instrument_volatility')
    op.drop_table('adjusted_prices')
    op.drop_table('instrument_config')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instrument_config',
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('pointsize', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('asset_class', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('per_block', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('percentage', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('per_trade', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('region', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('symbol', name='instrument_config_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('adjusted_prices',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='adjusted_prices_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='adjusted_prices_pkey')
    )
    op.create_table('instrument_volatility',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('instrument_volatility', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='instrument_volatility_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='instrument_volatility_pkey')
    )
    op.create_table('multiple_prices',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('carry', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('carry_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('price_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('forward', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('forward_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='multiple_prices_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='multiple_prices_pkey')
    )
    op.create_table('daily_vol_normalized_returns',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('normalized_volatility', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='daily_vol_normalized_returns_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='daily_vol_normalized_returns_pkey')
    )
    op.create_table('spread_costs',
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('spread_costs', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='spread_costs_symbol_fkey'),
    sa.PrimaryKeyConstraint('symbol', name='spread_costs_pkey')
    )
    op.create_table('daily_returns_volatility',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('daily_returns_volatility', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='daily_returns_volatility_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='daily_returns_volatility_pkey')
    )
    op.create_table('tradable_instruments',
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('symbol', name='tradable_instruments_pkey')
    )
    op.create_table('daily_vol_normalised_price_for_asset_class',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('asset_class', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('normalized_volatility', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('unix_date_time', 'asset_class', name='daily_vol_normalised_price_for_asset_class_pkey')
    )
    op.create_table('roll_config',
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('hold_roll_cycle', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('roll_offset_days', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('carry_offset', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('priced_roll_cycle', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('expiry_offset', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='roll_config_symbol_fkey'),
    sa.PrimaryKeyConstraint('symbol', name='roll_config_pkey')
    )
    op.create_table('roll_calendars',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('current_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('next_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('carry_contract', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='roll_calendars_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='roll_calendars_pkey')
    )
    op.create_table('instrument_metadata',
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('asset_class', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('sub_class', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('sub_sub_class', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('style', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('duration', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='instrument_metadata_symbol_fkey'),
    sa.PrimaryKeyConstraint('symbol', name='instrument_metadata_pkey')
    )
    op.create_table('fx_prices',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False)
    )
    # ### end Alembic commands ###
