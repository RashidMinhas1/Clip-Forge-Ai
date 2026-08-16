import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import httpx
from app.services.ai.providers.openrouter import OpenRouterProvider
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.exceptions import AIProviderError

@pytest.fixture
def provider():
    return OpenRouterProvider("test-key")

@pytest.fixture
def sample_request():
    return AIRequest(
        model="openrouter-test",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=100,
        temperature=0.7
    )

@pytest.mark.asyncio
async def test_fetch_free_models_success(provider):
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"id": "free-model-1", "pricing": {"prompt": "0", "completion": "0"}},
                {"id": "free-model-2", "pricing": {"prompt": "0.00", "completion": 0}},
                {"id": "paid-model-1", "pricing": {"prompt": "0.01", "completion": "0.02"}},
                {"id": "invalid-model", "pricing": {}}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        free_models = await provider.get_free_models()
        assert len(free_models) == 2
        assert "free-model-1" in free_models
        assert "free-model-2" in free_models
        assert "paid-model-1" not in free_models

@pytest.mark.asyncio
async def test_fetch_free_models_timeout(provider):
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Timeout")
        
        free_models = await provider.get_free_models()
        assert free_models == []

@pytest.mark.asyncio
async def test_generate_text_free_only_override(provider, sample_request):
    provider._cached_free_models = ["free-model-override"]
    provider._last_fetch_time = 200000000000.0 # future time to bypass cache expiry

    with patch("app.services.ai.providers.openrouter.settings") as mock_settings:
        mock_settings.AI_ROUTING_POLICY = "FREE_ONLY"
        mock_settings.OPENROUTER_DISCOVERY_CACHE_TTL = 3600
        
        with patch.object(provider.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_choice = MagicMock()
            mock_choice.message.content = "Success"
            mock_resp = MagicMock()
            mock_resp.choices = [mock_choice]
            mock_resp.usage = None
            mock_create.return_value = mock_resp
            
            resp = await provider.generate_text(sample_request)
            
            mock_create.assert_called_once()
            assert mock_create.call_args[1]["model"] == "free-model-override"
            assert resp.model == "free-model-override"

@pytest.mark.asyncio
async def test_generate_text_free_only_no_models(provider, sample_request):
    provider._cached_free_models = []
    
    with patch("app.services.ai.providers.openrouter.settings") as mock_settings:
        mock_settings.AI_ROUTING_POLICY = "FREE_ONLY"
        mock_settings.OPENROUTER_DISCOVERY_CACHE_TTL = 3600
        
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"data": []}
            mock_get.return_value = mock_response
            
            with pytest.raises(AIProviderError, match="No free OpenRouter models available."):
                await provider.generate_text(sample_request)
