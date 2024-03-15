"""Update models

Revision ID: b2fcc1cb57e2
Revises: 917b06740104
Create Date: 2024-03-10 12:14:07.044008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = 'b2fcc1cb57e2'
down_revision: Union[str, None] = '917b06740104'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fxpricesmodel',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrumentconfig.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('instrumentmetadata',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('asset_class', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('sub_class', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('sub_sub_class', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('style', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('country', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrumentconfig.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('multiplepricesmodel',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('carry', sa.Float(), nullable=False),
    sa.Column('carry_contract', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('price_contract', sa.Integer(), nullable=False),
    sa.Column('forward', sa.Float(), nullable=False),
    sa.Column('forward_contract', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrumentconfig.symbol'], ),
    sa.PrimaryKeyConstraint('date_time', 'symbol')
    )
    op.create_table('rollconfig',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('hold_roll_cycle', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('roll_offset_days', sa.Integer(), nullable=False),
    sa.Column('carry_offset', sa.Integer(), nullable=False),
    sa.Column('priced_roll_cycle', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiry_offset', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrumentconfig.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('spreadcosts',
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['instrumentconfig.symbol'], ),
    sa.PrimaryKeyConstraint('symbol')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spreadcosts')
    op.drop_table('rollconfig')
    op.drop_table('multiplepricesmodel')
    op.drop_table('instrumentmetadata')
    op.drop_table('fxpricesmodel')
    # ### end Alembic commands ###