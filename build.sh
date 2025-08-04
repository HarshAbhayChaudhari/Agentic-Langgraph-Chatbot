#!/bin/bash

# Build script for Vercel deployment
# Tries to use uv if available, otherwise falls back to pip

echo "Starting build process..."

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv package manager..."
    uv pip install -r requirements.txt
else
    echo "uv not available, using pip..."
    pip install -r requirements.txt
fi

echo "Build completed!" 