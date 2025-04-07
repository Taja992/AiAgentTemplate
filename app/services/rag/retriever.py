from typing import List, Optional, Dict, Any
from langchain.schema import Document
from app.services.rag.base import BaseRetriever, BaseVectorStore
from app.services.rag.vector_store import FAISSVectorStore
from app.utils.logger import get_logger

logger = get_logger(__name__)

class VectorStoreRetriever(BaseRetriever):
    """
    Implementation of BaseRetriever using a vector store for retrieval.
    
    This retriever performs similarity search on the provided vector store
    to find relevant documents based on the query
    """

    def __init__(
            self,
            vector_store: Optional[BaseVectorStore] = None,
            search_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the vector store retriever
        
        Args:
            vector_store: The vector store to search in
            search_kwargs: Additional search params
        """
        self.vector_store = vector_store or FAISSVectorStore()
        self.search_kwargs = search_kwargs or {"k": 4}

        logger.info("Initialized VectorStoreRetriever")

    async def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents for query.
        
        Args:
            query: Query String
            top_k: Number of top documents to retrieve
            
        Returns:
            List of document objects
        """
        if not query.strip():
            logger.warning("Empty query string provided.")
            return []
        
        try:
            # Override k if provided in retriever call
            search_params = self.search_kwargs.copy()
            search_params["k"] = top_k

            # Perform similarity search
            documents = await self.vector_store.similarity_search(
                query,
                **search_params # use ** to unpack the dictionary into keyword arguments
            )

            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents for query: {str(e)}")
            raise
    