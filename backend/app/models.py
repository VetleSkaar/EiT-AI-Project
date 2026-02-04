from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DraftCreate(BaseModel):
    title: str
    content: str

class DraftResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RiskAnalysis(BaseModel):
    score: float
    level: str
    description: str

class SustainabilityAnalysis(BaseModel):
    score: float
    level: str
    description: str

class CompetitionAnalysis(BaseModel):
    score: float
    level: str
    description: str

class InnovationAnalysis(BaseModel):
    score: float
    level: str
    description: str

class AnalysisResponse(BaseModel):
    id: int
    draft_id: int
    risk: RiskAnalysis
    sustainability: SustainabilityAnalysis
    competition: CompetitionAnalysis
    innovation: InnovationAnalysis
    recommendation: str
    created_at: datetime
    
    class Config:
        from_attributes = True
