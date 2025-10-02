#!/usr/bin/env python3
import os
import json
import argparse
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Any

# ========= Editable video config (applies to every page) =========
VIDEO_CONFIG = {
    "layout": "video",
    "video_host": "youtube",
    "video_id": "MaqVvXv6zrU",
    "upload_date": "2025-10-01T00:00:01+00:00",
    "duration": "PT34M04S",
    "thumbnail_url": "https://i.ytimg.com/vi/MaqVvXv6zrU/maxresdefault.jpg",
    "content_url": "https://youtu.be/MaqVvXv6zrU?si=VOAp6ZlsZl8RS13b",
    "embed_url": "https://www.youtube.com/embed/MaqVvXv6zrU",
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
    # Normalize and strip non-ascii
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # Replace anything not alnum or space with a space
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Collapse whitespace -> single dash
    text = re.sub(r"\s+", "-", text)
    # Collapse multiple dashes and trim
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "untitled"

def yaml_bool(val: bool) -> str:
    return "true" if val else "false"

def yaml_quote(s: str) -> str:
    """
    Simple YAML double-quote escaper for title/description.
    """
    if s is None:
        return '""'
    s = s.replace('"', '\\"')
    return f'"{s}"'

def yaml_list(items: List[str], indent: int = 0) -> str:
    pad = " " * indent
    lines = []
    for it in items or []:
        safe = it.replace("\n", " ").strip()
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

def build_front_matter(record: Dict[str, Any]) -> str:
    """
    Create YAML front matter block for Jekyll.
    - layout from VIDEO_CONFIG
    - title/description from record
    - video fields from VIDEO_CONFIG
    - tags from record.tags (YAML list)
    """
    title = record.get("title", "").strip()
    desc = record.get("description", "").strip()
    tags = record.get("tags", []) or []

    # Front matter lines
    fm = ["---"]
    fm.append(f'layout: {VIDEO_CONFIG["layout"]}')
    fm.append(f'title: {yaml_quote(title)}')
    fm.append(f'description: {yaml_quote(desc)}')
    fm.append(f'video_host: {yaml_quote(VIDEO_CONFIG["video_host"])}')
    fm.append(f'video_id: {yaml_quote(VIDEO_CONFIG["video_id"])}')
    fm.append(f'upload_date: {yaml_quote(VIDEO_CONFIG["upload_date"])}')
    fm.append(f'duration: {yaml_quote(VIDEO_CONFIG["duration"])}')
    fm.append(f'thumbnail_url: {yaml_quote(VIDEO_CONFIG["thumbnail_url"])}')
    fm.append(f'content_url: {yaml_quote(VIDEO_CONFIG["content_url"])}')
    fm.append(f'embed_url: {yaml_quote(VIDEO_CONFIG["embed_url"])}')
    fm.append(f'publisher_name: {yaml_quote(VIDEO_CONFIG["publisher_name"])}')
    fm.append(f'publisher_logo: {yaml_quote(VIDEO_CONFIG["publisher_logo"])}')
    fm.append(f'in_language: {yaml_quote(VIDEO_CONFIG["in_language"])}')
    fm.append(f'is_accessible_for_free: {yaml_bool(VIDEO_CONFIG["is_accessible_for_free"])}')
    fm.append("tags:")
    fm.append(yaml_list(tags, indent=2))
    fm.append("---")
    return "\n".join(fm)

def build_body_html(record: Dict[str, Any]) -> str:
    """
    Wrap the JSON 'body' HTML in your provided section and card layout.
    The record['heading'] is not required here, since the design uses only 'body' in the card.
    """
    body_html = record.get("body", "").strip()
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
        # allow single-object JSON
        data = [data]
    if not isinstance(data, list):
        raise ValueError("Input JSON must be an array of objects or a single object.")
    return data

def main():
    ap = argparse.ArgumentParser(description="Create Jekyll HTML pages from SEO JSON.")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (default: articles.json)")
    ap.add_argument("--outdir", "-o", default=DEFAULT_OUTDIR, help="Output directory (default: generated)")
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
