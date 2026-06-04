import fastapi 
from fastapi import Depends
import uvicorn
import os
from dotenv import load_dotenv
from database import get_db

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
def create_mood(db = Depends(get_db)):
    pass
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
