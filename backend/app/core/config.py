from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List, Union

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # API Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///clipforge.db"
    SUPABASE_URL: str = ""
    SUPABASE_JWT_SECRET: str = ""
    ACTIVATION_KEY: str = ""

    # Infrastructure Readiness checks
    REDIS_URL: str = "redis://localhost:6379/0"

    # Transcription Configuration
    WHISPER_MODEL_SIZE: str = "small"
    WHISPER_DEVICE: str = "auto"
    WHISPER_COMPUTE_TYPE: str = "auto"
    TRANSCRIPTION_TIMEOUT: int = 300
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_DISCOVERY_CACHE_TTL: int = 3600
    GEMINI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    AI_ROUTING_POLICY: str = "FREE_ONLY"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
