import requests
import json
import os
from typing import Dict, Any

class LLMService:
    def __init__(self, use_mock: bool = None):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:latest")
        
        # Auto-detect if Ollama is available
        if use_mock is None:
            self.use_mock = not self._check_ollama_available()
        else:
            self.use_mock = use_mock
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze_draft(self, draft_content: str, similar_notices: list) -> Dict[str, Any]:
        """Analyze draft using LLM or mock data"""
        if self.use_mock:
            return self._mock_analysis(draft_content, similar_notices)
        else:
            return self._real_analysis(draft_content, similar_notices)
    
    def _mock_analysis(self, draft_content: str, similar_notices: list) -> Dict[str, Any]:
        """Return mock analysis for testing"""
        # Simple scoring based on content length and keywords
        content_lower = draft_content.lower()
        
        # Risk scoring
        risk_keywords = ["new", "untested", "experimental", "prototype"]
        risk_score = sum(1 for kw in risk_keywords if kw in content_lower) * 0.15 + 0.4
        risk_score = min(risk_score, 1.0)
        
        # Sustainability scoring
        sustainability_keywords = ["sustainable", "eco", "green", "renewable", "environment"]
        sustainability_score = sum(1 for kw in sustainability_keywords if kw in content_lower) * 0.2 + 0.3
        sustainability_score = min(sustainability_score, 1.0)
        
        # Competition scoring
        competition_score = 0.6 + len(similar_notices) * 0.03
        competition_score = min(competition_score, 1.0)
        
        # Innovation scoring
        innovation_keywords = ["innovative", "ai", "advanced", "smart", "modern"]
        innovation_score = sum(1 for kw in innovation_keywords if kw in content_lower) * 0.15 + 0.5
        innovation_score = min(innovation_score, 1.0)
        
        def get_level(score):
            if score >= 0.75:
                return "High"
            elif score >= 0.5:
                return "Medium"
            else:
                return "Low"
        
        return {
            "risk": {
                "score": round(risk_score, 2),
                "level": get_level(risk_score),
                "description": f"Based on content analysis, the risk level is {get_level(risk_score).lower()}. The draft contains elements that may require careful consideration."
            },
            "sustainability": {
                "score": round(sustainability_score, 2),
                "level": get_level(sustainability_score),
                "description": f"The sustainability score is {get_level(sustainability_score).lower()}. Consider incorporating more eco-friendly practices."
            },
            "competition": {
                "score": round(competition_score, 2),
                "level": get_level(competition_score),
                "description": f"Competition level is {get_level(competition_score).lower()} based on {len(similar_notices)} similar tenders found in the database."
            },
            "innovation": {
                "score": round(innovation_score, 2),
                "level": get_level(innovation_score),
                "description": f"The innovation aspect is rated as {get_level(innovation_score).lower()}. The draft shows potential for technological advancement."
            },
            "recommendation": f"Based on the analysis, this draft shows promise with a competition level of {get_level(competition_score).lower()}. Consider enhancing the sustainability aspects and addressing identified risks. The innovation potential is {get_level(innovation_score).lower()}, which could be a differentiating factor."
        }
    
    def _real_analysis(self, draft_content: str, similar_notices: list) -> Dict[str, Any]:
        """Use Ollama LLM for real analysis"""
        notices_text = "\n".join([f"- {notice['notice']}" for notice in similar_notices[:10]])
        
        prompt = f"""Analyze the following tender draft and provide a STRICT JSON response with the exact structure shown below.

Draft Content:
{draft_content}

Similar Tenders Found:
{notices_text}

You must respond with ONLY a JSON object (no other text) with this exact structure:
{{
    "risk": {{
        "score": <float between 0 and 1>,
        "level": "<High/Medium/Low>",
        "description": "<brief description>"
    }},
    "sustainability": {{
        "score": <float between 0 and 1>,
        "level": "<High/Medium/Low>",
        "description": "<brief description>"
    }},
    "competition": {{
        "score": <float between 0 and 1>,
        "level": "<High/Medium/Low>",
        "description": "<brief description>"
    }},
    "innovation": {{
        "score": <float between 0 and 1>,
        "level": "<High/Medium/Low>",
        "description": "<brief description>"
    }},
    "recommendation": "<comprehensive recommendation text>"
}}

Provide the JSON analysis now:"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = json.loads(result.get("response", "{}"))
                return analysis
            else:
                print(f"Ollama error: {response.status_code}, falling back to mock")
                return self._mock_analysis(draft_content, similar_notices)
                
        except Exception as e:
            print(f"LLM error: {e}, falling back to mock")
            return self._mock_analysis(draft_content, similar_notices)

# Global instance
llm_service = LLMService()
