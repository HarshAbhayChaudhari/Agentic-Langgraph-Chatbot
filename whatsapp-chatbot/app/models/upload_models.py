from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ProcessingStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UploadResponse(BaseModel):
    message: str
    filename: str
    status: ProcessingStatus
    collection_name: str 