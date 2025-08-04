import sys
import os

# Add the whatsapp-chatbot directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
whatsapp_dir = os.path.join(parent_dir, 'whatsapp-chatbot')

if whatsapp_dir not in sys.path:
    sys.path.insert(0, whatsapp_dir)

try:
    from app.main import app
    print(f"✅ Successfully imported FastAPI app from {whatsapp_dir}")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Create a minimal app if import fails
    from fastapi import FastAPI
    app = FastAPI(title="WhatsApp Chat API - Fallback")
    
    @app.get("/")
    async def root():
        return {
            "message": "WhatsApp Chat API is running (fallback mode)",
            "error": str(e),
            "python_path": sys.path,
            "current_dir": os.getcwd()
        }
    
    @app.get("/health")
    async def health():
        return {"status": "import_error", "error": str(e)}

# This is the entry point for Vercel serverless functions
# Vercel expects the app to be named 'app' 