from typing import List, Dict, Any, Optional, Callable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentSplitter:
    """Utility class for splitting documents into chunks."""

    def __init__(
            self,
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
            separators: Optional[List[str]] = None,
    ):
        """
        Initialize the document splitter.
        
        Args:
            chunk_size (int): Size of each chunk in characters.
            chunk_overlap (int): Overlap size between chunks in characters.
            separators (Optional[List[str]]): List of separators to use for splitting, ordered by priority.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Default separators if none provided
        self.separators = separators or [
            "\n\n",   # Paragraphs
            "\n",     # Line breaks
            ". ",     # Sentences
            ", ",     # Clauses
            " ",      # Words
            ""        # Characters (fallback)
        ]

        # Create the LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators
        )

    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks based on configured separators.

        Args:
            text (str): Text to be split.
            
        Returns:
            List[str]: List of text chunks.
        """
        return self.text_splitter.split_text(text)
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split LangChain documents into chunks.
        
        Args:
            documents (List[Document]): List of LangChain Document objects
            
        Returns:
            List[Document]: List of split Document objects.
        """
        return self.text_splitter.split_documents(documents)
    

    def create_documents(
            self,
            texts: List[str],
            metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Document]:
        """
        Create LangChain Document objects from text and metadata.

        Args:
            texts (List[str]): List of text strings.
            metadatas (Optional[List[Dict[str, Any]]]): List of metadata dictionaries.
            
        Returns:
            List[Document]: List of LangChain Document objects.
        """
        if metadatas is None:
            metadatas = [{} for _ in texts]

        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]

        return self.split_documents(documents)
