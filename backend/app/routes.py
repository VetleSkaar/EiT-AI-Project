from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Draft, Analysis
from app.models import DraftCreate, DraftResponse, AnalysisResponse
from app.vector_store import vector_store
from app.llm_service import llm_service

router = APIRouter()

@router.post("/drafts", response_model=DraftResponse)
async def create_draft(draft: DraftCreate, db: Session = Depends(get_db)):
    """Create a new draft"""
    db_draft = Draft(title=draft.title, content=draft.content)
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft

@router.post("/drafts/{draft_id}/analyze", response_model=AnalysisResponse)
async def analyze_draft(draft_id: int, db: Session = Depends(get_db)):
    """Analyze a draft and return results"""
    # Get the draft
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    # Check if analysis already exists
    existing_analysis = db.query(Analysis).filter(Analysis.draft_id == draft_id).first()
    if existing_analysis:
        return existing_analysis
    
    # Search for similar notices
    similar_notices = vector_store.search(draft.content, top_k=10)
    
    # Get LLM analysis
    analysis_result = llm_service.analyze_draft(draft.content, similar_notices)
    
    # Save analysis
    db_analysis = Analysis(
        draft_id=draft_id,
        risk=analysis_result["risk"],
        sustainability=analysis_result["sustainability"],
        competition=analysis_result["competition"],
        innovation=analysis_result["innovation"],
        recommendation=analysis_result["recommendation"]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return db_analysis

@router.get("/drafts/{draft_id}/analysis", response_model=AnalysisResponse)
async def get_analysis(draft_id: int, db: Session = Depends(get_db)):
    """Get analysis for a draft"""
    analysis = db.query(Analysis).filter(Analysis.draft_id == draft_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found. Please analyze the draft first.")
    
    return analysis

@router.get("/drafts/{draft_id}", response_model=DraftResponse)
async def get_draft(draft_id: int, db: Session = Depends(get_db)):
    """Get a specific draft"""
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft

@router.get("/drafts", response_model=list[DraftResponse])
async def list_drafts(db: Session = Depends(get_db)):
    """List all drafts"""
    drafts = db.query(Draft).order_by(Draft.created_at.desc()).all()
    return drafts
