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
    op.alter_column("daily_mood", "Date", new_column_name="date")
    op.alter_column("daily_mood", "Happiness", new_column_name="happiness")
    op.alter_column("daily_mood", "Energy", new_column_name="energy")
    op.alter_column("daily_mood", "Stressed", new_column_name="stressed")
    op.alter_column("daily_mood", "FriendsFamilyTime", new_column_name="friends_family_time")
    op.alter_column("daily_mood", "Notes", new_column_name="notes")

def downgrade() -> None:
    op.alter_column("daily_mood", "date", new_column_name="Date")
    op.alter_column("daily_mood", "happiness", new_column_name="Happiness")
    op.alter_column("daily_mood", "energy", new_column_name="Energy")
    op.alter_column("daily_mood", "stressed", new_column_name="Stressed")
    op.alter_column("daily_mood", "friends_family_time", new_column_name="FriendsFamilyTime")
    op.alter_column("daily_mood", "notes", new_column_name="Notes")
