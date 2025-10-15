"""PDF parsing service using PyMuPDF4LLM."""
import re
from typing import List
import pymupdf4llm
from fastapi import UploadFile, HTTPException

from app.models.schemas import QAPair


async def parse_pdf(file: UploadFile) -> List[QAPair]:
    """
    Parse uploaded PDF or TXT file and extract Q&A pairs.
    
    Args:
        file: Uploaded PDF or TXT file
        
    Returns:
        List of QAPair objects
        
    Raises:
        HTTPException: If file is invalid or parsing fails
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )
        
        filename_lower = file.filename.lower()
        if not (filename_lower.endswith('.pdf') or filename_lower.endswith('.txt')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only PDF and TXT files are accepted."
            )
        
        # Read file content
        content = await file.read()
        
        if not content:
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )
        
        # Check if it's a TXT file - process directly
        if filename_lower.endswith('.txt'):
            # Decode text content
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                # Try other encodings
                try:
                    text = content.decode('latin-1')
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400,
                        detail="Unable to decode text file. Please ensure it's in UTF-8 or Latin-1 encoding."
                    )
            
            # Extract Q&A pairs from text
            qa_pairs = _extract_qa_pairs(text)
            
            if not qa_pairs:
                raise HTTPException(
                    status_code=400,
                    detail="No Q&A pairs found in text file. Ensure the file contains clearly marked questions and answers."
                )
            
            return qa_pairs
        
        # Parse PDF using pymupdf4llm
        # Save temporarily to parse
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Extract markdown text from PDF
            md_text = pymupdf4llm.to_markdown(tmp_path)
            
            # Extract Q&A pairs from markdown
            qa_pairs = _extract_qa_pairs(md_text)
            
            if not qa_pairs:
                raise HTTPException(
                    status_code=400,
                    detail="No Q&A pairs found in PDF. Ensure the PDF contains clearly marked questions and answers."
                )
            
            return qa_pairs
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse PDF: {str(e)}"
        )


def _extract_qa_pairs(text: str) -> List[QAPair]:
    """
    Extract Q&A pairs from parsed text.
    
    Supports multiple formats:
    - Q: question\nA: answer
    - Question: question\nAnswer: answer
    - 1. question\nanswer (numbered format)
    - **Q:** question\n**A:** answer (bold format)
    
    Args:
        text: Parsed text from PDF
        
    Returns:
        List of QAPair objects
    """
    qa_pairs = []
    
    # Try multiple patterns
    patterns = [
        # Pattern 1: Q: ... A: ...
        r'(?:Q|Question)[\s:]+(.+?)(?:\n|\r\n)+(?:A|Answer)[\s:]+(.+?)(?=(?:\n|\r\n){2,}|(?:Q|Question)[\s:]|$)',
        
        # Pattern 2: **Q:** ... **A:** ...
        r'\*\*(?:Q|Question)[:\s]+\*\*(.+?)(?:\n|\r\n)+\*\*(?:A|Answer)[:\s]+\*\*(.+?)(?=(?:\n|\r\n){2,}|\*\*(?:Q|Question)|$)',
        
        # Pattern 3: Numbered format with clear separation
        r'(?:^|\n)(\d+\.\s+.+?)(?:\n|\r\n)+(.+?)(?=(?:\n|\r\n){2,}|\d+\.\s+|$)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        temp_pairs = []
        
        for idx, match in enumerate(matches, 1):
            question = match.group(1).strip()
            answer = match.group(2).strip()
            
            # Clean up text
            question = _clean_text(question)
            answer = _clean_text(answer)
            
            # Validate Q&A pair
            if _is_valid_qa_pair(question, answer):
                temp_pairs.append(QAPair(
                    qa_id=idx,
                    question=question,
                    answer=answer
                ))
        
        # Use the pattern that found the most pairs
        if len(temp_pairs) > len(qa_pairs):
            qa_pairs = temp_pairs
    
    return qa_pairs


def _clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)      # Italic
    text = re.sub(r'#{1,6}\s+', '', text)         # Headers
    
    # Remove numbering at the start
    text = re.sub(r'^\d+\.\s+', '', text)
    
    return text.strip()


def _is_valid_qa_pair(question: str, answer: str) -> bool:
    """
    Validate if extracted Q&A pair is legitimate.
    
    Args:
        question: Question text
        answer: Answer text
        
    Returns:
        True if valid Q&A pair
    """
    # Minimum length requirements
    if len(question) < 10 or len(answer) < 10:
        return False
    
    # Maximum length check (prevent parsing errors)
    if len(question) > 5000 or len(answer) > 10000:
        return False
    
    # Check if question looks like a question
    question_indicators = ['?', 'what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe']
    has_question_indicator = any(indicator in question.lower() for indicator in question_indicators)
    
    # Check if answer looks like an answer (not another question)
    is_not_question = not (question.lower().strip() == answer.lower().strip())
    
    return has_question_indicator and is_not_question
