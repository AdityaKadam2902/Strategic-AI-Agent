"""
Configuration management for Strategic Debate Engine.
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_config():
    """Validate that all required configuration is present."""
    if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY not set. Please create a .env file with your API key."
        )
    return True
