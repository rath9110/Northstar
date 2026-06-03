import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION")
engine = create_engine(connection_string)
SessionLocal = sessionmaker(engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()