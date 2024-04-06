"""Update models

Revision ID: 149e37c02786
Revises: 
Create Date: 2024-04-06 17:18:43.291116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = '149e37c02786'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('daily_vol_normalised_price_for_asset_class',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('asset_clas', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('vol_normalized_price_for_asset', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('date_time')
    )
    op.create_table('fx_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_fx_prices_date_time'), 'fx_prices', ['date_time'], unique=False)
    op.create_index(op.f('ix_fx_prices_symbol'), 'fx_prices', ['symbol'], unique=False)
    op.create_table('instrument_config',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pointsize', sa.Float(), nullable=False),
    sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('asset_class', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('per_block', sa.Float(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=False),
    sa.Column('per_trade', sa.Integer(), nullable=False),
    sa.Column('region', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('adjusted_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_adjusted_prices_date_time'), 'adjusted_prices', ['date_time'], unique=False)
    op.create_index(op.f('ix_adjusted_prices_symbol'), 'adjusted_prices', ['symbol'], unique=False)
    op.create_table('daily_returns_volatility',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('vol_returns', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_daily_returns_volatility_date_time'), 'daily_returns_volatility', ['date_time'], unique=False)
    op.create_table('daily_vol_normalized_returns',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('vol_normalized_returns', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('instrument_metadata',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('asset_class', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('sub_class', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('instrument_volatility',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('instrument_volatility', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('multiple_prices',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('carry', sa.Float(), nullable=True),
    sa.Column('carry_contract', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('price_contract', sa.Integer(), nullable=False),
    sa.Column('forward', sa.Float(), nullable=True),
    sa.Column('forward_contract', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_multiple_prices_date_time'), 'multiple_prices', ['date_time'], unique=False)
    op.create_index(op.f('ix_multiple_prices_symbol'), 'multiple_prices', ['symbol'], unique=False)
    op.create_table('roll_calendars',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('current_contract', sa.Integer(), nullable=False),
    sa.Column('next_contract', sa.Integer(), nullable=False),
    sa.Column('carry_contract', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_index(op.f('ix_roll_calendars_date_time'), 'roll_calendars', ['date_time'], unique=False)
    op.create_index(op.f('ix_roll_calendars_symbol'), 'roll_calendars', ['symbol'], unique=False)
    op.create_table('roll_config',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('hold_roll_cycle', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('roll_offset_days', sa.Integer(), nullable=False),
    sa.Column('carry_offset', sa.Integer(), nullable=False),
    sa.Column('priced_roll_cycle', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiry_offset', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('spred_costs',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('spread_costs', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spred_costs')
    op.drop_table('roll_config')
    op.drop_index(op.f('ix_roll_calendars_symbol'), table_name='roll_calendars')
    op.drop_index(op.f('ix_roll_calendars_date_time'), table_name='roll_calendars')
    op.drop_table('roll_calendars')
    op.drop_index(op.f('ix_multiple_prices_symbol'), table_name='multiple_prices')
    op.drop_index(op.f('ix_multiple_prices_date_time'), table_name='multiple_prices')
    op.drop_table('multiple_prices')
    op.drop_table('instrument_volatility')
    op.drop_table('instrument_metadata')
    op.drop_table('daily_vol_normalized_returns')
    op.drop_index(op.f('ix_daily_returns_volatility_date_time'), table_name='daily_returns_volatility')
    op.drop_table('daily_returns_volatility')
    op.drop_index(op.f('ix_adjusted_prices_symbol'), table_name='adjusted_prices')
    op.drop_index(op.f('ix_adjusted_prices_date_time'), table_name='adjusted_prices')
    op.drop_table('adjusted_prices')
    op.drop_table('instrument_config')
    op.drop_index(op.f('ix_fx_prices_symbol'), table_name='fx_prices')
    op.drop_index(op.f('ix_fx_prices_date_time'), table_name='fx_prices')
    op.drop_table('fx_prices')
    op.drop_table('daily_vol_normalised_price_for_asset_class')
    # ### end Alembic commands ###
