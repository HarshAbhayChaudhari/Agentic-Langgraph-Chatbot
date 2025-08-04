from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.llm_service import LLMService
from app.services.chroma_service import ChromaService
from app.services.embedding_service import EmbeddingService

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    collection_name: str = "whatsapp_messages"
    top_k: int = 5

class ChatResponse(BaseModel):
    answer: str
    sources: list
    query: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_messages(request: ChatRequest):
    """
    Query WhatsApp messages using natural language
    """
    try:
        # Generate embedding for the query
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.generate_embeddings([request.query])[0]
        
        # Search for similar messages
        chroma_service = ChromaService()
        search_results = chroma_service.search_similar(
            collection_name=request.collection_name,
            query_embedding=query_embedding,
            top_k=request.top_k
        )
        
        # Extract context from search results
        context = "\n".join([doc for doc in search_results.get("documents", [])])
        
        # Generate answer using LLM
        llm_service = LLMService()
        answer = llm_service.generate_answer(request.query, context)
        
        return ChatResponse(
            answer=answer,
            sources=search_results.get("documents", []),
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}") 