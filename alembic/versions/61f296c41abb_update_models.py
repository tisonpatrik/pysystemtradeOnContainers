"""Update models

Revision ID: 61f296c41abb
Revises: 2e91977cfb01
Create Date: 2024-03-16 11:17:19.199678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = '61f296c41abb'
down_revision: Union[str, None] = '2e91977cfb01'
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
