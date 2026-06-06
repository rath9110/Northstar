import fastapi 
from fastapi import Depends
import uvicorn
import os
from dotenv import load_dotenv
from database import get_db
from schemas import DailyMoodCreate
from models import DailyMood
from sqlalchemy.dialects.postgresql import insert

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
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
