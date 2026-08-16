import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.ai.router import AIRouter
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.exceptions import AIProviderError

@pytest.fixture
def mock_settings():
    with patch("app.services.ai.router.settings") as settings:
        settings.AI_ROUTING_POLICY = "FREE_ONLY"
        settings.OPENAI_API_KEY = "test-openai"
        settings.OPENROUTER_API_KEY = "test-openrouter"
        settings.GEMINI_API_KEY = "test-gemini"
        yield settings

@pytest.mark.asyncio
async def test_router_free_only(mock_settings):
    router = AIRouter()
    req = AIRequest(messages=[{"role": "user", "content": "Hi"}], model="test")
    
    with patch.object(router, "_try_provider") as mock_try:
        mock_try.return_value = AIResponse(content="Success", provider="ollama", model="llama3", usage={}, latency=0.1)
        resp = await router.generate(req)
        mock_try.assert_called_once_with("ollama", req)
        assert resp.provider == "ollama"

@pytest.mark.asyncio
async def test_router_fallback(mock_settings):
    mock_settings.AI_ROUTING_POLICY = "FREE_FIRST"
    router = AIRouter()
    req = AIRequest(messages=[{"role": "user", "content": "Hi"}], model="test")
    
    with patch.object(router, "_try_provider") as mock_try:
        mock_try.side_effect = [AIProviderError("Failed"), AIResponse(content="Success", provider="openrouter", model="test", usage={}, latency=0.1)]
        resp = await router.generate(req)
        assert mock_try.call_count == 2
        assert resp.provider == "openrouter"
