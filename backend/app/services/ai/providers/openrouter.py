import time
from typing import Any, Dict
import openai
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.exceptions import AIAuthenticationError, AIRateLimitError, AITimeoutError, AIProviderError

class OpenRouterProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

    async def generate_text(self, req: AIRequest) -> AIResponse:
        start_time = time.time()
        try:
            response = await self.client.chat.completions.create(
                model=req.model,
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
                model=req.model,
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
