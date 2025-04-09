from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Metadata for a document."""
    source: Optional[str] = Field(None, description="Source of the document(e.g., URL, file path)")
    author: Optional[str] = Field(None, description="Author of the document")
    created_at: Optional[str] = Field(None, description="Creation date of the document")
    document_type: Optional[str] = Field(None, description="Type of the document (e.g., PDF, DOCX)")
    page_number: Optional[int] = Field(None, description="Page number for paginated documents")

    # Allow Additional Properties
    extra: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata fields")


class DocumentChunk(BaseModel):
    """A chunk of text from a document with its metadata."""
    content: str = Field(..., description="Text content of the chunk")
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata, description="Metadata for the document")
    chunk_id: Optional[str] = Field(None, description="Unique identifier for the chunk")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the chunk")

    
class DocumentUploadRequest(BaseModel):
    """Request for uploading a document."""
    document_name: str = Field(..., description="Name of the document")
    content: str = Field(..., description="Content of the document")
    metadata: Optional[DocumentMetadata] = Field(None, description="Optional metadata for the document")
    collection_name: str = Field("default", description="Collection name to store the document in")
    chunk_size: int = Field(1000, description="Size of each chunk in characters")
    chunk_overlap: int = Field(200, description="Overlap size between chunks in characters")

    class Config:
        schema_extra = {
            "example": {
                "document_name": "research_paper.pdf",
                "content": "This is example document content...",
                "metadata": {
                    "source": "user_upload",
                    "author": "Jane Doe"
                },
                "collection_name": "research_papers",
                "chunk_size": 1000,
                "chunk_overlap": 200
            }
        }

class RAGRequest(BaseModel):
    """Request for a RAG-augmented response."""
    query: str = Field(..., description="User query or retrieval request")
    collection_name: Optional[str] = Field("default", description="Name of document collection to query")
    num_results: int = Field(3, description="Number of documents to retrieve")
    use_semantic_ranker: bool = Field(True, description="Whether to use semantic ranking")
    include_sources: bool = Field(True, description="Whether to include source references in response")
    model: Optional[str] = Field(None, description="Model to use for generation")

class RAGResponse(BaseModel):
    """Response from RAG-augmented query."""
    answer: str = Field(..., description="Generated answer")
    sources: List[DocumentChunk] = Field(default_factory=list, description="Source documents used for generation")
    model: str = Field(..., description="Model used for generation")
    embedding_model: Optional[str] = Field(None, description="Model used for embeddings")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Token usage information")
