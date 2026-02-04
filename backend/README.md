# Backend - Draft Analysis API

FastAPI backend for analyzing tender drafts using AI.

## Features

- SQLite database for storing drafts and analyses
- Simple hash-based vector similarity search for finding related tenders
- Ollama integration for LLM analysis (with mock mode fallback)
- RESTful API endpoints

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Install and run Ollama:
```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull qwen2.5:latest
# or
ollama pull mistral:latest
```

3. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

- `OLLAMA_URL`: Ollama API URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: qwen2.5:latest)

## API Endpoints

### POST /drafts
Create a new draft.

Request:
```json
{
  "title": "Draft Title",
  "content": "Draft content..."
}
```

Response:
```json
{
  "id": 1,
  "title": "Draft Title",
  "content": "Draft content...",
  "created_at": "2024-01-01T00:00:00"
}
```

### POST /drafts/{id}/analyze
Analyze a draft and generate insights.

Response:
```json
{
  "id": 1,
  "draft_id": 1,
  "risk": {
    "score": 0.65,
    "level": "Medium",
    "description": "..."
  },
  "sustainability": {
    "score": 0.75,
    "level": "High",
    "description": "..."
  },
  "competition": {
    "score": 0.80,
    "level": "High",
    "description": "..."
  },
  "innovation": {
    "score": 0.70,
    "level": "Medium",
    "description": "..."
  },
  "recommendation": "Overall recommendation...",
  "created_at": "2024-01-01T00:00:00"
}
```

### GET /drafts/{id}/analysis
Retrieve existing analysis for a draft.

### GET /drafts
List all drafts.

### GET /drafts/{id}
Get a specific draft.

## Mock Mode

The system automatically falls back to mock mode if Ollama is not available. Mock mode generates simple keyword-based analyses for testing purposes.

To force mock mode, set the environment variable:
```bash
USE_MOCK_LLM=true
```
