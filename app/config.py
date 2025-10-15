"""Configuration management using Pydantic settings."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Application
    environment: str = "production"
    log_level: str = "INFO"
    global_threshold: float = 85.0
    
    # CORS - Allow file:// protocol and localhost variants
    allowed_origins: str = "*"  # Allow all origins (including file://)
    
    # Rate Limiting
    max_retries: int = 3
    retry_delay: int = 1
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key and self.openai_api_key != "your_openai_api_key_here")
    
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.anthropic_api_key and self.anthropic_api_key != "your_anthropic_api_key_here")


# Global settings instance
settings = Settings()
