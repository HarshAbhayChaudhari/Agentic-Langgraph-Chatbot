# WhatsApp Chat Query API

A FastAPI-based application that allows you to upload WhatsApp chat exports and query them using natural language. The application uses vector search with ChromaDB and Groq LLM for intelligent responses.

## Features

- Upload WhatsApp chat exports (.txt files)
- Vector-based search using ChromaDB
- Natural language querying using Groq LLM
- RESTful API endpoints
- CORS support for frontend integration

## Local Development

### Prerequisites

- Python 3.9+
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd whatsapp-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Vercel Deployment

### Prerequisites

- Vercel account
- Groq API key
- GitHub repository with your code

### Deployment Steps

1. **Push your code to GitHub**

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "New Project"
   - Import your GitHub repository

3. **Configure Environment Variables:**
   - In your Vercel project dashboard, go to "Settings" → "Environment Variables"
   - Add the following variables:
     - `GROQ_API_KEY`: Your Groq API key
     - `TAVILY_API_KEY`: (Optional) Your Tavily API key for web search

4. **Deploy:**
   - Vercel will automatically detect the Python project
   - The `vercel.json` configuration will handle the routing
   - Click "Deploy" to start the deployment process

### Important Notes for Vercel Deployment

- **ChromaDB**: The application automatically switches to in-memory storage when deployed on Vercel (serverless environment)
- **Data Persistence**: Data will not persist between function invocations on Vercel. For production use, consider using a cloud database
- **Cold Starts**: The first request may take longer due to serverless cold starts
- **Memory Limits**: Vercel has memory limits, so large chat files may need to be processed in chunks

### Alternative Deployment Options

For production use with data persistence, consider:
- **Railway**: Supports persistent storage
- **Render**: Offers persistent disk storage
- **DigitalOcean App Platform**: Good for Python applications
- **AWS/GCP/Azure**: For more control and scalability

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Upload
- `POST /api/v1/upload` - Upload WhatsApp chat file
  - Body: Form data with file field

### Chat
- `POST /api/v1/chat` - Query the chat
  - Body: JSON with `query` field

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM | Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | No |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB persistence directory | No (default: ./data/chroma_db) |
| `HOST` | Server host | No (default: 0.0.0.0) |
| `PORT` | Server port | No (default: 8000) |

## Project Structure

```
whatsapp-chatbot/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic models
│   ├── routes/              # API routes
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── data/                    # Data storage (local only)
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel configuration
└── README.md               # This file
```

## Troubleshooting

### Common Issues

1. **ChromaDB initialization errors**: Make sure the data directory is writable
2. **API key errors**: Verify your Groq API key is correctly set
3. **File upload issues**: Check file format and size limits
4. **Memory errors on Vercel**: Consider processing files in smaller chunks

### Local Development Issues

- If you get import errors, make sure you're in the correct directory
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your `.env` file is in the correct location

### Vercel Deployment Issues

- Check the Vercel function logs for detailed error messages
- Verify environment variables are set correctly
- Ensure your `vercel.json` configuration is correct
- Check that your Python version is compatible (3.9+)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
