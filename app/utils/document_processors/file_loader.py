import os
import base64
from typing import Dict, List, Optional, Union, BinaryIO
from pathlib import Path
import mimetypes
from app.utils.logger import get_logger

# Optional imports for specific file types
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

logger = get_logger(__name__)

class FileLoader:
    """Utility class for loading document files."""

    @staticmethod
    def load_text_file(file_path: Union[str, Path]) -> str:
        """
        Load a text file and return its content.
        
        Args:
            file_path (Union[str, Path]): Path to the text file.

        Returns:
            str: Content of the text file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    @staticmethod
    def load_pdf_with_fitz(file_path: Union[str, Path, BinaryIO]) -> str:
        """
        Extract text from PDF using PyMuPDF (fitz).
        
        Args:
            file_path (Union[str, Path, BinaryIO]): Path to the PDF file or a file-like object.
            
        Returns:
            str: Extracted text from the PDF as a string.

        Raises:
            ImportError: If PyMuPDF is not installed.
        """
        if not PYMUPDF_AVAILABLE:
            raise ImportError(
                "PyMuPDF package is required to load PDFs." \
                "Please install it with 'pip install pymupdf"
            )
        
        # Handle both file paths and file-like objects
        if isinstance(file_path, (str, Path)):
            pdf_document=fitz.open(file_path)
        else:
            pdf_document = fitz.open(stream=file_path.read(), filetype="pdf")

        text_content = []
        metadata = {}

        # Extract document metadata
        if pdf_document.metadata:
            metadata = pdf_document.metadata

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text_content.append(page.get_text())

        pdf_document.close()
        return "\n\n".join(text_content)
    
    @classmethod
    def load_file(cls, file_path: Union[str, Path], file_type: Optional[str] = None) -> str:
        """
        Load document from file based on file type
        
        Args:
            file_path (Union[str, Path]): Path to the file.
            file_type (Optional[str]): Optional fil etype override.
            
            
        Returns:
            str: Text content as string
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Determine file type if not provided
        if not file_type:
            file_type = mimetypes.guess_type(file_path)[0]

            if not file_type:
                # Fallback to extension if mimetype fails
                file_type = file_path.suffix.lower()

        # Handle PDF Files
        if 'pdf' in str(file_type).lower():
            logger.debug(f"Loading PDF file: {file_path}")
            return cls.load_pdf_with_fitz(file_path)
        
        # Handle text files
        elif any(txt in str(file_type).lower() for txt in ['text', 'txt', 'markdown', 'md']):
            logger.debug(f"Loading text file: {file_path}")
            return cls.load_text_file(file_path)
        
        # Default to text loader for unknown types
        else:
            try:
                logger.debug(f"Attempting to load file as text: {file_path}")
                return cls.load_text_file(file_path)
            except UnicodeDecodeError:
                error_msg = f"Unsupported file type: {file_path}."
                logger.error(error_msg)
                raise ValueError(error_msg)
            

    @classmethod
    def load_binary(cls, data: bytes, file_type: str) -> str:
        """
        Load document from binary data.
        
        Args:
            data (bytes): Binary file data
            file_type (str): File type (e.g., 'pdf', 'txt')
            
        Returns:
            str: Text content as string
        """
        import io

        # Handle PDF data
        if 'pdf' in file_type.lower():
            if PYMUPDF_AVAILABLE:
                logger.debug("Loading PDF from binary data")
                file_obj = io.BytesIO(data)
                return cls.load_pdf_with_fitz(file_obj)
            else:
                error_msg = "PyMuPDF Required for PDF Extraction"
                logger.error(error_msg)
                raise ImportError(error_msg)
            

        # Handle text data
        elif any(txt in file_type.lower() for txt in ['text', 'txt', 'markdown', 'md']):
            logger.debug("Loading text from binary data")
            return data.decode('utf-8')
        
        else:
            error_msg = f"Unsupported file type: {file_type}."
            logger.error(error_msg)
            raise ValueError(error_msg)

