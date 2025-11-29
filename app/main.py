# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import requests
import uvicorn
import os
from ocr_pipeline import process_document_url
# from utils import compute_reconciled_amount, format_response_with_tokens

app = FastAPI(title="Bajaj Health Datathon - Bill Extractor")

class ExtractRequest(BaseModel):
    document: str

@app.post("/extract-bill-data")
async def extract_bill_data(req: ExtractRequest):
    doc_url = req.document
    if not doc_url.startswith("http"):
        raise HTTPException(status_code=400, detail="document must be a valid URL")
    try:
        # process_document_url returns:
        # { "pagewise_line_items": [...], "total_item_count": int, "reconciled_amount": float, "token_usage": {...} }
        result = await process_document_url(doc_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Wrap in required response format and include token usage
    response = {
        "is_success": True,
        "token_usage": result.get("token_usage", {"total_tokens":0,"input_tokens":0,"output_tokens":0}),
        "data": {
            "pagewise_line_items": result["pagewise_line_items"],
            "total_item_count": result["total_item_count"],
            "reconciled_amount": result["reconciled_amount"]
        }
    }
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
