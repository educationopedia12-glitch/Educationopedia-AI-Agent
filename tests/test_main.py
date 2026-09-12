"""
Milestone 1 sanity tests: app boots, health/root endpoints work,
and the /chat router is actually mounted.

Run with:
    pytest tests/test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import APP_NAME, APP_VERSION, ENVIRONMENT

client = TestClient(app)


class TestRootEndpoint:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_has_expected_keys(self):
        data = client.get("/").json()
        assert set(data.keys()) == {"message", "environment", "version"}

    def test_root_values_match_config(self):
        data = client.get("/").json()
        assert APP_NAME in data["message"]
        assert data["environment"] == ENVIRONMENT
        assert data["version"] == APP_VERSION


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_is_healthy(self):
        data = client.get("/health").json()
        assert data == {"status": "healthy"}


class TestChatRouterMounted:
    """
    We don't know the exact request/response schema of /chat yet
    (that's Milestone 1 Tasks 6-7), so this is a smoke test only:
    it just confirms the route exists and isn't a 404.
    """

    def test_chat_route_exists(self):
        response = client.post("/chat", json={"message": "hello"})
        assert response.status_code != 404

    def test_chat_rejects_garbage_payload_gracefully(self):
        # Should not 500 on bad input - either 422 (validation) or handled error
        response = client.post("/chat", json={"nonsense_field": 123})
        assert response.status_code in (200, 400, 422)


class TestOpenAPISchema:
    """Cheap way to catch broken route registration / import errors."""

    def test_openapi_schema_loads(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_expected_paths_registered(self):
        schema = client.get("/openapi.json").json()
        paths = schema["paths"].keys()
        assert "/" in paths
        assert "/health" in paths
        assert "/chat" in paths