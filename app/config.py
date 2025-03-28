from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load Environment variables from .env file if needed
load_dotenv()

class Settings(BaseSettings):
    """Configuration stetings"""
    # API Settings
    API_TITLE: str = "AI Agent API"
    API_DESCRIPTION: str = "API for interacting with various AI models."
    API_VERSION: str = "0.1.0"

    # Default model settings
    DEFAULT_MODEL: str = "ollama:llama2"
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 1000


    # Ollama Settings
    OLLAMA_HOST: str = "http://localhost:11434"

    # Logging
    LOG_LEVEL: str ="INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()