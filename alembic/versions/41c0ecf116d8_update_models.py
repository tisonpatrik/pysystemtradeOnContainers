"""Update models

Revision ID: 41c0ecf116d8
Revises: 8b6edbeb4fd5
Create Date: 2024-03-15 20:55:13.469260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = '41c0ecf116d8'
down_revision: Union[str, None] = '8b6edbeb4fd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
