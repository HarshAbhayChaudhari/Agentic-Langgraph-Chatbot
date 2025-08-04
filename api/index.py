import sys
import os

# Add the whatsapp-chatbot directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'whatsapp-chatbot'))

try:
    from app.main import app
    print("Successfully imported FastAPI app from api/index.py")
except ImportError as e:
    print(f"Import error in api/index.py: {e}")
    # Create a minimal app if import fails
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "API index imported successfully", "error": str(e)}
    
    @app.get("/health")
    async def health():
        return {"status": "api_import_error", "error": str(e)}

# This is the entry point for Vercel serverless functions
# Vercel expects the app to be named 'app' 