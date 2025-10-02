#!/usr/bin/env python3
import os
import json
import argparse
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Any

# ========= Stable, site-wide defaults (used if a record omits a field) =========
VIDEO_DEFAULTS = {
    "layout": "video",
    "video_host": "youtube",
    "publisher_name": "CertificationExams.guru",
    "publisher_logo": "/assets/images/logo-512.png",
    "in_language": "en",
    "is_accessible_for_free": True,
}

# Default input and output
DEFAULT_INPUT = "articles.json"
DEFAULT_OUTDIR = "."

# ========= Utilities =========
def slugify(text: str) -> str:
    """
    Make a kebab-case slug from title:
    - normalize unicode to ASCII
    - lower-case
    - keep alphanumerics and spaces
    - replace whitespace with single dashes
    - collapse multiple dashes and strip dash edges
    """
    if not text:
        return "untitled"
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "untitled"

def yaml_bool(val: bool) -> str:
    return "true" if val else "false"

def yaml_quote(s: Any) -> str:
    """
    Simple YAML double-quote escaper for title/description/strings.
    """
    if s is None:
        return '""'
    s = str(s)
    s = s.replace('"', '\\"')
    return f'"{s}"'

def yaml_list(items: List[str], indent: int = 0) -> str:
    pad = " " * indent
    lines = []
    for it in items or []:
        safe = str(it).replace("\n", " ").strip()
        lines.append(f"{pad}- {safe}")
    return "\n".join(lines)

def ensure_unique_path(base_dir: Path, slug: str) -> Path:
    """
    Ensure we do not overwrite accidentally: add -2, -3, ... if needed.
    """
    p = base_dir / f"{slug}.html"
    if not p.exists():
        return p
    i = 2
    while True:
        cand = base_dir / f"{slug}-{i}.html"
        if not cand.exists():
            return cand
        i += 1

def pick(meta: Dict[str, Any], key: str, default: Any = "") -> Any:
    """
    Pick a key from meta with a sensible fallback.
    Treat empty strings as missing.
    """
    v = meta.get(key)
    if isinstance(v, str):
        v = v.strip()
    return v if v not in (None, "") else default

# --- light normalizers (accept good values as-is) ---
ISO_OFFSET_RE = re.compile(r"[+-]\d{2}:\d{2}$")

def normalize_upload_date(s: str) -> str:
    """
    Return ISO-8601 with explicit offset when possible.
    Accepts '...Z', '...+00:00', or naive 'YYYY-MM-DDTHH:MM:SS' and makes it UTC.
    """
    if not s:
        return ""
    s = s.strip()
    if s.endswith("Z"):
        return s[:-1] + "+00:00"
    if ISO_OFFSET_RE.search(s):
        return s
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", s):
        return s + "+00:00"
    return s

def looks_like_iso_duration(s: str) -> bool:
    # Very loose check: starts with PT and contains at least one time component
    return isinstance(s, str) and s.startswith("PT") and any(ch in s for ch in "HMS")

def normalize_duration(s: str) -> str:
    """
    Leave correct ISO-8601 durations alone (e.g., PT34M04S).
    If not recognized, just return as-is (your generator should have formatted it).
    """
    if looks_like_iso_duration(s):
        return s
    return s or ""

# ========= Page building =========
def build_front_matter(record: Dict[str, Any]) -> str:
    """
    Create YAML front matter block for Jekyll.
    - layout and stable site fields from VIDEO_DEFAULTS (overridden by record if present)
    - title/description/tags from record
    - video fields read from the record generated earlier
    """
    title = (record.get("title") or "").strip()
    desc = (record.get("description") or "").strip()
    tags = record.get("tags", []) or []

    # Read per-record video metadata (fallback to defaults as needed)
    video_host = pick(record, "video_host", VIDEO_DEFAULTS["video_host"])
    video_id = pick(record, "video_id")
    upload_date = "2025-10-01T11:11:11+11:11"
    duration = normalize_duration(pick(record, "duration"))
    thumbnail_url = pick(record, "thumbnail_url")
    content_url = pick(record, "content_url")
    embed_url = pick(record, "embed_url")

    publisher_name = pick(record, "publisher_name", VIDEO_DEFAULTS["publisher_name"])
    publisher_logo = pick(record, "publisher_logo", VIDEO_DEFAULTS["publisher_logo"])
    in_language = pick(record, "in_language", VIDEO_DEFAULTS["in_language"])
    # allow record override but default to site-wide boolean
    is_free = record.get("is_accessible_for_free")
    if is_free is None:
        is_free = VIDEO_DEFAULTS["is_accessible_for_free"]
    is_free = bool(is_free)

    fm = ["---"]
    fm.append(f'layout: {VIDEO_DEFAULTS["layout"]}')
    fm.append(f'title: {yaml_quote(title)}')
    fm.append(f'description: {yaml_quote(desc)}')

    # Video meta
    fm.append(f'video_host: {yaml_quote(video_host)}')
    fm.append(f'video_id: {yaml_quote(video_id)}')
    fm.append(f'upload_date: {yaml_quote(upload_date)}')
    fm.append(f'duration: {yaml_quote(duration)}')
    fm.append(f'thumbnail_url: {yaml_quote(thumbnail_url)}')
    fm.append(f'content_url: {yaml_quote(content_url)}')
    fm.append(f'embed_url: {yaml_quote(embed_url)}')

    # Publisher / language / access
    fm.append(f'publisher_name: {yaml_quote(publisher_name)}')
    fm.append(f'publisher_logo: {yaml_quote(publisher_logo)}')
    fm.append(f'in_language: {yaml_quote(in_language)}')
    fm.append(f'is_accessible_for_free: {yaml_bool(is_free)}')

    fm.append("tags:")
    fm.append(yaml_list(tags, indent=2))
    fm.append("---")
    return "\n".join(fm)

def build_body_html(record: Dict[str, Any]) -> str:
    """
    Wrap the JSON 'body' HTML in your provided section and card layout.
    """
    body_html = (record.get("body") or "").strip()
    return f"""<section class="py-6" id="exam-overview" style="padding-top:5px; padding-bottom:35px;">
  <div class="container mt-4 mb-14">
    <div class="row g-4 mt-4">
      <!-- Left card: Certification Info -->
      <div class="col-12">
        <div class="compare-card border-accent-subtle h-100">
          <div class="card-body">
{body_html}
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

def write_page(outdir: Path, record: Dict[str, Any]) -> Path:
    title = record.get("title", "Untitled")
    slug = slugify(title)
    target = ensure_unique_path(outdir, slug)

    front_matter = build_front_matter(record)
    page_html = build_body_html(record)

    target.write_text(front_matter + "\n" + page_html, encoding="utf-8")
    return target

# ========= Main =========
def load_input(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise ValueError("Input JSON must be an array of objects or a single object.")
    return data

def main():
    ap = argparse.ArgumentParser(description="Create Jekyll HTML pages from SEO JSON (reads per-record YouTube metadata).")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (default: articles.json)")
    ap.add_argument("--outdir", "-o", default=DEFAULT_OUTDIR, help="Output directory (default: .)")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    records = load_input(in_path)
    if not records:
        print("No records found in input JSON.")
        return

    written = []
    for rec in records:
        try:
            p = write_page(out_dir, rec)
            written.append(p.name)
            print(f"Wrote: {p}")
        except Exception as e:
            print(f"Error writing page for title='{rec.get('title','')}' -> {e}")

    print(f"Done. Pages written: {len(written)} to {out_dir.resolve()}")

if __name__ == "__main__":
    main()
