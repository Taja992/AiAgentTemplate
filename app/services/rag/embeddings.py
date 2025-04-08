import asyncio
from typing import List, Dict, Any, Optional
from functools import partial
from langchain_ollama import OllamaEmbeddings
from app.services.rag.base import BaseEmbeddings
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class OllamaEmbeddingService(BaseEmbeddings):
    """
    Implementation of BaseEmbeddings using Ollama's embedding models.
    
    This service provides document and query embedding capabilities
    using locally hosted Ollama models."""


    def __init__(
            self,
            model_name: str = "nomic-embed-text",
            base_url: Optional[str] = None,
            dimensions: Optional[int] = None,
    ):
        """
        Initialize the Ollama embedding service.
        
        Args:
            model_name: Name of the embedding model in Ollama
            base_url: URL for ollama API(defaults to settings.OLLAMA_HOST)
            dimensions: output dimensions for embeddings (model-dependent)"""
        
        self.model_name = model_name
        self.base_url = base_url or settings.OLLAMA_HOST
        self.dimensions = dimensions

        # Initialize the LangChain OllamaEmbeddings
        self.ollama_embeddings = OllamaEmbeddings(
            model=self.model_name,
            base_url=self.base_url
        )

        logger.info(f"Initialized OllamaEmbeddingService with model: {model_name}")

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (as a list of floats)"""
        if not texts:
            return []
        
        try:
            # Run in thread pool as Ollama embeddings are synchronous
            loop= asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                partial(self.ollama_embeddings.embed_documents, texts)
            )
            logger.debug(f"Generated embeddings for {len(texts)} documents")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating document embeddings: {str(e)}")
            raise

    async def embed_query(self, text: str) -> List[float]:
        """
        Generate an embedding for single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        if not text.strip():
            return []
        
        try:
            # Run in thread pool as Ollama embeddings are synchronous
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                partial(self.ollama_embeddings.embed_query, text)
            )
            logger.debug("Generated embedding for query")

            return embedding
        
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise