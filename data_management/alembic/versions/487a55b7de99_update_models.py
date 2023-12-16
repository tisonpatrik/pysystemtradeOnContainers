"""Update models

Revision ID: 487a55b7de99
Revises: a18d20193348
Create Date: 2023-12-16 20:57:38.490420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '487a55b7de99'
down_revision: Union[str, None] = 'a18d20193348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fx_prices_symbol_fkey', 'fx_prices', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fx_prices_symbol_fkey', 'fx_prices', 'instrument_config', ['symbol'], ['symbol'])
    # ### end Alembic commands ###
