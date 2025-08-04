import sys
import os

# Add the whatsapp-chatbot directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whatsapp-chatbot'))

from app.main import app

# This is the entry point for Vercel serverless functions
# Vercel expects the app to be named 'app' 