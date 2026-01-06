# Chat with Files

A FastAPI-based application that allows you to chat with your documents using DeepSeek R1 (via OpenRouter) and OpenAI embeddings with vector search.

## Features

- Upload and process various file formats (PDF, etc.)
- Vector-based document search using OpenAI embeddings
- Chat interface to query your documents using DeepSeek R1 (free tier)
- RESTful API with FastAPI

## Project Structure

```
chat-with-files/
│
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── ingest.py            # File processing and ingestion
│   ├── query.py             # Chat logic and query processing
│   ├── models.py            # Pydantic schemas
│   └── config.py            # Configuration settings
│
├── data/
│   ├── uploads/             # Uploaded files storage
│   └── vectordb/            # Vector database storage
│
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Example environment configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup

1. **Clone the repository** (if applicable)

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Set up OpenRouter API Key:**
   - Copy `.env.example` to `.env`
   - Get your API key from [OpenRouter](https://openrouter.ai/keys)
   - Add your key to `.env`:
   ```
   OPENAI_API_KEY=sk-or-v1-your-actual-key-here
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   ```

4. **Run the server:**
```powershell
cd backend
uvicorn main:app --reload
```

5. **Access the application:**
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## Usage

### Upload a File
```powershell
curl -X POST "http://localhost:8000/upload" -F "file=@document.pdf"
```

### Ask a Question
```powershell
curl -X POST "http://localhost:8000/ask" `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is this document about?\"}'
```

## Configuration

You can modify the following settings in `backend/config.py`:

- **OPENAI_MODEL**: Default is `deepseek/deepseek-r1-0528:free` (free DeepSeek R1 via OpenRouter)
  - Other options: `openai/gpt-4o-mini`, `anthropic/claude-3.5-sonnet`, etc.
  - See [OpenRouter models](https://openrouter.ai/models) for full list
- **OPENAI_BASE_URL**: Default is `https://openrouter.ai/api/v1`
- **OPENAI_EMBEDDING_MODEL**: Default is `text-embedding-3-small`
- **CHUNK_SIZE**: Size of text chunks (default: 800)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 150)
- **TOP_K**: Number of relevant chunks to retrieve (default: 4)

## Supported File Types

- PDF (.pdf)

See [ingest.py](backend/ingest.py) for implementation details.

## Technologies

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for LLM applications
- **DeepSeek R1**: Advanced reasoning model (via OpenRouter)
- **OpenRouter**: Unified API gateway for multiple LLM providers
- **OpenAI Embeddings**: Text embeddings for semantic search
- **FAISS**: Vector database for similarity search
- **Unstructured**: Document parsing library

## Notes

- Vector store is persisted in `data/vectordb` using FAISS
- Uploaded files are stored in `data/uploads`
- The application uses DeepSeek R1 (free tier) via OpenRouter for chat responses
- OpenAI embeddings are used for document vectorization (minimal cost)
- OpenRouter provides a unified API for multiple AI models

## License

MIT
