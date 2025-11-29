# app/ocr_pipeline.py
import tempfile, os, asyncio, re, json
from pdf2image import convert_from_path
import requests
from utils import parse_currency_str, dedupe_lineitems, extract_totals_from_text, normalize_item_name
import pytesseract
from PIL import Image
from typing import List, Dict, Any

# Async wrapper for CPU-bound ops
async def run_blocking(fn, *args, **kwargs):
    import asyncio
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

async def download_file(url: str, dest_path: str):
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    return dest_path

async def process_document_url(url: str) -> Dict[str, Any]:
    tmpdir = tempfile.mkdtemp()
    local_path = os.path.join(tmpdir, "document")
    await download_file(url, local_path)
    pages = []
    # If pdf -> convert to images, else try open as image
    if local_path.lower().endswith(".pdf") or local_path.lower().endswith(".PDF"):
        images = await run_blocking(convert_from_path, local_path, 300)
        pages = images
    else:
        img = Image.open(local_path).convert("RGB")
        pages = [img]

    pagewise_line_items = []
    total_items = 0
    all_amounts = []
    combined_text = ""

    for idx, pil_img in enumerate(pages):
        page_no = idx + 1
        # OCR the whole page
        text = pytesseract.image_to_string(pil_img, lang='eng')
        combined_text += "\n" + text

        # Try to extract table-like blocks using simple line heuristics
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        # Heuristic: lines containing a currency/number at end are likely line items
        page_items = []
        for ln in lines:
            # find last currency-looking token
            m = re.search(r'([₹RsEUR$]?\s?\d{1,3}(?:[,\d]*)(?:\.\d{1,2})?)\s*$', ln)
            if m:
                amount_str = m.group(1)
                # try to split name and amount
                name = ln[:m.start(1)].strip(" -:,.")
                amount = parse_currency_str(amount_str)
                if amount is not None:
                    # optionally attempt to parse rate/qty inside name using "x" or "@" heuristics
                    item = {
                        "item_name": normalize_item_name(name if name else "UNKNOWN"),
                        "item_amount": float(round(amount,2)),
                        "item_rate": None,
                        "item_quantity": None
                    }
                    page_items.append(item)
                    all_amounts.append(amount)
        # dedupe page_items (simple normalized-name based)
        page_items = dedupe_lineitems(page_items)
        total_items += len(page_items)
        page_obj = {"page_no": str(page_no), "page_type": "Bill Detail", "bill_items": page_items}
        pagewise_line_items.append(page_obj)

    # totals reconciliation: look for explicit subtotal/final total strings in combined text
    totals = extract_totals_from_text(combined_text)
    reconciled_amount = totals.get("final_total") if totals.get("final_total") is not None else round(sum(all_amounts),2)

    # token usage placeholder (0 unless you call LLM)
    token_usage = {"total_tokens": 0, "input_tokens": 0, "output_tokens": 0}

    return {
        "pagewise_line_items": pagewise_line_items,
        "total_item_count": total_items,
        "reconciled_amount": float(round(reconciled_amount,2)),
        "token_usage": token_usage
    }
