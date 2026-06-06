"""rename columns to snake_case

Revision ID: b16afe8f640d
Revises: 38863abd78db
Create Date: 2026-06-06 22:33:15.743058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b16afe8f640d'
down_revision: Union[str, Sequence[str], None] = '38863abd78db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
