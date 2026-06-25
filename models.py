#SQLAlchemy column type maps to each field.
from sqlalchemy import Column, Integer, Boolean, Date, Text, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyMood(Base):
    __tablename__ = "daily_mood"
    date = Column(Date, primary_key=True)
    happiness = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    stressed = Column(Boolean, nullable=False)
    friends_family_time = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)
    __repr__ = f"<DailyMood(date={self.date}, happiness={self.happiness}, energy={self.energy}, stressed={self.stressed}, friends_family_time={self.friends_family_time}, notes={self.notes})>"

class DailyAutomatedData(Base):
    __tablename__ = "daily_automated_mood"
    date = Column(Date, primary_key=True)
    weather_code = Column(String, nullable=True)
    __repr__ = f"<DailyAutomatedData(date={self.date}, weather_code={self.weather_code})>"