"""start

Revision ID: b2bd5436658f
Revises: 99b4381e400d
Create Date: 2025-06-07 18:56:25.274343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2bd5436658f'
down_revision: Union[str, None] = '99b4381e400d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
