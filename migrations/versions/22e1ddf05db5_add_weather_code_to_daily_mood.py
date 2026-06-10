"""add weather_code to daily_mood

Revision ID: 22e1ddf05db5
Revises: 47ac42fbf6c2
Create Date: 2026-06-08 21:49:30.833102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22e1ddf05db5'
down_revision: Union[str, Sequence[str], None] = '47ac42fbf6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("weather_code", sa.String(), nullable=True)


def downgrade() -> None:
    op.add_column("daily_mood", sa.Column("weather_code", sa.Integer(), nullable=True))