from fastapi.testclient import TestClient
from app import app
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "App is running"}
def test_health():
    response = client.get("/health_status")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}