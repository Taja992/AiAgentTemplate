from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from app.models.rag_schemas import DocumentChunk
from app.utils.logger import get_logger


logger = get_logger(__name__)


class BaseEmbeddings(ABC):
    """Abstract base class for embedding generators."""

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (as lists of floats)
        """
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """
        Generate an embedding for a single query text
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        pass

class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        pass
    
    @abstractmethod
    async def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search for the query.
        
        Args:
            query: The query text
            k: Number of documents to return
            
        Returns:
            List of documents sorted by relevance
        """
        pass
    
    @abstractmethod
    async def delete_collection(self) -> None:
        """Delete the entire collection from the vector store."""
        pass

class BaseDocumentStore(ABC):
    """Abstract base class for document storage."""

    @abstractmethod
    async def store_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Store a document and return its ID.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            Document ID
        """
        pass

    @abstractmethod
    async def get_document(self, document_id: str) -> Optional[DocumentChunk]:
        """
        Retrieve a document by ID.
        
        Args:
            document_id: ID of the document to retrieve
            
        Returns:
            Document object or None if not found
        """
        pass

    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if deleted, False otherwise
        """
        pass

    @abstractmethod
    async def list_documents(self) -> List[DocumentChunk]:
        """
        List all available documents.
        
        Returns:
            List of document objects
        """
        pass

class BaseRetriever(ABC):
    """Abstract base class for document retrievers."""

    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Query string
            top_k: Number of top documents to retrieve
        
        Returns:
            List of Document objects
        """
        pass