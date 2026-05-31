import fastapi 
import uvicorn 
import sqlalchemy
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION")

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
