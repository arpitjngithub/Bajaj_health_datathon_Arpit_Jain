# app/utils.py
import re
from typing import List, Dict, Any
import unicodedata

def parse_currency_str(s):
    if s is None: return None
    s = s.strip()
    s = s.replace("Rs.", "").replace("Rs", "").replace("₹", "").replace(",", "")
    s = re.sub(r'[^\d\.\-]', '', s)
    try:
        return float(s)
    except:
        return None

def normalize_item_name(name):
    if not name: return ""
    # basic normalize: remove excessive spaces, control chars
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def dedupe_lineitems(items: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    # Simple dedupe by normalized name and amount
    seen = {}
    out = []
    for it in items:
        key = (it.get("item_name","").lower(), round(float(it.get("item_amount",0)),2))
        if key not in seen:
            seen[key] = True
            out.append(it)
    return out

def extract_totals_from_text(text: str) -> dict:
    # look for keywords like TOTAL, GRAND TOTAL, SUB TOTAL, NET AMOUNT etc.
    patterns = {
        "final_total": r'(grand total|final total|net payable|total amount|amount payable|net amount)\s*[:\-\s]*([₹Rs$]?\s?\d[\d,\.]*)',
        "sub_total": r'(sub[-\s]*total|subtotal)\s*[:\-\s]*([₹Rs$]?\s?\d[\d,\.]*)'
    }
    res = {}
    lower = text.lower()
    for k,pat in patterns.items():
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            val = m.group(2)
            try:
                valn = parse_currency_str(val)
                res[k] = valn
            except:
                res[k] = None
    return res
