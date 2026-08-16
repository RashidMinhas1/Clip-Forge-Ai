import pytest
from app.services.ai.models import AIRequest
from app.services.ai.providers.mock import MockProvider
from app.services.ai.providers.openai import OpenAIProvider
from app.services.ai.providers.gemini import GeminiProvider
import openai
import httpx
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_mock_provider():
    provider = MockProvider()
    req = AIRequest(messages=[{"role": "user", "content": "Hi"}], model="test")
    resp = await provider.generate_text(req)
    assert resp.content == "Mock response"
    assert resp.provider == "mock"

@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_openai_provider(mock_openai):
    mock_client = mock_openai.return_value
    mock_create = AsyncMock()
    
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "OpenAI response"
    mock_response.usage = AsyncMock()
    mock_response.usage.prompt_tokens = 5
    mock_response.usage.completion_tokens = 5
    mock_response.usage.total_tokens = 10
    
    mock_create.return_value = mock_response
    mock_client.chat.completions.create = mock_create
    
    provider = OpenAIProvider("test-key")
    req = AIRequest(messages=[{"role": "user", "content": "Hi"}], model="gpt-4o-mini")
    resp = await provider.generate_text(req)
    
    assert resp.content == "OpenAI response"
    assert resp.provider == "openai"

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_gemini_provider(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Gemini response"}]}}]
    }
    
    mock_post.return_value = mock_response
    
    provider = GeminiProvider("test-key")
    req = AIRequest(messages=[{"role": "user", "content": "Hi"}], model="gemini-1.5-flash")
    resp = await provider.generate_text(req)
    
    assert resp.content == "Gemini response"
    assert resp.provider == "gemini"
