"""hypertables incomming

Revision ID: 27f7193cef55
Revises:
Create Date: 2024-08-12 23:00:27.064094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '27f7193cef55'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Create the table for storing real-time FX prices
    op.create_table(
        'fx_prices',
        sa.Column('time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('time', 'symbol')  # Set the primary key on 'time' and 'symbol'
    )

    # Convert the table to a hypertable
    op.execute("SELECT create_hypertable('fx_prices', 'time');")

    # Create an index on the symbol column, including time for better query performance
    op.create_index('ix_fx_prices_symbol_time', 'fx_prices', ['symbol', 'time DESC'], unique=False)


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

    op.create_table('rules',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('speed', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('name', 'speed')
    )


    op.create_table(
        'adjusted_prices',
        sa.Column('time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol']),
        sa.PrimaryKeyConstraint('time', 'symbol')  # Set the primary key on 'time' and 'symbol'
    )

    # Convert the table to a hypertable
    op.execute("SELECT create_hypertable('adjusted_prices', 'time');")

    # Create an index on the symbol column, including time for better query performance
    op.create_index('ix_adjusted_prices_symbol_time', 'adjusted_prices', ['symbol', 'time DESC'], unique=False)


    op.create_table('instrument_metadata',
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('asset_class', sa.String(), nullable=True),
        sa.Column('sub_class', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
        sa.PrimaryKeyConstraint('symbol')
    )

    op.create_table('multiple_prices',
        sa.Column('time', sa.DateTime(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('carry', sa.Float(), nullable=True),
        sa.Column('carry_contract', sa.Integer(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('price_contract', sa.Integer(), nullable=True),
        sa.Column('forward', sa.Float(), nullable=True),
        sa.Column('forward_contract', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
        sa.PrimaryKeyConstraint('time', 'symbol')
    )
    # Convert the table to a hypertable
    op.execute("SELECT create_hypertable('multiple_prices', 'time');")

    # Create an index on the symbol column, including time for better query performance
    op.create_index('ix_multiple_prices_symbol_time', 'multiple_prices', ['symbol', 'time DESC'], unique=False)

    op.create_table('roll_calendars',
        sa.Column('time', sa.DateTime(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('current_contract', sa.Integer(), nullable=True),
        sa.Column('next_contract', sa.Integer(), nullable=True),
        sa.Column('carry_contract', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], ),
        sa.PrimaryKeyConstraint('time', 'symbol')
    )

    # Convert the table to a hypertable
    op.execute("SELECT create_hypertable('roll_calendars', 'time');")

    # Create an index on the symbol column, including time for better query performance
    op.create_index('ix_roll_calendars_symbol_time', 'roll_calendars', ['symbol', 'time DESC'], unique=False)

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
    op.drop_index(op.f('ix_roll_calendars_symbol'), table_name='roll_calendars')
    op.drop_index(op.f('ix_roll_calendars_time'), table_name='roll_calendars')
    op.drop_table('roll_calendars')
    op.drop_index(op.f('ix_multiple_prices_symbol'), table_name='multiple_prices')
    op.drop_index(op.f('ix_multiple_prices_time'), table_name='multiple_prices')
    op.drop_table('multiple_prices')
    op.drop_table('instrument_metadata')
    op.drop_index(op.f('ix_adjusted_prices_symbol'), table_name='adjusted_prices')
    op.drop_index('ix_adjusted_prices_time', table_name='adjusted_prices')
    op.drop_table('adjusted_prices')
    op.drop_table('rules')
    op.drop_table('instrument_config')
    op.drop_index('ix_fx_prices_symbol', table_name='fx_prices')
    op.drop_index(op.f('ix_fx_prices_time'), table_name='fx_prices')
    op.drop_table('fx_prices')
    # ### end Alembic commands ###
