"""empty message

Revision ID: fccf943ad443
Revises: b2bd5436658f
Create Date: 2025-06-08 17:00:57.422833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fccf943ad443'
down_revision: Union[str, None] = 'b2bd5436658f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
