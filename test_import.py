#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""
import sys
import os

print("Testing imports...")

# Test the api/index.py approach
print("\n1. Testing api/index.py approach:")
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'whatsapp-chatbot'))

try:
    from app.main import app
    print("✅ Successfully imported FastAPI app from api/index.py")
    print(f"App title: {app.title}")
except ImportError as e:
    print(f"❌ Import error: {e}")

# Test the vercel_app.py approach
print("\n2. Testing vercel_app.py approach:")
sys.path = [os.path.dirname(os.path.abspath(__file__))]  # Reset path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whatsapp-chatbot'))

try:
    from app.main import app
    print("✅ Successfully imported FastAPI app from vercel_app.py")
    print(f"App title: {app.title}")
except ImportError as e:
    print(f"❌ Import error: {e}")

print("\nImport test completed!") 