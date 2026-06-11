"""change weather_code to string

Revision ID: ae8fee6726c7
Revises: 22e1ddf05db5
Create Date: 2026-06-11 21:34:17.596121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae8fee6726c7'
down_revision: Union[str, Sequence[str], None] = '22e1ddf05db5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
    "daily_mood",
    "weather_code",
    type_=sa.String(),
    existing_type=sa.Integer(),
    existing_nullable=True,
    postgresql_using="weather_code::varchar",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
    "daily_mood",
    "weather_code",
    type_=sa.Integer(),
    existing_type=sa.String(),
    existing_nullable=True,
    postgresql_using="weather_code::integer",
    )
