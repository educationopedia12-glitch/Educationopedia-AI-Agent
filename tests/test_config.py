"""
Tests for app/config.py

Because config values are read from the environment at *import time*,
we reload the module inside each test after patching os.environ.
Otherwise every test would just see whatever was cached on first import.
"""
import importlib
import sys

import pytest


def reload_config():
    """Force a fresh import of app.config so env var patches take effect."""
    if "app.config" in sys.modules:
        del sys.modules["app.config"]
    import app.config as config
    return config


class TestDefaults:
    """No env vars set -> should fall back to hardcoded defaults."""

    def test_default_app_name(self, monkeypatch):
        monkeypatch.delenv("APP_NAME", raising=False)
        config = reload_config()
        assert config.APP_NAME == "Educationopedia AI Agent"

    def test_default_app_version(self, monkeypatch):
        monkeypatch.delenv("APP_VERSION", raising=False)
        config = reload_config()
        assert config.APP_VERSION == "0.1.0"

    def test_default_environment(self, monkeypatch):
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        config = reload_config()
        assert config.ENVIRONMENT == "development"

    def test_default_openrouter_model(self, monkeypatch):
        monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
        config = reload_config()
        assert config.OPENROUTER_MODEL == "openrouter/free"

    def test_default_openrouter_key_is_none_if_unset(self, monkeypatch):
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
        config = reload_config()
        assert config.OPENROUTER_API_KEY is None


class TestEnvOverrides:
    """Env vars set -> config should reflect them, not the defaults."""

    def test_app_name_override(self, monkeypatch):
        monkeypatch.setenv("APP_NAME", "Test Agent")
        config = reload_config()
        assert config.APP_NAME == "Test Agent"

    def test_app_version_override(self, monkeypatch):
        monkeypatch.setenv("APP_VERSION", "9.9.9")
        config = reload_config()
        assert config.APP_VERSION == "9.9.9"

    def test_environment_override(self, monkeypatch):
        monkeypatch.setenv("ENVIRONMENT", "production")
        config = reload_config()
        assert config.ENVIRONMENT == "production"

    def test_openrouter_api_key_override(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test-12345")
        config = reload_config()
        assert config.OPENROUTER_API_KEY == "sk-test-12345"

    def test_openrouter_model_override(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_MODEL", "some/other-model")
        config = reload_config()
        assert config.OPENROUTER_MODEL == "some/other-model"


class TestHardcodedConstants:
    """
    These aren't read from env vars at all - they're plain constants.
    If someone accidentally makes them configurable later, or changes
    the value without realizing it affects token usage, this should
    catch it.
    """

    def test_max_history_messages_value(self, monkeypatch):
        config = reload_config()
        assert config.MAX_HISTORY_MESSAGES == 10

    def test_max_history_messages_is_int(self, monkeypatch):
        config = reload_config()
        assert isinstance(config.MAX_HISTORY_MESSAGES, int)

    def test_rag_ingestion_batch_size_value(self, monkeypatch):
        config = reload_config()
        assert config.RAG_INGESTION_BATCH_SIZE == 50

    def test_rag_ingestion_batch_size_is_int(self, monkeypatch):
        config = reload_config()
        assert isinstance(config.RAG_INGESTION_BATCH_SIZE, int)


@pytest.fixture(autouse=True)
def _cleanup_config_module():
    """
    Ensure app.config is freshly reloaded before each test, so leftover
    monkeypatch env vars from a previous test can't leak into imports
    that happen outside these tests (e.g. app.main importing app.config).
    """
    yield
    if "app.config" in sys.modules:
        del sys.modules["app.config"]
    importlib.import_module("app.config")