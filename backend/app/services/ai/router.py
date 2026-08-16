import logging
from app.core.config import settings
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.exceptions import AIProviderError, AIAuthenticationError, AIRateLimitError, AITimeoutError
from app.services.ai.providers.openai import OpenAIProvider
from app.services.ai.providers.openrouter import OpenRouterProvider
from app.services.ai.providers.gemini import GeminiProvider
from app.services.ai.providers.ollama import OllamaProvider

logger = logging.getLogger(__name__)

class AIRouter:
    def __init__(self):
        self.policy = settings.AI_ROUTING_POLICY
        self.providers = {}
        
        if settings.OLLAMA_BASE_URL:
            self.providers["ollama"] = OllamaProvider(settings.OLLAMA_BASE_URL)
        if settings.OPENAI_API_KEY:
            self.providers["openai"] = OpenAIProvider(settings.OPENAI_API_KEY)
        if settings.OPENROUTER_API_KEY:
            self.providers["openrouter"] = OpenRouterProvider(settings.OPENROUTER_API_KEY)
        if settings.GEMINI_API_KEY:
            self.providers["gemini"] = GeminiProvider(settings.GEMINI_API_KEY)

    async def generate(self, req: AIRequest) -> AIResponse:
        if self.policy == "FREE_ONLY":
            try:
                return await self._try_provider("ollama", req)
            except AIProviderError:
                try:
                    return await self._try_provider("gemini", req)
                except AIProviderError:
                    return await self._try_provider("openrouter", req)
        elif self.policy == "FREE_FIRST":
            try:
                return await self._try_provider("ollama", req)
            except AIProviderError:
                try:
                    return await self._try_provider("gemini", req)
                except AIProviderError:
                    return await self._try_provider("openrouter", req)
        else: # NORMAL
            try:
                return await self._try_provider("openai", req)
            except AIProviderError:
                return await self._try_provider("openrouter", req)
                
    async def _try_provider(self, provider_name: str, req: AIRequest) -> AIResponse:
        provider = self.providers.get(provider_name)
        if not provider:
            raise AIProviderError(f"Provider {provider_name} not configured")
        
        provider_model = req.model
        if provider_name == "gemini" and not provider_model.startswith("gemini"):
            provider_model = "gemini-1.5-flash"
        elif provider_name == "openai" and not provider_model.startswith("gpt"):
            provider_model = "gpt-4o-mini"
        elif provider_name == "ollama":
            provider_model = settings.OLLAMA_MODEL
            
        req_copy = req.model_copy()
        req_copy.model = provider_model
        
        return await provider.generate_text(req_copy)

    async def generate_structured(self, req: AIRequest, schema: type) -> AIResponse:
        if self.policy == "FREE_ONLY":
            try:
                return await self._try_provider_structured("ollama", req, schema)
            except AIProviderError:
                try:
                    return await self._try_provider_structured("gemini", req, schema)
                except AIProviderError:
                    return await self._try_provider_structured("openrouter", req, schema)
        elif self.policy == "FREE_FIRST":
            try:
                return await self._try_provider_structured("ollama", req, schema)
            except AIProviderError:
                try:
                    return await self._try_provider_structured("gemini", req, schema)
                except AIProviderError:
                    return await self._try_provider_structured("openrouter", req, schema)
        else: # NORMAL
            try:
                return await self._try_provider_structured("openai", req, schema)
            except AIProviderError:
                return await self._try_provider_structured("openrouter", req, schema)

    async def _try_provider_structured(self, provider_name: str, req: AIRequest, schema: type) -> AIResponse:
        provider = self.providers.get(provider_name)
        if not provider:
            raise AIProviderError(f"Provider {provider_name} not configured")
        
        provider_model = req.model
        if provider_name == "gemini" and not provider_model.startswith("gemini"):
            provider_model = "gemini-1.5-flash"
        elif provider_name == "openai" and not provider_model.startswith("gpt"):
            provider_model = "gpt-4o-mini"
        elif provider_name == "ollama":
            provider_model = settings.OLLAMA_MODEL
            
        req_copy = req.model_copy()
        req_copy.model = provider_model
        
        return await provider.generate_structured(req_copy, schema)
