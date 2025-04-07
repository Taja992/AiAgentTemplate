import logging
import logging.handlers
import sys
from pathlib import Path
from app.config import settings

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure basic logging format
# %(asctime)s - Timestamp when the log was created (e.g., "2025-03-28 14:30:45")
# %(levelname)s - Log level (e.g., "INFO", "WARNING", "ERROR")
# %(name)s - Logger name (typically the module name like "app.services.model_service")
# %(lineno)d - Line number in the source file where the log was generated
# %(message)s - The actual log message you passed to the logger
# 2025-03-28 14:30:45 | INFO | app.services.model_service:27 | ModelService initialized with handlers: ['ollama']
logging_format = "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"


# Map string log level from settings to logging constants
log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Configure the root logger
logging.basicConfig(
    level=log_level,
    format=logging_format,
    datefmt=date_format,
    handlers=[
        # Console Handler
        logging.StreamHandler(sys.stdout),
        # File Handler - rotates logs when they reach 5MB
        logging.handlers.RotatingFileHandler(
            logs_dir / "app.log",
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,  # Keep 3 backup files
            encoding="utf-8",
        ),
    ],
)


# Reduce verbosity of third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING) 
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("starlette").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("faiss").setLevel(logging.WARNING) 
logging.getLogger("aiohttp").setLevel(logging.WARNING)


logging.getLogger("app.services.rag").setLevel(logging.INFO)
logging.getLogger("app.services.rag.embeddings").setLevel(logging.INFO)
logging.getLogger("app.services.rag.vector_store").setLevel(logging.INFO)
logging.getLogger("app.services.rag.document_store").setLevel(logging.INFO)
logging.getLogger("app.services.rag.retriever").setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the specified module.
    
    Args:
        name: Usually __name__ of the module.
        
    Returns:
        a configured logger instance.
    """
    return logging.getLogger(name)