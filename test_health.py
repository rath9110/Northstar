from fastapi.testclient import TestClient
from hello import app

client = TestClient(app)

def test_health_returns_200_when_db_reachable():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

"""  Run it with pytest test_health.py — it should fail right now (no /health route exists yet). That's correct.

  Your job is to make it pass by adding a /health endpoint to hello.py that:
  1. Uses psycopg2 to open a connection to your Postgres using the connection_string variable you already have
  2. Runs SELECT 1
  3. Closes the connection
  4. Returns {"status": "ok"} """