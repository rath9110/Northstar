""" "Happiness is "how happy did i feel today?", energy is "how much energy did I feel I had today?",
stress is "was i feeling stressed or not?" have it be yes no instead of 1-10, friends/family time is if I hung out
with them or not and then have notes be additional things I want to add such as "slept very late yesterday, drank,
etc" """

""" 
  1. What SQLAlchemy column type maps to each field — Integer, Boolean, String, Date, Text -> happiness: Integer, energy: Integer, stress: Boolean, friends/family time: Boolean, notes: Text
  2. Which columns are nullable=False (required) vs nullable=True (optional) -> all are nullable false except notes which is nullable true
  3. What the primary key is — think about what uniquely identifies a day  -> day_id that is a date and primary key
"""

from sqlalchemy import Column, Integer, Boolean, Date, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyMood(Base):
    __tablename__ = "daily_mood"
    date = Column("Date", Date, primary_key=True)
    happiness = Column("Happiness", Integer, nullable=False)
    energy = Column("Energy", Integer, nullable=False)
    stressed = Column("Stressed", Boolean, nullable=False)
    friends_family_time = Column("FriendsFamilyTime", Boolean, nullable=False)
    notes = Column("Notes", Text, nullable=True)