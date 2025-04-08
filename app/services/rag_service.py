from typing import List, Dict, Any, Optional, Union, BinaryIO
import asyncio
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from pathlib import Path

from app.models.rag_schemas import DocumentChunk, DocumentMetadata, RAGRequest, RAGResponse
from app.services.rag.embeddings import OllamaEmbeddingService
from app.services.rag.vector_store import FAISSVectorStore
from app.services.rag.document_store import FileSystemDocumentStore
from app.services.rag.retriever import VectorStoreRetriever
from app.utils.document_processors.text_splitter import DocumentSplitter
from app.utils.document_processors.file_loader import FileLoader
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class RAGService:
    """
    Retrieval-Augmented Generation service that orchestrates document processing,
    storage, retrieval, and generation.
    """

    def __init__(
            self,
            embedding_service: Optional[OllamaEmbeddingService] = None,
            vector_store: Optional[FAISSVectorStore] = None,
            document_store: Optional[FileSystemDocumentStore] = None,
            document_splitter: Optional[DocumentSplitter] = None,
            persist_directory: str = "data/vector_db",
            default_collection: str = "default"
    ):
        """
        Initialize the RAG service with its components.
        
        Args:
            embedding_service: Service for generating text embeddings
            vector_store: Vector database for semantic search
            document_store: Storage for document content and metadata
            document_splitter: Utility for chunking documents
            persist_directory: Directory to persist vector databases
            default_collection: Default collection/namespace for documents
        """
        # Initialize components
        self.embedding_service = embedding_service or OllamaEmbeddingService()

        self.vector_store = vector_store or FAISSVectorStore(
            embedding_service=self.embedding_service,
            persist_directory=persist_directory,
            collection_name=default_collection
        )

        self.document_store = document_store or FileSystemDocumentStore()

        self.document_splitter = document_splitter or DocumentSplitter()

        self.default_collection = default_collection
        self.persist_directory = persist_directory

        logger.info(f"Initialized RAG service with collection: {default_collection}")

    async def process_file(
            self,
            file_path: str,
            metadata: Optional[Dict[str, Any]] = None,
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
            collection_name: str = "default"
    ) -> List[str]:
        """
        process a file for RAG, extracting text, chunking, and storing in vector DB.
        
        Args:
            file_path: Path to the file
            metadata: Additional metadata about the file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of document IDs created
        """
        logger.info(f"Processing file: {file_path}")

        # Extract text from file
        try:
            text_content = FileLoader.load_file(file_path)
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            raise

        # Process the extracted text
        return await self.process_text(
            text_content,
            metadata or {"source": file_path},
            chunk_size,
            chunk_overlap,
            collection_name
        )
    
    async def process_text(
            self,
            text: str,
            metadata: Dict[str, Any],
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
            collection_name: str = "default"
    ) -> List[str]:
        """
        Process text for RAG, chunking and storing in vector DB.
        
        Args:
            text: Text content to process
            metadata: Metadata about the text
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
            
        Returns:
            List of document IDs created
        """
        logger.info(f"Processing text content with chunk size: {chunk_size}")

        # Configure text splitter with provided parameters
        if chunk_size != self.document_splitter.chunk_size or chunk_overlap != self.document_splitter.chunk_overlap:
            self.document_splitter = DocumentSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

        # Split text into chunks
        text_chunks = self.document_splitter.split_text(text)
        logger.info(f"Text Split into {len(text_chunks)} chunks")

        # Store each chunk and get document IDs
        document_ids = []
        langchain_docs = []

        for i, chunk in enumerate(text_chunks):
            # Create chunk-specific metadata
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "chunk_count": len(text_chunks),
                "collection": collection_name
            }

            # Store in document store
            doc_id = await self.document_store.store_document(
                content=chunk,
                metadata=chunk_metadata
            )
            document_ids.append(doc_id)

            # Create LangChain Document for vector storage
            langchain_docs.append(
                Document(
                    page_content=chunk,
                    metadata={**chunk_metadata, "document_id": doc_id}
                )
            )

        # Use the specified collection's vector store
        vector_store = (
            self.vector_store if collection_name == self.default_collection
            else FAISSVectorStore(
                embedding_service=self.embedding_service,
                persist_directory=self.persist_directory,
                collection_name=collection_name
            )
        )

        #Store documents in vector Database
        await vector_store.add_documents(langchain_docs)
        logger.info(f"Added {len(langchain_docs)} documents to vector store collection: {collection_name}")
        return document_ids


    async def retrieve_relevant_documents(
            self,
            query: str,
            top_k: int = 3,
            collection_name: Optional[str] = None
    ) -> List[Document]:
        """
        Retrieve documents relevant to the query.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            collection_name: Vector store collection to query
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Retrieving relevant documents for query: {query[:50]}...")

        # If a different collection is specified, create a retriever for it
        if collection_name and collection_name != self.default_collection:
            vector_store = FAISSVectorStore(
                embedding_service=self.embedding_service,
                persist_directory=self.persist_directory,
                collection_name=collection_name
            )
            retriever = VectorStoreRetriever(vector_store=vector_store)
        else:
            # use the default retriever
            retriever = VectorStoreRetriever(vector_store=self.vector_store)


        # Retrieve documents
        documents = await retriever.retrieve(query, top_k=top_k)
        logger.info(f"Retrieved {len(documents)} documents")
        return documents
    
    async def generate_rag_response(
            self,
            request: RAGRequest
    ) -> RAGResponse:
        """
        Generate an answer to a query using RAG.
        
        Args:
            request: RAG request with query and parameters
            
        Returns:
            Rag response with answer and sources
        """
        logger.info(f"Generating RAG response for query: {request.query[:50]}...")

        # Set up the model to use
        model_name = request.model or settings.DEFAULT_MODEL

        # Uf using Ollama model, extract just the model name
        if ":" in model_name:
            _, model_name = model_name.split(":", 1)

        # Retrieve relevant documents
        documents = await self.retrieve_relevant_documents(
            query=request.query,
            top_k=request.num_results,
            collection_name=request.collection_name
        )

        if not documents:
            logger.warning("No relevant documents found for query")
            return RAGResponse(
                answer="I couldn't find any relevant documents.",
                sources=[],
                model=model_name,
                embedding_model=self.embedding_service.model_name
            )
        
        # Create a retriever object

        retriever = VectorStoreRetriever(
            vector_store=self.vector_store
        )

        # Set up a RetrievalQA chain
        llm = Ollama(model=model_name)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", # Simple method that stuffs all documents into prompts
            retriever=retriever.vector_store.faiss_index.as_retriever(
                search_kwargs={"k": request.num_results}
            ),
            return_source_documents=True
        )

        # Generate response (run synchronously as LangChain's RetrievalQA does not support async)
        loop = asyncio.get_event_loop()
        chain_response = await loop.run_in_executor(
            None,
            lambda: qa_chain({"query": request.query})
        )


        # Extract answer and source documents
        answer = chain_response.get("result", "")
        source_docs = chain_response.get("source_documents", [])

        # Convert source documents to DocumentChunk objects
        sources = []
        for doc in source_docs:
            # Create metadata object
            metadata = doc.metadata.copy()
            doc_id = metadata.pop("document_id", None)

            # Convert to DocumentChunk
            sources.append(
                DocumentChunk(
                    content=doc.page_content,
                    metadata=DocumentMetadata(**metadata),
                    chunk_id=doc_id
                )
            )

        return RAGResponse(
            answer=answer,
            sources=sources,
            model=model_name,
            embedding_model=self.embedding_service.model_name
        )
    
    async def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection of documents.
        
        Args:
            collection_name: Name of the collection to delete
            
        Returns:
            true if successful
        """
        logger.info(f"Deleting collection: {collection_name}")

        # Create a vector store instance for the collection

        vector_store = FAISSVectorStore(
            embedding_service=self.embedding_service,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )

        await vector_store.delete_collection()

        # Note This doesn't delete documents from the document store
        # as that would require tracking which document IDs belong to which collection

        return True
    
    async def list_collections(self) -> List[str]:
        """
        List all available collections in the vector store.
        
        Returns:
            List of collection names
        """
        logger.info("Listing all collections")

        try:
            # Find all subdirectories in the persist_directory
            collections = []
            persist_path = Path(self.persist_directory)

            if persist_path.exists() and persist_path.is_dir():
                # List all directories (Each directory is a collection)
                collections = [d.name for d in persist_path.iterdir() if d.is_dir()]

            logger.info(f"Found {len(collections)} collections")
            return collections
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []


