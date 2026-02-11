# LLM Service Documentation

## Overview

The LLM service (`backend/app/services/llm.py`) provides integration with Ollama for AI-powered analysis of procurement drafts. It generates comprehensive analysis reports including similar notice ranking, qualitative assessment, and recommendations.

## Features

- **Ollama Integration**: Calls Ollama API at configurable endpoint
- **Structured Output**: Uses Pydantic schemas for type-safe, validated responses
- **Retry Logic**: Automatically retries with stricter prompts if JSON parsing fails
- **JSON-Only Output**: Forces the model to output valid JSON
- **Configurable**: URL, model, and timeout can be configured

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```bash
OLLAMA_API_URL=http://localhost:11434
```

3. Ensure Ollama is running on the configured endpoint.

## Usage

### Basic Usage

```python
from app.services.llm import analyze_draft_with_llm

# Analyze a draft with similar notices
result = await analyze_draft_with_llm(
    draft_title="Construction of Public Library",
    draft_description="Seeking contractors for library construction...",
    similar_notices=[
        {
            "notice_id": "N001",
            "title": "School Building Construction",
            "buyer": "City Council",
            "cpv_codes": ["45000000"],
            "published_date": "2024-01-15",
            "similarity_score": 0.92,
            "description_excerpt": "Construction project..."
        }
    ],
    cpv="45214200"
)

print(f"Decision: {result.recommendation.decision}")
print(f"Confidence: {result.confidence}")
```

### Using OllamaClient Directly

```python
from app.services.llm import OllamaClient

# Create client with custom configuration
client = OllamaClient(
    base_url="http://custom-ollama:11434",
    model="llama3.2",
    timeout=180.0
)

# Generate analysis
result = await client.generate_analysis(
    draft_title="...",
    draft_description="...",
    similar_notices=[...],
    cpv="..."
)
```

## Data Structures

### AnalysisResult

Main output schema containing the complete analysis:

```python
{
    "similar_notices_ranked": [
        {
            "notice_id": "string",
            "score": 0.0-1.0,
            "title": "string or null",
            "buyer": "string or null",
            "cpv_codes": ["string"] or null,
            "published_date": "string or null"
        }
    ],
    "overlap_summary": "string",
    "qualitative_analysis": {
        "risk_management": "string",
        "sustainability_social_values": "string",
        "transparency_fair_competition": "string",
        "innovation_forward_thinking": "string"
    },
    "recommendation": {
        "decision": "approve|revise|reject",
        "rationale": "string"
    },
    "confidence": 0.0-1.0,
    "caveats": "string"
}
```

## Configuration

### Environment Variables

- `OLLAMA_API_URL`: Base URL for Ollama API (default: `http://localhost:11434`)

### Client Configuration

```python
OllamaClient(
    base_url: Optional[str] = None,  # Override env var
    model: str = "llama3.2",         # Model to use
    timeout: float = 120.0           # Timeout in seconds
)
```

### Constants

Available in `OllamaClient` class:
- `MAX_DESCRIPTION_LENGTH = 200`: Maximum description length in context
- `DEFAULT_TIMEOUT = 120.0`: Default timeout for API calls

## Error Handling

The service handles several error scenarios:

1. **JSON Parse Errors**: Automatically retries with stricter prompt
2. **Validation Errors**: Returns Pydantic ValidationError with details
3. **HTTP Errors**: Raises httpx.HTTPError for network/API issues
4. **Timeout**: Raises timeout exception after configured duration

Example error handling:

```python
try:
    result = await analyze_draft_with_llm(...)
except httpx.HTTPError as e:
    print(f"API call failed: {e}")
except ValidationError as e:
    print(f"Response validation failed: {e}")
except json.JSONDecodeError as e:
    print(f"JSON parsing failed: {e}")
```

## Integration with FastAPI

Example endpoint in `main.py`:

```python
from fastapi import FastAPI, HTTPException
from app.services.llm import analyze_draft_with_llm, AnalysisResult

@app.post("/drafts/{draft_id}/analyze-with-llm", response_model=AnalysisResult)
async def analyze_draft_with_llm_endpoint(draft_id: int):
    """Analyze a draft using LLM after TF-IDF similarity search."""
    if draft_id not in drafts_db:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    if draft_id not in analysis_db:
        raise HTTPException(
            status_code=400,
            detail="Please run TF-IDF analysis first"
        )
    
    draft = drafts_db[draft_id]
    analysis = analysis_db[draft_id]
    
    try:
        llm_result = await analyze_draft_with_llm(
            draft_title=draft['title'],
            draft_description=draft['description'],
            similar_notices=analysis['top_notices'],
            cpv=draft.get('cpv')
        )
        
        return llm_result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM analysis failed: {str(e)}"
        )
```

## Testing

The service includes comprehensive tests for:
- Pydantic schema validation
- JSON parsing (clean and markdown-wrapped)
- Similar notice formatting
- Prompt creation

Run tests:
```bash
PYTHONPATH=/path/to/backend python test_llm_service.py
```

## Logging

The service uses Python's logging module. Configure logging in your application:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

The service will log:
- Warning on first parse failure (before retry)
- Any other relevant operational information

## Requirements

- Python 3.8+
- httpx >= 0.26.0
- pydantic >= 2.5.3
- Ollama server running and accessible
