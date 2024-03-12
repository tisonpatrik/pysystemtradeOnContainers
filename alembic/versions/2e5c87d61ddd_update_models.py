"""Update models

Revision ID: 2e5c87d61ddd
Revises: a35781fdd9e2
Create Date: 2024-03-12 09:56:24.600434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = '2e5c87d61ddd'
down_revision: Union[str, None] = 'a35781fdd9e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fxprices_symbol_fkey', 'fxprices', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fxprices_symbol_fkey', 'fxprices', 'instrumentconfig', ['symbol'], ['symbol'])
    # ### end Alembic commands ###
