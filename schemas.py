
from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date

class DailyMoodCreate(BaseModel):
    date: date
    happiness: int
    energy: int
    stressed: bool
    friends_family_time: bool
    notes: str | None = None
    weather: str | None = None

    model_config = ConfigDict(from_attributes=True)