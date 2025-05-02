import os
from typing import Optional
from PyPDF2 import PdfReader
import magic
from pathlib import Path

class PDFProcessor:
    def __init__(self):
        self.supported_mime_types = [
            'application/pdf',
            'application/x-pdf',
            'application/acrobat',
            'application/vnd.pdf',
            'text/pdf',
            'text/x-pdf'
        ]

    def is_valid_pdf(self, file_path: str) -> bool:
        """Check if the file is a valid PDF."""
        try:
            mime = magic.Magic(mime=True)
            file_mime = mime.from_file(file_path)
            return file_mime in self.supported_mime_types
        except Exception:
            return False

    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not self.is_valid_pdf(file_path):
            raise ValueError(f"Invalid PDF file: {file_path}")

        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text by removing common PDF artifacts.
        
        Args:
            text: Raw text extracted from PDF
            
        Returns:
            Cleaned text
        """
        # Remove multiple newlines
        text = '\n'.join(line for line in text.split('\n') if line.strip())
        
        # Remove page numbers and headers/footers
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that are just numbers (likely page numbers)
            if line.strip().isdigit():
                continue
            # Skip lines that are too short (likely headers/footers)
            if len(line.strip()) < 5:
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines) 