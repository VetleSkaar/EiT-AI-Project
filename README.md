# EiT-AI-Project

MVP Monorepo for Tender Draft Analysis with AI

## Overview

This is a full-stack application for analyzing tender drafts using AI/LLM. It consists of:

- **Backend**: FastAPI with SQLite, FAISS vector store, sentence-transformers embeddings, and Ollama LLM integration
- **Frontend**: Vue 3 + Vite single-page application

## Features

### Backend
- ✅ RESTful API with FastAPI
- ✅ SQLite database for drafts and analyses
- ✅ FAISS vector store for similarity search
- ✅ Sentence-transformers for embeddings (all-MiniLM-L6-v2)
- ✅ Ollama LLM integration (Qwen2.5 / Mistral)
- ✅ **Mock LLM mode** for testing without Ollama
- ✅ Auto-detection of Ollama availability

### Frontend
- ✅ Vue 3 with Vite
- ✅ Draft submission form
- ✅ Analysis results page
- ✅ Editable rubric for customization
- ✅ Responsive UI design

### Analysis Criteria
- **Risk Assessment**: Evaluates potential risks and challenges
- **Sustainability**: Assesses environmental and long-term impact
- **Competition**: Analyzes market competition (based on similar tenders)
- **Innovation**: Measures technological and process innovation
- **Recommendation**: Provides actionable insights

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app and routes
│   │   ├── database.py     # SQLite models
│   │   ├── models.py       # Pydantic schemas
│   │   ├── routes.py       # API endpoints
│   │   ├── vector_store.py # FAISS similarity search
│   │   └── llm_service.py  # Ollama LLM integration
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                # Vue 3 frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── DraftForm.vue
│   │   │   ├── AnalysisResults.vue
│   │   │   └── RubricEditor.vue
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── api.js          # API client
│   ├── package.json
│   └── .env
│
└── README.md               # This file
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- (Optional) Ollama with Qwen2.5 or Mistral model

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. **(Optional)** Install and configure Ollama:
```bash
# Install from https://ollama.ai
# Then pull a model:
ollama pull qwen2.5:latest
# or
ollama pull mistral:latest
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Create a Draft**:
   - Fill in the title and content in the draft form
   - Click "Submit Draft"

2. **View Analysis**:
   - The system automatically analyzes the draft
   - Shows risk, sustainability, competition, and innovation scores
   - Displays recommendations

3. **Customize Rubric**:
   - Click "Edit Rubric" to customize evaluation criteria
   - Adjust weights and scoring criteria
   - Settings are saved in browser localStorage

## API Endpoints

### POST /drafts
Create a new draft

**Request:**
```json
{
  "title": "Smart City Infrastructure",
  "content": "Implementation of IoT sensors..."
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Smart City Infrastructure",
  "content": "Implementation of IoT sensors...",
  "created_at": "2024-01-01T00:00:00"
}
```

### POST /drafts/{id}/analyze
Analyze a draft and generate insights

**Response:**
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
  "recommendation": "...",
  "created_at": "2024-01-01T00:00:00"
}
```

### GET /drafts/{id}/analysis
Retrieve existing analysis

### GET /drafts
List all drafts

### GET /drafts/{id}
Get a specific draft

## Mock LLM Mode

The system includes a **mock LLM mode** that automatically activates when Ollama is not available. This allows you to:

- Test the application without setting up Ollama
- Develop and demo the UI
- Get keyword-based analysis

The mock mode:
- Analyzes content using keyword matching
- Generates scores based on content patterns
- Returns consistent JSON responses
- Automatically falls back if Ollama fails

### Environment Variables

Backend:
- `OLLAMA_URL`: Ollama API URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL`: Model name (default: `qwen2.5:latest`)

Frontend:
- `VITE_API_URL`: Backend API URL (default: `http://localhost:8000`)

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **FAISS**: Efficient similarity search
- **sentence-transformers**: State-of-the-art embeddings
- **Ollama**: Local LLM inference

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Vite**: Next-generation build tool
- **Axios**: HTTP client

## Development

### Backend Development
```bash
cd backend
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Access API docs
open http://localhost:8000/docs
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install

# Run dev server with hot reload
npm run dev

# Build for production
npm run build
```

## Sample Data

The system comes pre-loaded with 15 sample tender notices for similarity search:
- Construction projects
- IT/Software development
- Healthcare solutions
- Sustainability initiatives
- Smart city projects
- And more...

## Future Enhancements

- [ ] User authentication
- [ ] Draft versioning
- [ ] Export to PDF
- [ ] Batch analysis
- [ ] Custom embedding models
- [ ] Multi-language support
- [ ] Analytics dashboard

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.