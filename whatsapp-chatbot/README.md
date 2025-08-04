# WhatsApp Chat Query API

A FastAPI backend application that allows you to upload WhatsApp chat exports, create vector embeddings, and query your messages using natural language.

## Features

- 📁 **File Upload**: Upload WhatsApp chat export files (.txt format)
- 🔍 **Vector Search**: Create embeddings and store them in ChromaDB
- 🤖 **LLM Integration**: Use Groq API for natural language querying
- 🔄 **Background Processing**: Process files asynchronously
- 📊 **Collection Management**: Manage multiple chat collections
- 🏥 **Health Checks**: API health monitoring

## Prerequisites

- Python 3.8+
- Groq API key
- WhatsApp chat export file (.txt format)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd whatsapp-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your API keys
   ```

5. **Create data directory**
   ```bash
   mkdir -p data/chroma_db
   ```

## Usage

### Starting the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Upload Chat File
```bash
POST /api/v1/upload
Content-Type: multipart/form-data

file: <your-chat-file.txt>
collection_name: "my_chat" (optional)
```

#### Query Messages
```bash
POST /api/v1/query
Content-Type: application/json

{
  "query": "What did I say about the meeting?",
  "collection_name": "my_chat",
  "top_k": 5
}
```

#### Get Processing Status
```bash
GET /api/v1/status/{collection_name}
```

#### List Collections
```bash
GET /api/v1/collections
```

#### Delete Collection
```bash
DELETE /api/v1/collections/{collection_name}
```

### WhatsApp Chat Export Format

The application expects WhatsApp chat exports in the following format:
```
[DD/MM/YYYY, HH:MM:SS] Sender: Message
```

Example:
```
[31/12/2023, 14:30:25] John Doe: Happy New Year!
[31/12/2023, 14:31:00] You: Thanks! Same to you!
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Deployment

### Local Development
```bash
python main.py
```

### Production with Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Vercel Deployment

1. Create a `vercel.json` file:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. Deploy to Vercel:
```bash
vercel --prod
```

## Project Structure

```
whatsapp-chatbot/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic models
│   ├── routes/              # API routes
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── data/                    # ChromaDB data storage
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
└── README.md               # This file
```

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key
- `TAVILY_API_KEY`: Optional Tavily API key
- `CHROMA_PERSIST_DIRECTORY`: ChromaDB storage directory
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### ChromaDB Settings

The application uses ChromaDB for vector storage. Data is persisted in the `./data/chroma_db` directory by default.

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Error**
   - Ensure the data directory exists
   - Check file permissions

2. **LLM Initialization Error**
   - Verify your Groq API key is set correctly
   - Check internet connectivity

3. **File Upload Error**
   - Ensure the file is in .txt format
   - Check file size limits

### Logs

The application logs to stdout. Check the console output for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
