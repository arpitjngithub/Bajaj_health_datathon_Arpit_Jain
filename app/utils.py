# app/utils.py
import re
from typing import List, Dict, Any
import unicodedata

# -----------------------------------------
# Basic Parsing Utilities
# -----------------------------------------

def parse_currency_str(s):
    if s is None: 
        return None
    s = s.strip()
    s = s.replace("Rs.", "").replace("Rs", "").replace("₹", "").replace(",", "")
    s = re.sub(r'[^\d\.\-]', '', s)
    try:
        return float(s)
    except:
        return None


def normalize_item_name(name):
    if not name:
        return ""
    # basic normalize: remove excessive spaces, control chars
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def dedupe_lineitems(items: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    """
    Simple dedupe by (normalized item_name + item_amount).
    Prevents double counting.
    """
    seen = {}
    out = []
    for it in items:
        key = (
            it.get("item_name","").lower(), 
            round(float(it.get("item_amount",0)), 2)
        )
        if key not in seen:
            seen[key] = True
            out.append(it)
    return out


def extract_totals_from_text(text: str) -> dict:
    """
    Extract subtotal / final total keywords from OCR text.
    """
    patterns = {
        "final_total": r'(grand total|final total|net payable|total amount|amount payable|net amount)\s*[:\-\s]*([₹Rs$]?\s?\d[\d,\.]*)',
        "sub_total": r'(sub[-\s]*total|subtotal)\s*[:\-\s]*([₹Rs$]?\s?\d[\d,\.]*)'
    }
    res = {}
    for k, pat in patterns.items():
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            val = m.group(2)
            try:
                res[k] = parse_currency_str(val)
            except:
                res[k] = None
    return res


# -----------------------------------------
# Functions required by main.py
# -----------------------------------------

def compute_reconciled_amount(line_items: List[Dict[str,Any]]):
    """
    Compute the final total by summing item_amount.
    Used as a fallback reconciliation if pipeline does not provide explicit totals.
    """
    total = 0.0
    for it in line_items:
        try:
            total += float(it.get("item_amount", 0))
        except:
            pass
    return round(total, 2)


def format_response_with_tokens(response: Dict[str,Any], token_usage: Dict[str,int] = None):
    """
    Wraps the API response with token usage.
    
    This matches the format expected by the Datathon:
      {
        "is_success": true,
        "token_usage": {...},
        "data": {...}
      }
    """
    if token_usage is None:
        token_usage = {"total_tokens": 0, "input_tokens": 0, "output_tokens": 0}

    response["token_usage"] = token_usage
    return response
