from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_routes, upload_routes

app = FastAPI(
    title="WhatsApp Chat Query API",
    description="API for querying WhatsApp chat messages using vector search",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload_routes.router, prefix="/api/v1", tags=["upload"])
app.include_router(chat_routes.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "WhatsApp Chat Query API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "whatsapp-chat-query-api"} 