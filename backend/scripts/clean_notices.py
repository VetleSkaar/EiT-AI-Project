#!/usr/bin/env python3
"""
Clean and validate a small, manually curated Doffin notice dataset for a demo.

Input supports:
- JSON array file: data/notices.json
- JSONL file:      data/notices.jsonl

Output:
- data/notices.cleaned.json (JSON array)

What it does:
- Deduplicates by notice_id
- Normalizes cpv_codes to list of 8-digit strings
- Ensures required fields exist (fills missing with defaults)
- Trims description_excerpt to max length (default 1200 chars)
- Creates description_excerpt from description_raw if missing
- Normalizes dates to YYYY-MM-DD where possible
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CPV_RE = re.compile(r"\b(\d{8})\b")

DEFAULT_EXCERPT_MAX = 1200
DEFAULT_EXCERPT_MIN = 200


def load_records(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if path.suffix.lower() == ".jsonl":
        records = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
        return records

    # Assume JSON array
    data = json.loads(text)
    if isinstance(data, list):
        return data
    raise ValueError(f"Expected JSON array in {path}, got {type(data)}")


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_notice_id(n: Dict[str, Any]) -> str:
    notice_id = str(n.get("notice_id") or "").strip()
    if notice_id:
        return notice_id

    url = str(n.get("url") or "").strip()
    m = re.search(r"/notices/([^/?#]+)", url)
    if m:
        return m.group(1)

    return ""


def normalize_cpv_codes(n: Dict[str, Any]) -> List[str]:
    cpv = n.get("cpv_codes")

    codes: List[str] = []
    if isinstance(cpv, list):
        for x in cpv:
            if x is None:
                continue
            s = str(x).strip()
            found = CPV_RE.findall(s)
            if found:
                codes.extend(found)
            elif s.isdigit():
                codes.append(s)
    elif isinstance(cpv, str):
        codes = CPV_RE.findall(cpv)
        if not codes and cpv.strip().isdigit():
            codes = [cpv.strip()]

    # Normalize to 8 digits only
    codes = [c for c in codes if re.fullmatch(r"\d{8}", c)]
    codes = sorted(set(codes))
    return codes


def normalize_date(s: Any) -> str:
    if not s:
        return ""
    t = str(s).strip()
    if DATE_RE.match(t):
        return t

    # Accept common variants like "2026.02.10" or "10.02.2026"
    m1 = re.match(r"^(\d{4})[./](\d{2})[./](\d{2})$", t)
    if m1:
        return f"{m1.group(1)}-{m1.group(2)}-{m1.group(3)}"

    m2 = re.match(r"^(\d{2})[./](\d{2})[./](\d{4})$", t)
    if m2:
        return f"{m2.group(3)}-{m2.group(2)}-{m2.group(1)}"

    # Otherwise keep empty (avoid lying)
    return ""


def clean_whitespace(text: str) -> str:
    # Normalize whitespace without destroying paragraphs too much
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse repeated spaces
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def make_excerpt(description_raw: str, max_len: int) -> str:
    raw = clean_whitespace(description_raw)
    if not raw:
        return ""
    if len(raw) <= max_len:
        return raw
    # Cut at word boundary
    cut = raw[:max_len]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.strip() + "…"


def normalize_estimated_value(n: Dict[str, Any]) -> Optional[float]:
    v = n.get("estimated_value_nok")
    if v is None or v == "":
        # allow alternative keys
        v = n.get("estimated_value") or n.get("value_nok")

    if v is None or v == "":
        return None

    if isinstance(v, (int, float)):
        return float(v)

    s = str(v).strip()
    # remove spaces, currency markers, etc.
    s = s.replace("NOK", "").replace("kr", "").replace(" ", "")
    s = s.replace(",", ".")
    # keep digits and dot
    s = re.sub(r"[^0-9.]", "", s)
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_record(n: Dict[str, Any], excerpt_max: int) -> Tuple[Dict[str, Any], List[str]]:
    warnings: List[str] = []

    notice_id = normalize_notice_id(n)
    if not notice_id:
        warnings.append("missing notice_id (and could not derive from url)")

    url = str(n.get("url") or "").strip()

    title = clean_whitespace(str(n.get("title") or ""))
    buyer = clean_whitespace(str(n.get("buyer") or n.get("buyer_name") or ""))

    cpv_codes = normalize_cpv_codes(n)
    if not cpv_codes:
        warnings.append("missing cpv_codes")

    published_date = normalize_date(n.get("published_date") or n.get("published_at"))
    deadline = normalize_date(n.get("deadline") or n.get("deadline_at"))

    procedure = clean_whitespace(str(n.get("procedure") or ""))
    duration = clean_whitespace(str(n.get("duration") or n.get("contract_duration") or ""))

    description_raw = clean_whitespace(str(n.get("description_raw") or n.get("description") or ""))
    description_excerpt = clean_whitespace(str(n.get("description_excerpt") or ""))

    if not description_excerpt:
        description_excerpt = make_excerpt(description_raw, excerpt_max)

    if not description_excerpt:
        warnings.append("missing description_excerpt/description_raw")

    if len(description_excerpt) < DEFAULT_EXCERPT_MIN and description_raw:
        # not a hard error; just a hint that TF-IDF may be weak
        warnings.append(f"very short description_excerpt ({len(description_excerpt)} chars)")

    estimated_value_nok = normalize_estimated_value(n)

    cleaned: Dict[str, Any] = {
        "notice_id": notice_id,
        "url": url,
        "title": title,
        "buyer": buyer,
        "cpv_codes": cpv_codes,
        "published_date": published_date,
        "deadline": deadline,
        "estimated_value_nok": estimated_value_nok,
        "procedure": procedure,
        "duration": duration,
        "description_raw": description_raw,
        "description_excerpt": description_excerpt,
    }

    # Optional: keep any tags if present
    tags = n.get("tags")
    if isinstance(tags, list):
        cleaned["tags"] = sorted(set(str(t).strip() for t in tags if str(t).strip()))

    return cleaned, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="Input notices file (.json or .jsonl)")
    ap.add_argument("--out", dest="out_path", required=True, help="Output cleaned notices file (.json)")
    ap.add_argument("--excerpt-max", dest="excerpt_max", type=int, default=DEFAULT_EXCERPT_MAX)
    args = ap.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    records = load_records(in_path)

    seen: Set[str] = set()
    cleaned_records: List[Dict[str, Any]] = []
    all_warnings: List[Dict[str, Any]] = []

    for i, r in enumerate(records, 1):
        if not isinstance(r, dict):
            all_warnings.append({"row": i, "notice_id": "", "warnings": [f"record not an object: {type(r)}"]})
            continue

        cleaned, warnings = clean_record(r, excerpt_max=args.excerpt_max)
        nid = cleaned.get("notice_id", "") or ""

        if nid and nid in seen:
            all_warnings.append({"row": i, "notice_id": nid, "warnings": ["duplicate notice_id (skipped)"]})
            continue
        if nid:
            seen.add(nid)

        cleaned_records.append(cleaned)
        if warnings:
            all_warnings.append({"row": i, "notice_id": nid, "warnings": warnings})

    dump_json(out_path, cleaned_records)

    # Print a readable summary to stdout (useful in CI / demo prep)
    print(f"Loaded: {len(records)} records")
    print(f"Written: {len(cleaned_records)} cleaned records -> {out_path}")
    if all_warnings:
        print("\nWarnings:")
        for w in all_warnings[:50]:
            nid = w["notice_id"] or "?"
            print(f"- row {w['row']} notice {nid}: {', '.join(w['warnings'])}")
        if len(all_warnings) > 50:
            print(f"... ({len(all_warnings) - 50} more)")


if __name__ == "__main__":
    main()
