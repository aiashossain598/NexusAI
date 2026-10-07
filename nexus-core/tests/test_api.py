from fastapi.testclient import TestClient

from app.server import app


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["service"] == "Nexus AI Core"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_system_endpoint():
    with TestClient(app) as client:
        response = client.get("/system/")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert "ram" in data
        assert "os" in data


def test_chat_endpoint_and_history():
    with TestClient(app) as client:
        response = client.post(
            "/api/chat/",
            json={"instruction": "Hello Nexus", "session_id": "test_api_session"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "response" in data

        history_resp = client.get("/api/chat/history/test_api_session")
        assert history_resp.status_code == 200
        history_data = history_resp.json()
        assert len(history_data["messages"]) >= 2


def test_websocket_chat():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            welcome = websocket.receive_json()
            assert welcome["type"] == "connected"

            websocket.send_json({"type": "ping"})
            pong = websocket.receive_json()
            assert pong["type"] == "pong"

            websocket.send_json({"type": "chat", "instruction": "Test message"})
            step = websocket.receive_json()
            assert "type" in step
