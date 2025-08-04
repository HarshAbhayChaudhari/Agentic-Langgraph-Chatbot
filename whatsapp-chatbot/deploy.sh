#!/bin/bash

# WhatsApp Chatbot Vercel Deployment Script

echo "🚀 WhatsApp Chatbot Vercel Deployment Script"
echo "============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Please run this script from the whatsapp-chatbot directory."
    exit 1
fi

echo "✅ Vercel CLI found"
echo "✅ vercel.json configuration found"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before deploying"
    echo "   Required: GROQ_API_KEY"
    echo "   Optional: TAVILY_API_KEY"
fi

echo ""
echo "📋 Deployment Checklist:"
echo "1. ✅ Vercel CLI installed"
echo "2. ✅ vercel.json configured"
echo "3. ⚠️  .env file configured (if local testing)"
echo "4. ⚠️  Code pushed to GitHub"
echo "5. ⚠️  Environment variables set in Vercel dashboard"
echo ""

echo "🔧 Available commands:"
echo ""
echo "For local development:"
echo "  python main.py"
echo ""
echo "For Vercel deployment:"
echo "  vercel                    # Deploy to preview"
echo "  vercel --prod            # Deploy to production"
echo "  vercel --help            # Show all options"
echo ""
echo "For environment setup:"
echo "  vercel env add GROQ_API_KEY"
echo "  vercel env add TAVILY_API_KEY"
echo ""

echo "📚 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Go to vercel.com and create a new project"
echo "3. Import your GitHub repository"
echo "4. Set environment variables in Vercel dashboard"
echo "5. Deploy!"
echo ""

echo "🌐 Your API will be available at: https://your-project-name.vercel.app"
echo "📖 API documentation: https://your-project-name.vercel.app/docs" 