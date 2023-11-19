"""empty message

Revision ID: 4bf57d5ce382
Revises: f48d93b34044
Create Date: 2023-11-19 23:37:38.317852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bf57d5ce382'
down_revision: Union[str, None] = 'f48d93b34044'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
