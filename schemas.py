from pydantic import BaseModel
from datetime import date


class DailyMoodCreate(BaseModel):
    date: date
    happiness: int
    energy: int
    stressed: bool
    friends_family_time: bool
    notes: str | None = None
