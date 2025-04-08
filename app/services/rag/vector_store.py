import os
import asyncio
import tempfile
import shutil
from typing import List, Optional, Dict, Any
from functools import partial

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from app.services.rag.base import BaseVectorStore, BaseEmbeddings
from app.services.rag.embeddings import OllamaEmbeddingService
from app.utils.logger import get_logger

logger = get_logger(__name__)

class FAISSVectorStore(BaseVectorStore):
    """
    Implementation of BaseVectorstore using FAISS for vector storage and retrieval
    
    FAISS provides efficient similarity search and cluster for dense vectors
    """

    def __init__(
            self,
            embedding_service: Optional[BaseEmbeddings] = None,
            persist_directory: Optional[str] = None,
            collection_name: str = "default",
            index_kwargs: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the FAISS vector store.
        
        Args:
            embedding_service: Service for generating embeddings
            persist_directory: Directory to persist FAISS index
            collection_name: Name of collection to use
            index_kwargs: Additional keyword arguments for FAISS
        """
        self.embedding_service = embedding_service or OllamaEmbeddingService()
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.index_kwargs = index_kwargs or {}
        self.faiss_index = None

        # Create directory for persisting if needed
        if self.persist_directory and not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory, exist_ok=True)
            logger.info(f"Created persistent directory at {self.persist_directory}")

        self.index_path = os.path.join(self.persist_directory, self.collection_name) if self.persist_directory else None

        logger.info(f"Initialized FAISS vector store with collection: {self.collection_name}")

    async def _init_or_load_index(self):
        """Initialize or load the FAISS index if it doesn't exist."""
        if self.faiss_index is not None:
            return
        
        # Check if we have a persisted index to load
        if self.index_path and os.path.exists(self.index_path):
            try:
                # Use a thread pool as FAISS operations are CPU-bound
                loop = asyncio.get_event_loop()
                self.faiss_index = await loop.run_in_executor(
                    None,
                    partial(
                        FAISS.load_local,
                        self.index_path,
                        self.embedding_service.ollama_embeddings
                        allow_dangerous_deserialization=True, # Allow loading of potentially unsafe data
                    )
                )
                logger.info(f"Loading existing FAISS index from {self.index_path}")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {str(e)}")
                # If loading fail create a new one
                self.faiss_index = FAISS.from_texts(
                    texts=[""], # Initialize with empty text - we'll add real documents later
                    embedding=self.embedding_service.ollama_embeddings,
                    **self.index_kwargs
                )
        else:
            # Create a new index
            self.faiss_index = FAISS.from_texts(
                texts=[""], # Initialize with empty text - we'll add real documents later
                embedding=self.embedding_service.ollama_embeddings,
                **self.index_kwargs
            )
            logger.info("Creating new FAISS index")


    async def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store
        
        Args:
            documents: List of documents to add
        """
        if not documents:
            logger.warning("No documents provided to add_documents")
            return
        
        try:
            await self._init_or_load_index()

            # Use a thread pool FAISS operations cpu-bound
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                partial(self.faiss_index.add_documents, documents)
            )

            # Persist index if a directory is specified
            if self.persist_directory:
                await loop.run_in_executor(
                    None,
                    partial(self.faiss_index.save_local, self.index_path)
                )
            
            logger.info(f"Added {len(documents)} documents to FAISS index")
        except Exception as e:
            logger.error(f"Error adding documents to FAISS index: {str(e)}")
            raise

    async def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search for the query.
        
        
        Args:
            query: The query text
            k: Number of docs to return
            
        Returns:
            List of docs sorted by relevance
        """
        if not query.strip():
            logger.warning("Empty query provided for similarity search")
            return []

        try:
            await self._init_or_load_index()

            # Use a thread pool as FAISS operations are CPU-bound
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                partial(self.faiss_index.similarity_search, query, k)
            )
            
            logger.info(f"Found {len(results)} documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            raise



    async def delete_collection(self) -> None:
        """Delete the entire collection from the vector store."""
        try:
            self.faiss_index = None
    
            if self.persist_directory and os.path.exists(os.path.join(self.persist_directory, self.collection_name)):
                collection_dir = os.path.join(self.persist_directory, self.collection_name)
                
                # Use a thread pool for file operations
                loop = asyncio.get_event_loop()
                
                # Delete directory and all its contents in one operation
                await loop.run_in_executor(None, partial(shutil.rmtree, collection_dir))
                
            logger.info(f"Deleted FAISS collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting FAISS collection: {str(e)}")
            raise




