import fastapi 
from fastapi import Depends
import uvicorn
import os
from dotenv import load_dotenv
from database import get_db
from schemas import DailyMoodCreate
from models import DailyMood

load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION")

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health(db = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/mood")
def create_mood(mood: DailyMoodCreate, db = Depends(get_db)):
    if mood is None:
        return {"error": "Invalid mood data"}

    db_mood = DailyMood(
        date=mood.date,
        happiness=mood.happiness,
        energy=mood.energy,
        stressed=mood.stressed,
        friends_family_time=mood.friends_family_time,
        notes=mood.notes
    )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return db_mood
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
