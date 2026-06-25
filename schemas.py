#Pydantic models for request validation and response serialization (API schemas)
from pydantic import ConfigDict, Field, BaseModel
from datetime import date

class DailyMoodCreate(BaseModel):
    date: date
    happiness: int = Field(ge=0, le=10)
    energy: int = Field(ge=0, le=10)
    stressed: bool
    friends_family_time: bool
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)