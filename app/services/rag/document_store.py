import asyncio
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from functools import partial
from pathlib import Path

from app.services.rag.base import BaseDocumentStore
from app.models.rag_schemas import DocumentChunk, DocumentMetadata
from app.utils.logger import get_logger


logger = get_logger(__name__)

class FileSystemDocumentStore(BaseDocumentStore):
    """
    Implementation of BaseDocumentStore using the file system.
    
    Stores documents as JSON files in a directory structure
    """

    def __init__(self, storage_path: str = "data/documents"):
        """
        Initialize the file system document store.
        
        Args:
            storage_path: Path to store documents
        """
        self.storage_path = Path(storage_path)

        os.makedirs(self.storage_path, exist_ok=True)
        logger.info(f"Initialized FileSystemDocumentStore at {self.storage_path}")

    async def store_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Store a document and return its ID.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            Document ID
        """
        # Generate a uniquie ID for document
        document_id = str(uuid.uuid4())

        # Create document object
        doc_metadata = DocumentMetadata(**metadata)
        document = DocumentChunk(
            content=content,
            metadata=doc_metadata,
            chunk_id=document_id
        )


        # Convert doc to json
        doc_json = document.model_dump()
        doc_json["created_at"] = datetime.now().isoformat()


        # Store document in file system
        file_path = self.storage_path / f"{document_id}.json"


        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                partial(self._write_json_file, file_path, doc_json)
            )
            logger.info(f"Stored doc with ID: {document_id}")
            return document_id
        except Exception as e:
            logger.error(f"Error storing document: {str(e)}")
            raise

    def _write_json_file(self, file_path: Path, data: Dict) -> None:
        """Write JSON data to a file."""
        # 'w' stands for 'write mode'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _read_json_file(self, file_path: Path) -> Dict:
        """Read JSON data from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    async def get_document(self, document_id: str) -> Optional[DocumentChunk]:
        """Retrieve doc by ID
        
        Args:
            document_id: ID of the document to retrieve
            
        Returns:
            Document object or None if not found
        """
        file_path = self.storage_path / f"{document_id}.json"

        if not file_path.exists():
            logger.warning(f"Document not found with ID: {document_id}")
            return None
        
        try:
            loop = asyncio.get_event_loop()
            doc_json = await loop.run_in_executor(
                None,
                partial(self._read_json_file, file_path)
            )

            # Convert JSON back to DocumentChunk

            document = DocumentChunk(**doc_json)
            logger.debug(f"Retrieved document with ID: {document_id}")
            return document
        except Exception as e:
            logger.error(f"Error retrieving document: {str(e)}")
            raise

    async def delete_document(self, document_id: str) -> bool:
        """Delete a doc by ID
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if deleted, False otherwise
        """
        file_path = self.storage_path / f"{document_id}.json"

        if not file_path.exists():
            logger.warning(f"Cannot Delete: Document not found with ID: {document_id}")
            return False
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                partial(os.remove, file_path)
            )
            logger.info(f"Deleted document with ID: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise

    async def list_documents(self) -> List[DocumentChunk]:
        """
        List all available documents.
        
        Returns:
            List of document objects
        """
        documents = []

        try:
            # Get all JSON files in the storage directory
            loop = asyncio.get_event_loop()
            file_paths = await loop.run_in_executor(
                None,
                lambda: list(self.storage_path.glob("*.json"))
            )

            # Load each doc
            for file_path in file_paths:
                try:
                    doc_json = await loop.run_in_executor(
                        None,
                        partial(self._read_json_file, file_path)
                    )
                    document = DocumentChunk(**doc_json)
                    documents.append(document)
                except Exception as e:
                    logger.error(f"Error loading document from {file_path}: {str(e)}")

            
            logger.info(f"Listed {len(documents)} documents")
            return documents
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            raise   
