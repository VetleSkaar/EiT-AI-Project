from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from dotenv import load_dotenv
import os
import json
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.services.llm import analyze_draft_with_llm, AnalysisResult, MAX_DESCRIPTION_EXCERPT_LENGTH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    notice_id: str
    url: str
    title: str
    buyer: str
    cpv_codes: List[str]
    published_date: str
    deadline: str
    estimated_value_nok: Optional[int] = None
    procedure: str
    duration: str
    description_raw: str
    description_excerpt: str
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
        logger.warning(f"{data_path} not found. TF-IDF will not be available.")
        return
    
    with open(data_path, 'r') as f:
        notices_data = json.load(f)
    
    # Build TF-IDF matrix
    if notices_data:
        # Combine title and description_excerpt for each notice
        documents = [
            f"{notice.get('title', '')} {notice.get('description_excerpt', '')}"
            for notice in notices_data
        ]
        
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        
        logger.info(f"Loaded {len(notices_data)} notices and built TF-IDF matrix")


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


@app.post("/drafts/{draft_id}/analyze")
async def analyze_draft(draft_id: int):
    """Analyze a draft using TF-IDF retrieval and LLM analysis"""
    if draft_id not in drafts_db:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    if tfidf_vectorizer is None or tfidf_matrix is None:
        raise HTTPException(status_code=503, detail="TF-IDF not initialized")
    
    draft = drafts_db[draft_id]
    
    # Combine draft title and description
    draft_text = f"{draft['title']} {draft['description']}"
    
    # Transform draft text using the same TF-IDF vectorizer
    draft_vector = tfidf_vectorizer.transform([draft_text])
    
    # Calculate cosine similarity with all notices
    similarities = cosine_similarity(draft_vector, tfidf_matrix)[0]
    
    # Get top 10 similar notices
    top_k = 10
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Build response with top notices
    retrieved_notices = []
    for idx in top_indices:
        notice = notices_data[idx].copy()
        notice['similarity_score'] = float(similarities[idx])
        
        # Truncate description_excerpt to max length for storage and API response
        # Note: This is also done in LLM service for defensive programming
        if 'description_excerpt' in notice and notice['description_excerpt']:
            notice['description_excerpt'] = notice['description_excerpt'][:MAX_DESCRIPTION_EXCERPT_LENGTH]
        
        retrieved_notices.append(notice)
    
    # Call LLM to generate analysis
    try:
        llm_result = await analyze_draft_with_llm(
            draft_title=draft['title'],
            draft_description=draft['description'],
            similar_notices=retrieved_notices,
            cpv=draft.get('cpv'),
            ollama_url=os.getenv("OLLAMA_API_URL"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2")
        )
        
        # Convert the AnalysisResult to dict for storage
        analysis = llm_result.model_dump()
        
    except Exception as e:
        # If LLM fails, log the error but continue
        logger.error(f"LLM analysis failed for draft {draft_id}: {e}")
        # Return a minimal analysis structure
        analysis = {
            "error": str(e),
            "similar_notices_ranked": [],
            "overlap_summary": "LLM analysis unavailable",
            "qualitative_analysis": {
                "risk_management": "Not analyzed",
                "sustainability_social_values": "Not analyzed",
                "transparency_fair_competition": "Not analyzed",
                "innovation_forward_thinking": "Not analyzed"
            },
            "recommendation": {
                "decision": "review_required",
                "rationale": "LLM analysis failed"
            },
            "confidence": 0.0,
            "caveats": f"Analysis could not be completed: {str(e)}"
        }
    
    # Store the complete result under draft ID
    analysis_db[draft_id] = {
        "draft_id": draft_id,
        "retrieved_notices": retrieved_notices,
        "analysis": analysis
    }
    
    # Return both retrieved notices and analysis
    return {
        "retrieved_notices": retrieved_notices,
        "analysis": analysis
    }


@app.get("/drafts/{draft_id}/analysis", response_model=Analysis)
async def get_analysis(draft_id: int):
    """Get the analysis results for a draft"""
    if draft_id not in analysis_db:
        raise HTTPException(status_code=404, detail="Analysis not found for this draft")
    
    return analysis_db[draft_id]
