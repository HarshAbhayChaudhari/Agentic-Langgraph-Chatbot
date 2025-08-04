#!/usr/bin/env python3
"""
Test script to verify Vercel import path works correctly
"""
import sys
import os

print("Testing Vercel import path...")

# Simulate the Vercel environment
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
whatsapp_dir = os.path.join(parent_dir, 'whatsapp-chatbot')

print(f"Current directory: {current_dir}")
print(f"Parent directory: {parent_dir}")
print(f"WhatsApp directory: {whatsapp_dir}")
print(f"WhatsApp directory exists: {os.path.exists(whatsapp_dir)}")

if whatsapp_dir not in sys.path:
    sys.path.insert(0, whatsapp_dir)

print(f"Python path: {sys.path}")

try:
    from app.main import app
    print("✅ Successfully imported FastAPI app")
    print(f"App title: {app.title}")
    print(f"App routes: {[route.path for route in app.routes]}")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Available files in whatsapp_dir: {os.listdir(whatsapp_dir) if os.path.exists(whatsapp_dir) else 'Directory not found'}")

print("\nVercel import test completed!") 