from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
import os
import tempfile
from app.services.file_parser import FileParser
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
    Upload and process files (TXT, PDF, DOCX)
    """
    # Validate file type
    allowed_extensions = ['.txt', '.pdf', '.docx']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save uploaded file temporarily with proper extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Get file info
        file_parser = FileParser()
        file_info = file_parser.get_file_info(temp_file_path)
        
        # Start background processing
        background_tasks.add_task(
            process_file,
            temp_file_path,
            collection_name,
            file_info
        )
        
        return UploadResponse(
            message=f"File uploaded successfully. Processing started in background. File type: {file_info['extension']}",
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

async def process_file(file_path: str, collection_name: str, file_info: dict):
    """
    Background task to process the uploaded file
    """
    try:
        # Parse file based on its type
        file_parser = FileParser()
        messages = file_parser.parse_file(file_path)
        
        if not messages:
            print(f"No content extracted from file: {file_info['filename']}")
            return
        
        print(f"Extracted {len(messages)} messages/documents from {file_info['filename']}")
        
        # Create chunks from messages
        chunks = create_chunks_from_messages(messages, chunk_size=512)
        
        # Generate embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Prepare metadata for each chunk
        metadata = []
        for i, message in enumerate(messages):
            chunk_metadata = {
                "source": message.get('source', 'unknown'),
                "sender": message.get('sender', 'unknown'),
                "timestamp": message.get('timestamp', ''),
                "file_type": file_info['extension'],
                "original_filename": file_info['filename']
            }
            
            # Add source-specific metadata
            if message.get('source') == 'pdf':
                chunk_metadata.update({
                    "page": message.get('page', 0),
                    "paragraph_id": message.get('paragraph_id', 0)
                })
            elif message.get('source') == 'docx':
                chunk_metadata.update({
                    "paragraph_id": message.get('paragraph_id', 0),
                    "table_id": message.get('table_id', None),
                    "row_id": message.get('row_id', None)
                })
            elif message.get('source') == 'whatsapp_chat':
                chunk_metadata.update({
                    "date": message.get('date', '').isoformat() if message.get('date') else ''
                })
            
            metadata.append(chunk_metadata)
        
        # Store in ChromaDB
        chroma_service = ChromaService()
        chroma_service.store_embeddings(
            collection_name=collection_name,
            documents=chunks,
            embeddings=embeddings,
            metadata=metadata
        )
        
        # Clean up temporary file
        os.unlink(file_path)
        
        print(f"Successfully processed {len(chunks)} chunks for collection: {collection_name}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        # Clean up temporary file even if processing fails
        if os.path.exists(file_path):
            os.unlink(file_path)

def create_chunks_from_messages(messages: list, chunk_size: int = 512) -> list:
    """
    Create text chunks from parsed messages
    """
    chunks = []
    current_chunk = ""
    
    for message in messages:
        # Format message based on source
        if message.get('source') == 'whatsapp_chat':
            message_text = f"[{message['sender']}]: {message['message']}"
        elif message.get('source') == 'pdf':
            message_text = f"[Page {message.get('page', 'N/A')}]: {message['message']}"
        elif message.get('source') == 'docx':
            if message.get('table_id'):
                message_text = f"[Table {message.get('table_id')} Row {message.get('row_id')}]: {message['message']}"
            else:
                message_text = f"[Paragraph {message.get('paragraph_id', 'N/A')}]: {message['message']}"
        else:
            message_text = f"[{message['sender']}]: {message['message']}"
        
        # If adding this message would exceed chunk size, save current chunk
        if len(current_chunk + " " + message_text) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = message_text
        else:
            if current_chunk:
                current_chunk += " " + message_text
            else:
                current_chunk = message_text
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks 