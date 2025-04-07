from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from typing import List, Optional
import os
import tempfile
from pathlib import Path

from app.models.rag_schemas import (
    DocumentUploadRequest,
    DocumentChunk,
    RAGRequest,
    RAGResponse
)
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service

router = APIRouter(tags=["rag"])

@router.post("/documents/upload", response_model=List[str])
async def upload_documents(
    document: DocumentUploadRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Upload a document for processing and indexing.
    """
    try:
        document_ids = await rag_service.process_text(
            text=document.content,
            metadata={} if document.metadata is None else document.metadata.dict(),
            chunk_size=document.chunk_size,
            chunk_overlap=document.chunk_overlap
        )
        return document_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    

@router.post("/documents/upload-file", response_model=List[str])
async def upload_file(
    file: UploadFile = File(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Upload a file (PDF, TXT, etc) for processing and indexing
    """
    # Save upload file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Process the file
        document_ids = await rag_service.process_file(
            file_path=temp_file_path,
            metadata={"filename": file.filename, "content_type": file.content_type},
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        # Clean up temp file
        os.unlink(temp_file_path)
                  
        return document_ids
    except Exception as e:
        #clean up temp file in case of error
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    

@router.get("/documents/{document_id}", response_model=DocumentChunk)
async def get_document(
    document_id: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Retrieve a specific document by ID
    """
    document = await rag_service.document_store.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    return document

@router.get("/documents", response_model=List[DocumentChunk])
async def list_documents(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    List all documents in the system
    """
    documents = await rag_service.document_store.list_documents()
    return documents

@router.delete("/documents/{document_id}", response_model=bool)
async def delete_document(
    document_id: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Delete a specific document by ID
    """
    success = await rag_service.document_store.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    return success

@router.post("/query", response_model=RAGResponse)
async def query_documents(
    request: RAGRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Query documents using RAG to generate an answer.
    """
    try:
        response = await rag_service.generate_rag_response(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating RAG response: {str(e)}") 
    

@router.get("/collections/{collection_name}/documents", response_model=List[DocumentChunk])
async def retrieve_documents_from_collection(
    collection_name: str,
    query: str = Query(..., description="Search query"),
    top_k: int = Query(3, description="Number of top documents to retrieve"),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Retrieve documents from a specific collection based on a query
    """
    try:
        documents = await rag_service.retrieve_relevant_documents(
            query=query,
            top_k=top_k,
            collection_name=collection_name
        )

        # Convert LangChain documents to our DocumentChunk model
        result = []
        for doc in documents:
            metadata = doc.metadata.copy()
            doc_id = metadata.pop("document_id", None)
            result.append(
                DocumentChunk(
                    content=doc.page_content,
                    metadata=metadata,
                    chunk_id=doc_id
                )
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")
    
@router.delete("/collections/{collection_name}", response_model=bool)
async def delete_collection(
    collection_name: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Delete a collection of documents
    """
    try:
        success = await rag_service.delete_collection(collection_name)
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting collection: {str(e)}")