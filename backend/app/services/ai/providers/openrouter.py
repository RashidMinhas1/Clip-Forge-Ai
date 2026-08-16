import time
from typing import Any, Dict, List, Optional
import openai
import httpx
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.exceptions import AIAuthenticationError, AIRateLimitError, AITimeoutError, AIProviderError
from app.core.config import settings

class OpenRouterProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self._cached_free_models: List[str] = []
        self._last_fetch_time: float = 0.0

    async def get_free_models(self) -> List[str]:
        current_time = time.time()
        # Cache TTL defined by settings, default 3600
        ttl = getattr(settings, "OPENROUTER_DISCOVERY_CACHE_TTL", 3600)
        
        if self._cached_free_models and (current_time - self._last_fetch_time < ttl):
            return self._cached_free_models

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://openrouter.ai/api/v1/models",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                free_models = []
                for model in data.get("data", []):
                    pricing = model.get("pricing", {})
                    # Ensure both prompt and completion are exactly "0" or "0.0" or 0
                    prompt_price = pricing.get("prompt")
                    completion_price = pricing.get("completion")
                    
                    if (str(prompt_price) in ["0", "0.0", "0.00"]) and (str(completion_price) in ["0", "0.0", "0.00"]):
                        free_models.append(model.get("id"))
                
                if free_models:
                    self._cached_free_models = free_models
                    self._last_fetch_time = current_time
                    
                return self._cached_free_models
        except httpx.TimeoutException:
            # Fallback to cache if available on timeout, else empty
            return self._cached_free_models
        except Exception:
            # Safe fail
            return self._cached_free_models

    async def generate_text(self, req: AIRequest) -> AIResponse:
        start_time = time.time()
        
        target_model = req.model
        
        # Determine if we must force a free model based on routing policy
        policy = getattr(settings, "AI_ROUTING_POLICY", "FREE_ONLY")
        if policy in ["FREE_ONLY", "FREE_FIRST"]:
            free_models = await self.get_free_models()
            if target_model not in free_models:
                if not free_models:
                    raise AIProviderError("No free OpenRouter models available.")
                target_model = free_models[0]
                
        try:
            response = await self.client.chat.completions.create(
                model=target_model,
                messages=req.messages,
                max_tokens=req.max_tokens,
                temperature=req.temperature,
            )
            latency = time.time() - start_time
            usage = {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            }
            return AIResponse(
                content=response.choices[0].message.content or "",
                provider="openrouter",
                model=target_model,
                usage=usage,
                latency=latency
            )
        except openai.AuthenticationError as e:
            raise AIAuthenticationError(str(e))
        except openai.RateLimitError as e:
            raise AIRateLimitError(str(e))
        except openai.APITimeoutError as e:
            raise AITimeoutError(str(e))
        except Exception as e:
            raise AIProviderError(str(e))

    async def generate_structured(self, req: AIRequest, schema: Dict[str, Any]) -> AIResponse:
        return await self.generate_text(req)
