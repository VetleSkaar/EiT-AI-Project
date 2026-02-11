# Data Directory

This directory contains the notices data used for TF-IDF analysis.

## notices.cleaned.json

This file contains procurement notices in JSON format. Each notice should have the following structure:

```json
{
  "notice_id": "unique_notice_id",
  "url": "URL to the notice",
  "title": "Notice title",
  "buyer": "Name of the buying organization",
  "cpv_codes": ["CPV code 1", "CPV code 2"],
  "published_date": "Publication date (YYYY-MM-DD)",
  "deadline": "Deadline date (YYYY-MM-DD)",
  "estimated_value_nok": 1000000,
  "procedure": "Procurement procedure type",
  "duration": "Contract duration",
  "description_raw": "Full detailed description of the procurement notice",
  "description_excerpt": "Shorter, cleaned description for similarity analysis"
}
```

**Field Descriptions:**
- `notice_id`: Unique identifier for the notice
- `url`: Link to the full notice details
- `title`: Brief title of the procurement
- `buyer`: Organization issuing the procurement
- `cpv_codes`: Array of Common Procurement Vocabulary codes
- `published_date`: When the notice was published
- `deadline`: Submission deadline for bids
- `estimated_value_nok`: Estimated contract value in Norwegian Kroner (optional)
- `procedure`: Type of procurement procedure (e.g., "Open procedure", "Restricted procedure")
- `duration`: Expected contract duration
- `description_raw`: Complete, unprocessed description text
- `description_excerpt`: Cleaned and shortened description optimized for TF-IDF similarity analysis

## TF-IDF Analysis

The file is loaded on application startup, and a TF-IDF matrix is built from the combined `title` and `description_excerpt` of all notices. The `description_excerpt` field is specifically designed to be a concise, cleaned version that works well for similarity matching, while `description_raw` preserves the full original text for reference.

## Sample Data

The included `notices.cleaned.json` file contains 10 sample procurement notices for testing purposes. Replace this file with your actual procurement data in production.
