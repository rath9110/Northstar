import fastapi 
import uvicorn 
import sqlalchemy
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Boolean, String, Date, Text
from sqlalchemy.orm import declarative_base
load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION")

base = declarative_base()

class SomeClass(base):
    __tablename__ = "some_table"
    id = Column("Date", Date, primary_key=True)
    happiness = Column("Happiness", Integer, nullable=False)
    energy = Column("Energy", Integer, nullable=False)
    stress = Column("Stress", Integer, nullable=False)
    friends_family_time = Column("FriendsFamilyTime", Integer, nullable=False)
    notes = Column("Notes", Text, nullable=True)

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
