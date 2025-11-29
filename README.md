# Bajaj Health Datathon — Bill Extraction (Your Name)

## Overview
This repo contains an API that accepts a document URL (image/PDF) and returns page-wise line items, counts and reconciled total as per the datathon API spec.

## How to run (local)
Prereqs:
- Python 3.9+
- Tesseract OCR installed (apt: `sudo apt-get install tesseract-ocr`)
- Poppler installed (`sudo apt-get install poppler-utils`)
- Java (for tabula/camelot) if using table extraction for PDFs

## Install:
```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Run:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Test (example curl):
```bash
curl -X POST "http://localhost:8080/extract-bill-data" -H "Content-Type: application/json" -d '{"document":"<DOCUMENT_URL>"}'
```
## Deployment

You can deploy to Render / Railway / Heroku / DigitalOcean / AWS Elastic Beanstalk / Azure App Service. Provide the resulting HTTPS webhook URL to the datathon submission portal.

## Files

1. main.py: FastAPI endpoint

2. ocr_pipeline.py: pipeline orchestration

3. utils.py: parsing helpers

4. Dockerfile: for containerization

5. pitch_deck.pdf: 2-page pitch deck

6. postman_collection.json: import to test

## Notes & Differentiators

1. Preprocessing: image deskew, contrast stretch, adaptive thresholding used (add if needed).

2. Deduplication heuristic: name+amount normalized matching.

3. Fraud detection cues: inconsistent font sizes, heavy erasures, painters/whiteout detection — method described in Pitch deck.

4. Optional improvements: use LayoutLMv3 / Donut / Google Document AI for higher accuracy (instructions below).
