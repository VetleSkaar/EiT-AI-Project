from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for TF-IDF
notices_data = []
tfidf_vectorizer = None
tfidf_matrix = None

# In-memory storage for drafts
drafts_db: Dict[int, dict] = {}
analysis_db: Dict[int, dict] = {}
next_draft_id = 1


# Pydantic models
class DraftCreate(BaseModel):
    title: str
    description: str
    cpv: Optional[str] = None


class Draft(BaseModel):
    id: int
    title: str
    description: str
    cpv: Optional[str] = None


class Notice(BaseModel):
    id: str
    title: str
    description: str
    cpv: str
    similarity_score: float


class Analysis(BaseModel):
    draft_id: int
    top_notices: List[Notice]


@app.on_event("startup")
async def startup_event():
    """Load notices data and build TF-IDF on startup"""
    global notices_data, tfidf_vectorizer, tfidf_matrix
    
    # Load notices.cleaned.json
    data_path = Path(__file__).parent / "data" / "notices.cleaned.json"
    
    if not data_path.exists():
        print(f"Warning: {data_path} not found. TF-IDF will not be available.")
        return
    
    with open(data_path, 'r') as f:
        notices_data = json.load(f)
    
    # Build TF-IDF matrix
    if notices_data:
        # Combine title and description for each notice
        documents = [
            f"{notice.get('title', '')} {notice.get('description', '')}"
            for notice in notices_data
        ]
        
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        
        print(f"Loaded {len(notices_data)} notices and built TF-IDF matrix")


@app.get("/")
async def root():
    return {"message": "Welcome to the EiT AI Project API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/drafts", response_model=Draft)
async def create_draft(draft: DraftCreate):
    """Create a new draft with title, description, and optional CPV"""
    global next_draft_id
    
    draft_id = next_draft_id
    next_draft_id += 1
    
    draft_data = {
        "id": draft_id,
        "title": draft.title,
        "description": draft.description,
        "cpv": draft.cpv
    }
    
    drafts_db[draft_id] = draft_data
    
    return draft_data


@app.post("/drafts/{id}/analyze")
async def analyze_draft(id: int):
    """Analyze a draft and rank similar notices using TF-IDF cosine similarity"""
    if id not in drafts_db:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    if tfidf_vectorizer is None or tfidf_matrix is None:
        raise HTTPException(status_code=503, detail="TF-IDF not initialized")
    
    draft = drafts_db[id]
    
    # Combine draft title and description
    draft_text = f"{draft['title']} {draft['description']}"
    
    # Transform draft text using the same TF-IDF vectorizer
    draft_vector = tfidf_vectorizer.transform([draft_text])
    
    # Calculate cosine similarity with all notices
    similarities = cosine_similarity(draft_vector, tfidf_matrix)[0]
    
    # Get top 5 similar notices
    top_k = 5
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Build response with top notices
    top_notices = []
    for idx in top_indices:
        notice = notices_data[idx].copy()
        notice['similarity_score'] = float(similarities[idx])
        top_notices.append(notice)
    
    # Store analysis result
    analysis_result = {
        "draft_id": id,
        "top_notices": top_notices
    }
    analysis_db[id] = analysis_result
    
    return {"message": "Analysis complete", "draft_id": id}


@app.get("/drafts/{id}/analysis", response_model=Analysis)
async def get_analysis(id: int):
    """Get the analysis results for a draft"""
    if id not in analysis_db:
        raise HTTPException(status_code=404, detail="Analysis not found for this draft")
    
    return analysis_db[id]
