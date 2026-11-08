from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_events():
    response = client.get('/events')
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]['capacity'] == 500
