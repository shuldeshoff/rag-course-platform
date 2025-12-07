"""
Document parsers for different file formats
"""
import PyPDF2
import docx
from typing import Optional
import re

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Parse PDF file and extract text"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
        return text
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Parse DOCX file and extract text"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
        return text
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Parse TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise ValueError(f"Error parsing TXT: {str(e)}")
        return text
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.,!?;:()\-—]', '', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text
    
    @classmethod
    def parse(cls, file_path: str) -> str:
        """Parse file based on extension"""
        if file_path.endswith('.pdf'):
            text = cls.parse_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = cls.parse_docx(file_path)
        elif file_path.endswith('.txt'):
            text = cls.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        return cls.clean_text(text)

