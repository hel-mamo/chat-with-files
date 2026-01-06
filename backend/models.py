from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str
    file_id: Optional[str] = None

class QuestionResponse(BaseModel):
    answer: str
    sources: list

class FileUploadResponse(BaseModel):
    status: str
    file_id: str
    filename: str
    uploaded_at: str

class FileInfo(BaseModel):
    id: str
    filename: str
    uploaded_at: str
    chunk_count: int
