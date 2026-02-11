# Data Directory

This directory contains the notices data used for TF-IDF analysis.

## notices.cleaned.json

This file contains procurement notices in JSON format. Each notice should have the following structure:

```json
{
  "id": "unique_notice_id",
  "title": "Notice title",
  "description": "Detailed description of the procurement notice",
  "cpv": "CPV code (Common Procurement Vocabulary)"
}
```

The file is loaded on application startup, and a TF-IDF matrix is built from the combined title and description of all notices. This matrix is then used to find similar notices when analyzing drafts.

## Sample Data

The included `notices.cleaned.json` file contains 10 sample procurement notices for testing purposes. Replace this file with your actual procurement data in production.
