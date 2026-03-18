"""
LLM Service for calling Ollama API to analyze procurement drafts.
"""
import os
import json
import logging
import time
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
import httpx

logger = logging.getLogger(__name__)


# Configuration constants
MAX_DESCRIPTION_EXCERPT_LENGTH = 200


class SimilarNotice(BaseModel):
    """A similar notice with ranking information."""
    notice_id: str = Field(..., description="The ID of the similar notice")
    score: float = Field(..., description="Similarity score")
    title: Optional[str] = Field(None, description="Title of the notice")
    buyer: Optional[str] = Field(None, description="Buyer organization")
    cpv_codes: Optional[List[str]] = Field(None, description="CPV codes")
    published_date: Optional[str] = Field(None, description="Publication date")


class QualitativeAnalysis(BaseModel):
    """Qualitative analysis of the procurement draft."""
    risk_management: str = Field(..., description="Analysis of risk management aspects")
    sustainability_social_values: str = Field(..., description="Analysis of sustainability and social values")
    transparency_fair_competition: str = Field(..., description="Analysis of transparency and fair competition")
    innovation_forward_thinking: str = Field(..., description="Analysis of innovation and forward thinking")


class Recommendation(BaseModel):
    """Recommendation for the procurement draft."""
    decision: str = Field(..., description="The recommended decision (e.g., 'approve', 'revise', 'reject')")
    rationale: str = Field(..., description="Rationale for the recommendation")


class AnalysisResult(BaseModel):
    """Complete analysis result from LLM."""
    similar_notices_ranked: List[SimilarNotice] = Field(
        default_factory=list,
        description="Ranked list of similar notices"
    )
    overlap_summary: str = Field(..., description="Summary of overlaps with similar notices")
    qualitative_analysis: QualitativeAnalysis = Field(..., description="Qualitative analysis")
    recommendation: Recommendation = Field(..., description="Recommendation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)")
    caveats: str = Field(default="", description="Caveats and limitations of the analysis")


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    # Configuration constants
    MAX_DESCRIPTION_LENGTH = 200
    DEFAULT_TIMEOUT = 240.0
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: The base URL for Ollama API. If None, uses OLLAMA_API_URL from env
                     or defaults to http://host.docker.internal:11434
            model: The model to use for generation
            timeout: Timeout in seconds for API calls
        """
        self.base_url = base_url or os.getenv("OLLAMA_API_URL", "http://host.docker.internal:11434")
        self.model = model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
        self.timeout = timeout
        self.chat_endpoint = f"{self.base_url}/api/chat"
    
    async def generate_analysis(
        self,
        draft_title: str,
        draft_description: str,
        similar_notices: List[dict],
        cpv: Optional[str] = None
    ) -> AnalysisResult:
        """
        Generate analysis for a procurement draft using Ollama.
        
        Args:
            draft_title: Title of the procurement draft
            draft_description: Description of the procurement draft
            similar_notices: List of similar notices found via TF-IDF
            cpv: Optional CPV code
        
        Returns:
            AnalysisResult object with the analysis
        
        Raises:
            httpx.HTTPError: If the API call fails
            ValidationError: If the response cannot be parsed into AnalysisResult
        """
        # Prepare the context from similar notices
        similar_context = self._format_similar_notices(similar_notices)
        
        # Create the prompt
        prompt = self._create_analysis_prompt(
            draft_title, draft_description, similar_context, cpv
        )
        
        # First attempt with normal prompt
        try:
            response_text = await self._call_ollama(prompt)
            return self._parse_response(response_text)
        except (ValidationError, json.JSONDecodeError) as e:
            # Retry with stricter JSON-only prompt
            logger.warning(f"First parse attempt failed: {e}. Retrying with stricter prompt.")
            strict_prompt = self._create_strict_json_prompt(prompt)
            response_text = await self._call_ollama(strict_prompt)
            return self._parse_response(response_text)
    
    def _format_similar_notices(self, notices: List[dict]) -> str:
        """Format similar notices for context, with description truncated to max length."""
        if not notices:
            return "No similar notices found."
        
        formatted = []
        for i, notice in enumerate(notices, 1):
            # Get description and truncate if needed (defensive programming)
            desc = notice.get('description_excerpt', 'N/A')
            if desc != 'N/A' and len(desc) > MAX_DESCRIPTION_EXCERPT_LENGTH:
                desc = desc[:MAX_DESCRIPTION_EXCERPT_LENGTH]
            
            notice_info = [
                f"Notice {i}:",
                f"  ID: {notice.get('notice_id', 'N/A')}",
                f"  Title: {notice.get('title', 'N/A')}",
                f"  Buyer: {notice.get('buyer', 'N/A')}",
                f"  CPV: {', '.join(notice.get('cpv_codes', []))}",
                f"  Published: {notice.get('published_date', 'N/A')}",
                f"  Similarity Score: {notice.get('similarity_score', 0):.3f}",
                f"  Description: {desc}"
            ]
            formatted.append("\n".join(notice_info))
        
        return "\n\n".join(formatted)
    
    def _create_analysis_prompt(
        self,
        title: str,
        description: str,
        similar_context: str,
        cpv: Optional[str]
    ) -> str:
        """Create a compact, strict analysis prompt for Ollama."""
        cpv_text = f"\nCPV Code: {cpv}" if cpv else ""

        return f"""You are analyzing a draft public procurement notice for a prototype decision-support system.

    Use ONLY the draft and the provided similar notices.
    Do NOT invent facts, outcomes, supplier behavior, delays, or budget overruns unless they are clearly stated in the provided text.
    If information is missing, state that briefly in caveats.

    PROCUREMENT DRAFT
    Title: {title}
    Description: {description}{cpv_text}

    SIMILAR NOTICES
    {similar_context}

    TASK
    Compare the draft to the similar notices and produce a structured analysis.

    ANALYSIS RULES
    - Base the analysis only on the provided text.
    - Keep overlap_summary to 3-5 sentences.
    - Keep each qualitative_analysis field to 2-3 sentences.
    - Keep recommendation.rationale to 2-3 sentences.
    - Keep caveats to 1-3 short sentences.
    - confidence must be a number between 0.0 and 1.0.
    - recommendation.decision must be exactly one of:
    "approve", "revise", "reject"
    - similar_notices_ranked should include the most relevant retrieved notices first.
    - Preserve notice_id and score values from the retrieved notices when possible.
    - Return ONLY valid JSON.

    QUALITATIVE PRIORITIES
    1. Risk Management:
    Assess implementation risk, complexity, dependency risk, unclear scope, integration risk, and contract safeguards.
    2. Sustainability & Social Values:
    Assess whether the draft mentions environmental, social, or ethical considerations.
    3. Transparency & Fair Competition:
    Assess whether the scope and requirements appear clear, fair, and accessible to multiple bidders.
    4. Innovation & Forward-Thinking:
    Assess whether the draft appears modern, future-ready, and open to appropriate technological development.

    REQUIRED JSON SCHEMA
    {{
    "similar_notices_ranked": [
        {{
        "notice_id": "string",
        "score": 0.0,
        "title": "string or null",
        "buyer": "string or null",
        "cpv_codes": ["string"] or null,
        "published_date": "string or null"
        }}
    ],
    "overlap_summary": "string",
    "qualitative_analysis": {{
        "risk_management": "string",
        "sustainability_social_values": "string",
        "transparency_fair_competition": "string",
        "innovation_forward_thinking": "string"
    }},
    "recommendation": {{
        "decision": "approve | revise | reject",
        "rationale": "string"
    }},
    "confidence": 0.0,
    "caveats": "string"
    }}

    Every top-level field in the JSON schema is required. If information is limited, still include the field and keep the value brief.
    Do not omit caveats.

    Return ONLY the JSON object. No markdown. No code block. No extra commentary."""
    
    def _create_strict_json_prompt(self, original_prompt: str) -> str:
        """Create a stricter retry prompt for JSON-only output."""
        return f"""{original_prompt}

    CRITICAL JSON RETRY INSTRUCTIONS:
    - Return ONLY one valid JSON object.
    - Do NOT use markdown or code fences.
    - Do NOT include explanations before or after the JSON.
    - All keys and string values must use double quotes.
    - confidence must be a numeric value between 0.0 and 1.0.
    - recommendation.decision must be exactly "approve", "revise", or "reject".
    - If information is missing, keep the field brief rather than inventing facts.

    Do not omit any required field. If uncertain, use a short string instead of leaving fields out.

    Return ONLY valid JSON."""
    
    async def _call_ollama(self, prompt: str) -> str:
        """
        Call the Ollama API.
        
        Args:
            prompt: The prompt to send to the model
        
        Returns:
            The response text from the model
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json",  # Request JSON format from Ollama
                "options": {
                    "temperature": 0,
                    "num_predict": 800
                }
            }
            start = time.monotonic()
            logger.info(f"Calling Ollama at {self.chat_endpoint} with model {self.model}")

            response = await client.post(
                self.chat_endpoint,
                json=request_data
            )
            response.raise_for_status()

            elapsed = time.monotonic() - start
            logger.info(f"Ollama responded in {elapsed:.2f} seconds")
            
            result = response.json()
            
            # Extract the message content
            if "message" in result and "content" in result["message"]:
                return result["message"]["content"]
            else:
                raise ValueError(f"Unexpected response format: {result}")
    
    def _parse_response(self, response_text: str) -> AnalysisResult:
        """
        Parse the response text into an AnalysisResult.
        
        Args:
            response_text: The JSON response text from the model
        
        Returns:
            Parsed AnalysisResult object
        
        Raises:
            json.JSONDecodeError: If the response is not valid JSON
            ValidationError: If the JSON doesn't match the AnalysisResult schema
        """
        # Clean the response text
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line if it's ```json or ```
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)
        
        # Parse JSON
        data = json.loads(response_text)

        if "caveats" not in data:
            data["caveats"] = ""
        
        # Validate and return
        return AnalysisResult(**data)


async def analyze_draft_with_llm(
    draft_title: str,
    draft_description: str,
    similar_notices: List[dict],
    cpv: Optional[str] = None,
    ollama_url: Optional[str] = None,
    model: str = "qwen2.5:3b-instruct"
) -> AnalysisResult:
    """
    Convenience function to analyze a draft with LLM.
    
    Args:
        draft_title: Title of the procurement draft
        draft_description: Description of the procurement draft
        similar_notices: List of similar notices from TF-IDF analysis
        cpv: Optional CPV code
        ollama_url: Optional custom Ollama URL
        model: Model name to use (default: llama3.2)
    
    Returns:
        AnalysisResult with the analysis
    """
    client = OllamaClient(base_url=ollama_url, model=model)
    return await client.generate_analysis(
        draft_title=draft_title,
        draft_description=draft_description,
        similar_notices=similar_notices,
        cpv=cpv
    )
