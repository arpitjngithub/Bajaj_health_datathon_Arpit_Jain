# Bajaj Health Datathon — Bill Extraction (Your Name)

## Overview
This repo contains an API that accepts a document URL (image/PDF) and returns page-wise line items, counts and reconciled total as per the datathon API spec.

## How to run (local)
Prereqs:
- Python 3.9+
- Tesseract OCR installed (apt: `sudo apt-get install tesseract-ocr`)
- Poppler installed (`sudo apt-get install poppler-utils`)
- Java (for tabula/camelot) if using table extraction for PDFs

Install:
```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
