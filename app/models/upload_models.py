from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class ProcessingStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileInfo(BaseModel):
    filename: str
    extension: str
    size_bytes: int
    size_mb: float
    supported: bool

class UploadResponse(BaseModel):
    message: str
    filename: str
    status: ProcessingStatus
    collection_name: str
    file_info: Optional[FileInfo] = None 