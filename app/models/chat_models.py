from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str = Field(..., description="The query to search for in WhatsApp messages")
    collection_name: str = Field(default="whatsapp_messages", description="Name of the collection to search in")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of similar messages to retrieve")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer based on relevant messages")
    relevant_messages: List[str] = Field(..., description="List of relevant messages found")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the answer")
    query: str = Field(..., description="Original query") 