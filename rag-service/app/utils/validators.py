"""
Input validation utilities
"""
import re
from fastapi import HTTPException

class Validator:
    @staticmethod
    def validate_question(question: str, max_length: int = 500) -> str:
        """Validate question input"""
        # Strip whitespace
        question = question.strip()
        
        # Check length
        if len(question) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if len(question) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Question too long. Maximum {max_length} characters."
            )
        
        # Check for suspicious patterns (SQL injection, XSS)
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onclick=',
            r'DROP TABLE',
            r'DELETE FROM',
            r'INSERT INTO',
            r'UPDATE.*SET'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, question, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid characters in question"
                )
        
        return question
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input"""
        # Remove null bytes
        text = text.replace('\x00', '')
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

