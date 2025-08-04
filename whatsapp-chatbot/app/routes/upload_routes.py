from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
import os
import tempfile
from app.services.whatsapp_parser import WhatsAppParser
from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService
from app.models.upload_models import UploadResponse, ProcessingStatus

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_chat_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    collection_name: Optional[str] = "whatsapp_messages"
):
    """
    Upload and process WhatsApp chat export file
    """
    # Validate file type
    if not file.filename.endswith('.txt'):
        raise HTTPException(
            status_code=400, 
            detail="Only .txt files are supported"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Start background processing
        background_tasks.add_task(
            process_chat_file,
            temp_file_path,
            collection_name
        )
        
        return UploadResponse(
            message="File uploaded successfully. Processing started in background.",
            filename=file.filename,
            status=ProcessingStatus.PROCESSING,
            collection_name=collection_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/status/{collection_name}")
async def get_processing_status(collection_name: str):
    """
    Get the processing status and collection info
    """
    try:
        chroma_service = ChromaService()
        collection_info = chroma_service.get_collection_info(collection_name)
        
        return {
            "collection_name": collection_name,
            "status": "completed" if collection_info else "processing",
            "document_count": collection_info.get("count", 0) if collection_info else 0,
            "last_updated": collection_info.get("last_updated", None) if collection_info else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

async def process_chat_file(file_path: str, collection_name: str):
    """
    Background task to process the uploaded chat file
    """
    try:
        # Parse WhatsApp messages
        parser = WhatsAppParser()
        messages = parser.parse_file(file_path)
        
        # Create chunks
        chunks = parser.create_chunks(messages, chunk_size=512)
        
        # Generate embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Store in ChromaDB
        chroma_service = ChromaService()
        chroma_service.store_embeddings(
            collection_name=collection_name,
            documents=chunks,
            embeddings=embeddings
        )
        
        # Clean up temporary file
        os.unlink(file_path)
        
        print(f"Successfully processed {len(chunks)} chunks for collection: {collection_name}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        # Clean up temporary file even if processing fails
        if os.path.exists(file_path):
            os.unlink(file_path) 