import httpx
from typing import Optional
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.exceptions import AIProviderError, AITimeoutError

class OllamaProvider(BaseAIProvider):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def generate_text(self, request: AIRequest) -> AIResponse:
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": request.model,
            "messages": request.messages,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            },
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content", "")
                return AIResponse(
                    content=content,
                    provider="ollama",
                    model=request.model,
                    usage={"total_tokens": data.get("eval_count", 0)},
                    latency=data.get("eval_duration", 0) / 1e9 if "eval_duration" in data else 0.0
                )
        except httpx.TimeoutException as e:
            raise AITimeoutError(f"Ollama request timed out: {e}")
        except httpx.ConnectError as e:
            raise AIProviderError(f"Ollama connection failed: {e}")
        except Exception as e:
            raise AIProviderError(f"Ollama request failed: {e}")

    async def generate_structured(self, request: AIRequest, schema: dict) -> AIResponse:
        return await self.generate_text(request)
