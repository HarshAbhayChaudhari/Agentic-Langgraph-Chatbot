from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.models.chat_models import QueryRequest, QueryResponse
from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_messages(request: QueryRequest):
    """
    Query WhatsApp messages using vector similarity search
    """
    try:
        # Generate embedding for the query
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.generate_embeddings([request.query])[0]
        
        # Search similar messages in ChromaDB
        chroma_service = ChromaService()
        search_results = chroma_service.search_similar(
            collection_name=request.collection_name,
            query_embedding=query_embedding,
            top_k=request.top_k
        )
        
        if not search_results or not search_results.get('documents'):
            return QueryResponse(
                answer="I couldn't find any relevant messages in your chat history.",
                relevant_messages=[],
                confidence=0.0,
                query=request.query
            )
        
        # Prepare context from relevant messages
        relevant_messages = search_results['documents'][0]
        context = "\n".join(relevant_messages)
        
        # Generate answer using LLM
        llm_service = LLMService()
        answer = llm_service.generate_answer(request.query, context)
        
        # Calculate confidence based on similarity scores
        distances = search_results.get('distances', [[]])[0]
        confidence = 1.0 - min(distances) if distances else 0.5
        
        return QueryResponse(
            answer=answer,
            relevant_messages=relevant_messages,
            confidence=confidence,
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@router.get("/collections")
async def list_collections():
    """
    List all available collections
    """
    try:
        chroma_service = ChromaService()
        collections = chroma_service.list_collections()
        return {"collections": collections}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")

@router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """
    Delete a collection
    """
    try:
        chroma_service = ChromaService()
        chroma_service.delete_collection(collection_name)
        return {"message": f"Collection '{collection_name}' deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete collection: {str(e)}") 