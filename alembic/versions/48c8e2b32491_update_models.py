"""Update models

Revision ID: 48c8e2b32491
Revises: 
Create Date: 2024-04-27 12:41:44.026277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '48c8e2b32491'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('daily_vol_normalised_price_for_asset_class',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('asset_class', sa.String(), nullable=False),
    sa.Column('vol_normalized_price_for_asset', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('date_time', 'asset_class')
    )
    op.create_table('fx_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index('ix_fx_prices_date_time', 'fx_prices', ['date_time'], unique=False)
    op.create_index(op.f('ix_fx_prices_symbol'), 'fx_prices', ['symbol'], unique=False)
    op.create_table('instrument_config',
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('pointsize', sa.Float(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('asset_class', sa.String(), nullable=True),
    sa.Column('per_block', sa.Float(), nullable=True),
    sa.Column('percentage', sa.Float(), nullable=True),
    sa.Column('per_trade', sa.Integer(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('adjusted_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_adjusted_prices_date_time'), 'adjusted_prices', ['date_time'], unique=False)
    op.create_index('ix_adjusted_prices_symbol', 'adjusted_prices', ['symbol'], unique=False)
    op.create_table('daily_returns_volatility',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('vol_returns', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_daily_returns_volatility_date_time'), 'daily_returns_volatility', ['date_time'], unique=False)
    op.create_table('daily_vol_normalized_returns',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('vol_normalized_returns', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('instrument_currency_volatility',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('instrument_volatility', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('instrument_metadata',
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('asset_class', sa.String(), nullable=True),
    sa.Column('sub_class', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('multiple_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('carry', sa.Float(), nullable=True),
    sa.Column('carry_contract', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('price_contract', sa.Integer(), nullable=True),
    sa.Column('forward', sa.Float(), nullable=True),
    sa.Column('forward_contract', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index('ix_multiple_prices_date_time', 'multiple_prices', ['date_time'], unique=False)
    op.create_index(op.f('ix_multiple_prices_symbol'), 'multiple_prices', ['symbol'], unique=False)
    op.create_table('roll_calendars',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('current_contract', sa.Integer(), nullable=True),
    sa.Column('next_contract', sa.Integer(), nullable=True),
    sa.Column('carry_contract', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_roll_calendars_date_time'), 'roll_calendars', ['date_time'], unique=False)
    op.create_index('ix_roll_calendars_symbol', 'roll_calendars', ['symbol'], unique=False)
    op.create_table('roll_config',
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('hold_roll_cycle', sa.String(), nullable=True),
    sa.Column('roll_offset_days', sa.Integer(), nullable=True),
    sa.Column('carry_offset', sa.Integer(), nullable=True),
    sa.Column('priced_roll_cycle', sa.String(), nullable=True),
    sa.Column('expiry_offset', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('spred_costs',
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('spread_costs', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spred_costs')
    op.drop_table('roll_config')
    op.drop_index('ix_roll_calendars_symbol', table_name='roll_calendars')
    op.drop_index(op.f('ix_roll_calendars_date_time'), table_name='roll_calendars')
    op.drop_table('roll_calendars')
    op.drop_index(op.f('ix_multiple_prices_symbol'), table_name='multiple_prices')
    op.drop_index('ix_multiple_prices_date_time', table_name='multiple_prices')
    op.drop_table('multiple_prices')
    op.drop_table('instrument_metadata')
    op.drop_table('instrument_currency_volatility')
    op.drop_table('daily_vol_normalized_returns')
    op.drop_index(op.f('ix_daily_returns_volatility_date_time'), table_name='daily_returns_volatility')
    op.drop_table('daily_returns_volatility')
    op.drop_index('ix_adjusted_prices_symbol', table_name='adjusted_prices')
    op.drop_index(op.f('ix_adjusted_prices_date_time'), table_name='adjusted_prices')
    op.drop_table('adjusted_prices')
    op.drop_table('instrument_config')
    op.drop_index(op.f('ix_fx_prices_symbol'), table_name='fx_prices')
    op.drop_index('ix_fx_prices_date_time', table_name='fx_prices')
    op.drop_table('fx_prices')
    op.drop_table('daily_vol_normalised_price_for_asset_class')
    # ### end Alembic commands ###