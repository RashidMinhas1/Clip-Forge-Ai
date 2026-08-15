import os
import pytest
from app.core.config import Settings

def test_config_defaults():
    # To test defaults cleanly, we can instantiate Settings directly
    # However, pydantic-settings reads from environment.
    # We can pass empty env to force defaults if needed, 
    # but instantiating it usually uses current env.
    settings = Settings(_env_file=None)
    
    assert settings.ENVIRONMENT in ["development", "production", "test"]
    assert settings.BACKEND_PORT == 8000

def test_cors_origins_parsing():
    os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000", "https://example.com"]'
    settings = Settings(_env_file=None)
    assert "http://localhost:3000" in settings.BACKEND_CORS_ORIGINS
    assert "https://example.com" in settings.BACKEND_CORS_ORIGINS
    del os.environ["BACKEND_CORS_ORIGINS"]
