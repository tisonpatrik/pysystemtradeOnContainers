"""Update models

Revision ID: 1851fc2040e2
Revises: 32d099fd9188
Create Date: 2024-02-17 13:34:49.029412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1851fc2040e2'
down_revision: Union[str, None] = '32d099fd9188'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('normalised_price_for_asset_class')
    op.alter_column('fx_prices', 'unix_date_time',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('fx_prices', 'symbol',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fx_prices', 'symbol',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('fx_prices', 'unix_date_time',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    op.create_table('normalised_price_for_asset_class',
    sa.Column('unix_date_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('normalized_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['instrument_config.symbol'], name='normalised_price_for_asset_class_symbol_fkey'),
    sa.PrimaryKeyConstraint('unix_date_time', 'symbol', name='normalised_price_for_asset_class_pkey')
    )
    # ### end Alembic commands ###