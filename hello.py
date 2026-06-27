import fastapi 
from fastapi import Depends, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from database import get_db
from schemas import DailyMoodCreate
from models import DailyMood
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION")

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.post("/mood")
def create_mood(mood: DailyMoodCreate, db = Depends(get_db)):
    stmt = insert(DailyMood).values(
        date=mood.date,
        happiness=mood.happiness,
        energy=mood.energy,
        stressed=mood.stressed,
        friends_family_time=mood.friends_family_time,
        notes=mood.notes
    )
    
    stmt = stmt.on_conflict_do_update(
        index_elements=['date'],
        set_={
            "happiness": stmt.excluded.happiness,
            "energy": stmt.excluded.energy,
            "stressed": stmt.excluded.stressed,
            "friends_family_time": stmt.excluded.friends_family_time,
            "notes": stmt.excluded.notes
        }
    )
    db.execute(stmt)
    db.commit()
    return db.get(DailyMood, mood.date)

@app.get("/mood")
def get_moods(db = Depends(get_db)):
    moods = db.query(DailyMood).all()
    return moods


@app.get("/mood/{date}")
def get_mood_by_date(date: str, db = Depends(get_db)):
    mood = db.get(DailyMood, date)
    if mood is None:
        raise HTTPException(status_code=404, detail="Mood entry not found for the given date.")
    return mood

@app.delete("/mood/{date}")
def delete_mood(date: str, db = Depends(get_db)):
    mood = db.get(DailyMood, date)
    if mood is None:
        raise HTTPException(status_code=404, detail="Mood entry not found for the given date.")
    db.delete(mood)
    db.commit()
    return {"message": "Mood entry deleted successfully."}
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
