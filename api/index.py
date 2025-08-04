import sys
import os

# Add the whatsapp-chatbot directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
whatsapp_dir = os.path.join(parent_dir, 'whatsapp-chatbot')

if whatsapp_dir not in sys.path:
    sys.path.insert(0, whatsapp_dir)

try:
    # Import a lightweight version of the app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Create FastAPI app
    app = FastAPI(
        title="WhatsApp Chat Query API (Lightweight)",
        description="Lightweight API for WhatsApp chat queries",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Simple models
    class ChatRequest(BaseModel):
        query: str
        messages: List[str] = []
    
    class ChatResponse(BaseModel):
        answer: str
        query: str
    
    # Simple in-memory storage (for demo purposes)
    chat_messages = []
    
    @app.get("/")
    async def root():
        return {"message": "WhatsApp Chat Query API (Lightweight) is running!"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "whatsapp-chat-query-api-lightweight"}
    
    @app.post("/api/v1/chat", response_model=ChatResponse)
    async def chat_with_messages(request: ChatRequest):
        """
        Simple chat endpoint without heavy dependencies
        """
        try:
            # Simple response for demo
            answer = f"Received your query: '{request.query}'. This is a lightweight version without full LLM integration."
            
            return ChatResponse(
                answer=answer,
                query=request.query
            )
        except Exception as e:
            return ChatResponse(
                answer=f"Error processing query: {str(e)}",
                query=request.query
            )
    
    @app.post("/api/v1/upload")
    async def upload_chat_file(file_content: str):
        """
        Simple upload endpoint
        """
        try:
            # Store messages in memory (for demo)
            global chat_messages
            messages = file_content.split('\n')
            chat_messages.extend(messages)
            
            return {
                "message": f"Uploaded {len(messages)} messages successfully",
                "total_messages": len(chat_messages)
            }
        except Exception as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    @app.get("/api/v1/status")
    async def get_status():
        """
        Get current status
        """
        return {
            "status": "ready",
            "total_messages": len(chat_messages),
            "version": "lightweight"
        }
    
    print(f"✅ Successfully created lightweight FastAPI app")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Create a minimal app if import fails
    from fastapi import FastAPI
    app = FastAPI(title="WhatsApp Chat API - Fallback")
    
    @app.get("/")
    async def root():
        return {
            "message": "WhatsApp Chat API is running (fallback mode)",
            "error": str(e)
        }
    
    @app.get("/health")
    async def health():
        return {"status": "import_error", "error": str(e)}

# This is the entry point for Vercel serverless functions
# Vercel expects the app to be named 'app' 