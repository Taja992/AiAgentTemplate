from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
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
    # DEFAULT_MODEL: str = "ollama:deepseek-r1:7b"
    DEFAULT_MODEL: str = "ollama:gemma3:1b"
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 1000

    #Special model settings
    TRANSLATION_MODEL: str = "ollama:lauchacarro/qwen2.5-translator"
    CODE_MODEL: str = "ollama:codellama:7b"
    CREATIVE_MODEL: str = "ollama:mistral"
    MATH_MODEL: str = "ollama:llama2:13b"

    # Task specific parameters
    TASK_PARAMS: Dict[str, Dict[str, Any]] = {
        "DEFAULT": {
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "TRANSLATION": {
            "temperature": 0.3,
            "max_tokens": 1000
        },
        "CODE": {
            "temperature": 0.2,
            "max_tokens": 1500
        },
        "CREATIVE": {
            "temperature": 0.8,
            "max_tokens": 2000
        },
        "MATH": {
            "temperature": 0.1,
            "max_tokens": 800
        }
    }


    # Ollama Settings
    OLLAMA_HOST: str = "http://localhost:11434"

    # Logging
    LOG_LEVEL: str ="INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()