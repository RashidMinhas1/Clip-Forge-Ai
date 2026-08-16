import time
import httpx
from typing import Any, Dict
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.exceptions import AIAuthenticationError, AIRateLimitError, AITimeoutError, AIProviderError

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_text(self, req: AIRequest) -> AIResponse:
        start_time = time.time()
        url = f"{self.base_url}/{req.model}:generateContent?key={self.api_key}"
        
        contents = []
        for msg in req.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
            
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": req.temperature,
                "maxOutputTokens": req.max_tokens,
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                
            if response.status_code == 400:
                raise AIProviderError(response.text)
            elif response.status_code == 401:
                raise AIAuthenticationError("Invalid API key")
            elif response.status_code == 429:
                raise AIRateLimitError("Rate limit exceeded")
                
            response.raise_for_status()
            data = response.json()
            
            content = ""
            if "candidates" in data and data["candidates"]:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                
            latency = time.time() - start_time
            
            return AIResponse(
                content=content,
                provider="gemini",
                model=req.model,
                usage={"total_tokens": 0},
                latency=latency
            )
            
        except httpx.TimeoutException as e:
            raise AITimeoutError(str(e))
        except httpx.RequestError as e:
            raise AIProviderError(str(e))

    async def generate_structured(self, req: AIRequest, schema: Dict[str, Any]) -> AIResponse:
        return await self.generate_text(req)
