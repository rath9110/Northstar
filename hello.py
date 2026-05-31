#packages
import fastapi
import uvicorn
import sqlalchemy
import psycopg2
import os
os.getenv("connection_string")

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
