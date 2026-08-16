import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import httpx
from app.services.ai.providers.ollama import OllamaProvider
from app.services.ai.models import AIRequest
from app.services.ai.exceptions import AIProviderError, AITimeoutError

@pytest.fixture
def provider():
    return OllamaProvider("http://localhost:11434")

@pytest.fixture
def sample_request():
    return AIRequest(
        model="llama3",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.7,
        max_tokens=100
    )

@pytest.mark.asyncio
async def test_generate_text_success(provider, sample_request):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"message": {"content": "Hi there"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = await provider.generate_text(sample_request)

        assert response.content == "Hi there"
        assert response.provider == "ollama"
        assert response.model == "llama3"

@pytest.mark.asyncio
async def test_generate_text_timeout(provider, sample_request):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.TimeoutException("Timeout")

        with pytest.raises(AITimeoutError):
            await provider.generate_text(sample_request)

@pytest.mark.asyncio
async def test_generate_text_connect_error(provider, sample_request):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.ConnectError("Connection refused")

        with pytest.raises(AIProviderError):
            await provider.generate_text(sample_request)
