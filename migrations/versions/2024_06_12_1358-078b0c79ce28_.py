"""empty message

Revision ID: 078b0c79ce28
Revises: acc6cd9baa1d
Create Date: 2024-06-12 13:58:10.178973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '078b0c79ce28'
down_revision: Union[str, None] = 'acc6cd9baa1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
