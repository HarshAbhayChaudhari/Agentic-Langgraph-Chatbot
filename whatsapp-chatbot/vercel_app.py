import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# This is the entry point for Vercel serverless functions
# Vercel expects the app to be named 'app' 