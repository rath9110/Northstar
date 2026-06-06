"""rename columns to snake_case

Revision ID: 47ac42fbf6c2
Revises: b16afe8f640d
Create Date: 2026-06-06 22:37:51.825569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ac42fbf6c2'
down_revision: Union[str, Sequence[str], None] = 'b16afe8f640d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
