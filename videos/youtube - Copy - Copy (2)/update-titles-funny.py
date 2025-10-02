#!/usr/bin/env python3
"""
Batch-generate SEO title, heading, and BODY using OpenAI Batch + /v1/chat/completions
with Structured Outputs (JSON Schema), extensive diagnostics, and resume support.

Outputs:
  - openai-batch-input.jsonl     (requests)
  - openai-batch-id.txt          (last batch id)
  - openai-batch-output.jsonl    (raw output)
  - openai-batch-errors.jsonl    (raw errors)
  - articles-funny.json          (merged results)
  - errors_report.txt / .json    (error summaries)
  - batch_seo_titles.log         (logs)

Prereqs:
  pip install openai==1.*
  export OPENAI_API_KEY=...
"""

import argparse
import html
import json
import logging
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from openai import OpenAI
from openai._exceptions import OpenAIError

# ---------- Defaults / constants ----------
MODEL = "gpt-5-mini"
TEMPERATURE = 1.0
DEFAULT_POLL_SECONDS = 100
COMPLETION_WINDOW = "24h"

BATCH_INPUT_JSONL = "openai-batch-input.jsonl"
BATCH_ID_FILE = "openai-batch-id.txt"
BATCH_OUTPUT_JSONL = "openai-batch-output.jsonl"
BATCH_ERROR_JSONL = "openai-batch-errors.jsonl"

OUTPUT_FILE = "articles-funny.json"
LOG_FILE = "batch_seo_titles.log"

ERROR_REPORT_TXT = "errors_report.txt"
ERROR_REPORT_JSON = "errors_report.json"

# ---------- Logging ----------
logger = logging.getLogger("batch_seo_titles")
logger.setLevel(logging.INFO)
_fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(_fmt)
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(_fmt)
logger.addHandler(ch)
logger.addHandler(fh)

# ---------- Helpers ----------
def strip_html_to_words(html_text: str, max_words: int = 300) -> str:
    if not html_text:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(html_text))
    words = re.findall(r"\S+", text)
    return " ".join(words[:max_words])

def make_prompt(article: Dict[str, Any]) -> str:
    title = (article.get("title") or "").strip()
    tags = article.get("tags") or []
    body_300 = strip_html_to_words(article.get("body") or "", 300)
    prompt = f"""
You are an irreverent but accurate SEO editor and humor writer who does not use em-dashes, colons or semi-colons in your code, and you don't have any ChatGPT give-aways. Your style guidelines:

Tone:
- Funny, sarcastic, and a pinch of dark humor (PG-13; punch up, not down).
- Witty, eye-rolly, lightly self-aware. Never cruel or discriminatory.

What to produce (STRICTLY via the JSON schema):
1) "new_title": A DIFFERENT, SEO-optimized, clickworthy title.
   - Keep natural sentence casing.
   - Avoid keyword stuffing.
   - Prefer ~55–65 characters when it fits naturally.
   - DO NOT use em-dashes, colons, or semicolons. Use normal sentences instead.
   - Must be materially different from the original title (no trivial paraphrase).

2) "new_heading": A DISTINCT H1-style heading (not a paraphrase of your title).
   - Aim ~60–80 characters naturally.
   - Target secondary/long-tail variants.
   - DO NOT use em-dashes, colons, or semicolons.

3) "new_body": A fully rewritten HTML article body in the same topical domain as the original,
   but with humorous, sarcastic narration and light dark humor.
   - Preserve technical accuracy and core takeaways.
   - Reorganize the flow; change sentence structures; add witty asides.
   - Include headings (<h2>, <h3>), short paragraphs, and lists where helpful.
   - Keep facts correct; do not invent APIs or steps.
   - No em-dashes, colons, or semicolons in headings or title; normal punctuation elsewhere is fine.
   - Length: roughly comparable to a typical blog post section (at least several paragraphs).
   - Keep HTML valid.

General rules:
- American English.
- Absolutely do NOT repeat or trivially rephrase the original title.
- Make it look original to avoid near-duplicate detection.
- Naturally weave in primary and secondary keywords derived from the topic and tags.
- Return ONLY JSON that matches the provided schema.

Original context:
- Original Title: {title}
- Tags: {", ".join(tags)}
- First 300 words from the body (HTML stripped):
{body_300}
"""
    return prompt.strip()

def build_schema(loose: bool) -> Dict[str, Any]:
    """
    Strict servers may require every property to be present in 'required'.
    We include new_title, new_heading, new_body in BOTH properties and required.
    """
    schema_obj = {
        "type": "object",
        "properties": {
            "new_title":   {"type": "string"},
            "new_heading": {"type": "string"},
            "new_body":    {"type": "string"},
        },
        "required": ["new_title", "new_heading", "new_body"],
        "additionalProperties": False
    }
    return {
        "name": "seo_result",
        "schema": schema_obj,
        "strict": not loose
    }

def build_jsonl_requests(articles: List[Dict[str, Any]], loose_schema: bool) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Build /v1/chat/completions batch requests in JSONL format.
    Each line: {"custom_id": "...", "method": "POST", "url": "/v1/chat/completions", "body": {...}}
    """
    schema = build_schema(loose_schema)
    rows = []
    meta = {}
    for idx, art in enumerate(articles):
        custom_id = f"article_{idx}"
        prompt = make_prompt(art)

        body = {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "max_completion_tokens": 7000,
            "response_format": {
                "type": "json_schema",
                "json_schema": schema
            },
            "messages": [
                {"role": "system", "content": "Return only JSON for the requested schema. No extra text."},
                {"role": "user", "content": prompt}
            ]
        }

        rows.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": body
        })
        meta[custom_id] = {
            "index": idx,
            "original_title": (art.get("title") or "").strip()
        }
    return rows, meta

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def upload_and_create_batch(client: OpenAI, jsonl_path: Path) -> str:
    up = client.files.create(file=jsonl_path.open("rb"), purpose="batch")
    input_file_id = up.id
    logger.info(f"Uploaded JSONL file. file_id={input_file_id}")

    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/chat/completions",
        completion_window=COMPLETION_WINDOW,
    )
    logger.info(f"Created batch. id={batch.id} status={batch.status}")
    return batch.id

def poll_batch_until_done(client: OpenAI, batch_id: str, poll_seconds: int) -> Any:
    terminal = {"completed", "failed", "cancelled", "expired"}
    last_counts = None
    while True:
        batch = client.batches.retrieve(batch_id)
        counts = getattr(batch, "request_counts", None)
        if counts != last_counts:
            logger.info(f"Batch {batch.id}: status={batch.status} counts={counts}")
            last_counts = counts
        else:
            logger.info(f"Batch {batch.id}: status={batch.status}")
        if batch.status in terminal:
            return batch
        time.sleep(poll_seconds)

def download_file_bytes(client: OpenAI, file_id: str) -> bytes:
    resp = client.files.content(file_id)
    return getattr(resp, "read", lambda: getattr(resp, "text", "").encode("utf-8"))()

def load_articles(path: Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))

def parse_chat_output_line(line: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """
    Output line:
      {"custom_id":"article_0","response":{"status_code":200,"body":{"choices":[{"message":{"content":"{...json...}"}}]}}}
    """
    obj = json.loads(line)
    cid = obj.get("custom_id") or ""
    try:
        body = (obj.get("response") or {}).get("body") or {}
        choices = body.get("choices") or []
        if not choices:
            return cid, None, "No choices"
        msg = choices[0].get("message") or {}
        content = (msg.get("content") or "").strip()
        data = json.loads(content)
        return cid, data, None
    except Exception as e:
        return cid, None, f"parse error: {e}"

def merge_results(articles: List[Dict[str, Any]], output_jsonl: Path) -> Tuple[List[Dict[str, Any]], int, int]:
    mapping: Dict[str, Dict[str, Any]] = {}
    parse_fail = 0
    success = 0
    with output_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            cid, data, err = parse_chat_output_line(line)
            if err:
                logger.warning(f"Output parse issue for {cid}: {err}")
                parse_fail += 1
                continue
            new_title = (data.get("new_title") or "").strip()
            new_heading = (data.get("new_heading") or "").strip()
            new_body = (data.get("new_body") or "").strip()
            if new_title and new_heading and new_body:
                mapping[cid] = {
                    "seo_title": new_title,
                    "seo_heading": new_heading,
                    "new_body": new_body
                }
                success += 1
            else:
                parse_fail += 1
                logger.warning(f"Incomplete JSON for {cid}.")
    for idx, art in enumerate(articles):
        cid = f"article_{idx}"
        if cid in mapping:
            art["seo_title"] = mapping[cid]["seo_title"]
            art["seo_heading"] = mapping[cid]["seo_heading"]
            # **Replace the original body with the model-generated one**
            art["body"] = mapping[cid]["new_body"]
    return articles, success, parse_fail

# ---------- Error reporting ----------
def parse_error_line(line: str) -> Dict[str, Any]:
    obj = json.loads(line)
    cid = obj.get("custom_id")
    status = (obj.get("response", {}) or {}).get("status_code")
    err = obj.get("error") or {}
    msg = err.get("message") if isinstance(err, dict) else None
    code = err.get("code") if isinstance(err, dict) else None
    etype = err.get("type") if isinstance(err, dict) else None

    if not msg:
        body = (obj.get("response", {}) or {}).get("body") or {}
        berr = body.get("error") if isinstance(body, dict) else None
        if isinstance(berr, dict):
            msg = berr.get("message")
            code = berr.get("code")
            etype = berr.get("type")

    return {"custom_id": cid, "message": msg or "", "code": code, "type": etype, "status": status}

def build_error_summary(error_lines: List[str]):
    parsed = []
    bucket = Counter()
    samples = defaultdict(list)
    for ln in error_lines:
        if not ln.strip():
            continue
        rec = parse_error_line(ln)
        parsed.append(rec)
        reason_key = rec.get("code") or (rec.get("message")[:120] if rec.get("message") else f"HTTP {rec.get('status') or 'unknown'}")
        bucket[reason_key] += 1
        if len(samples[reason_key]) < 3:
            samples[reason_key].append(rec)
    top = bucket.most_common()
    return parsed, top, samples

def write_error_reports(text_path: Path, json_path: Path, error_lines: List[str],
                        meta_map: Dict[str, Dict[str, Any]], batch_id: str, counts: Any) -> None:
    parsed, top, samples = build_error_summary(error_lines)
    with text_path.open("w", encoding="utf-8") as tf:
        tf.write(f"# OpenAI Batch Error Report\n")
        tf.write(f"Batch ID: {batch_id}\n")
        tf.write(f"Request Counts: {counts}\n\n")
        if not parsed:
            tf.write("No error lines parsed.\n")
        else:
            tf.write("## Summary (Top Reasons)\n")
            for reason, n in top[:10]:
                tf.write(f"- {n}× {reason}\n")
                for ex in samples.get(reason, [])[:3]:
                    md = meta_map.get(ex.get("custom_id") or "", {})
                    tf.write(f"    • cid={ex.get('custom_id')} idx={md.get('index')} title={md.get('original_title','')[:80]}\n")
                    tf.write(f"      code={ex.get('code')} type={ex.get('type')} status={ex.get('status')}\n")
                    tf.write(f"      msg={ex.get('message')}\n")
            tf.write("\n## Per-item Errors\n")
            for rec in parsed:
                md = meta_map.get(rec.get("custom_id") or "", {})
                tf.write(f"- cid={rec.get('custom_id')} idx={md.get('index')} title={md.get('original_title','')}\n")
                tf.write(f"  code={rec.get('code')} type={rec.get('type')} status={rec.get('status')}\n")
                tf.write(f"  msg={rec.get('message')}\n")
    logger.info(f"Wrote error text report -> {text_path}")

    json_blob = {
        "batch_id": batch_id,
        "request_counts": counts if isinstance(counts, dict) else str(counts),
        "summary_top_reasons": top,
        "errors": [
            {**rec,
             "index": meta_map.get(rec.get("custom_id") or "", {}).get("index"),
             "original_title": meta_map.get(rec.get("custom_id") or "", {}).get("original_title")}
            for rec in parsed
        ],
    }
    json_path.write_text(json.dumps(json_blob, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Wrote error JSON report -> {json_path}")

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(description="Batch-generate SEO title/heading/BODY via /v1/chat/completions with JSON Schema.")
    ap.add_argument("--input", "-i", default="articles.json", help="Path to input articles.json")
    ap.add_argument("--out", "-o", default=OUTPUT_FILE, help="Path to write merged JSON")
    ap.add_argument("--poll", type=int, default=DEFAULT_POLL_SECONDS, help="Poll interval seconds (default 100)")
    ap.add_argument("--resume-batch-id", default=None, help="If set, skip creation and resume polling an existing batch id")
    ap.add_argument("--error-report", default=ERROR_REPORT_TXT, help="Path for text error report")
    ap.add_argument("--error-report-json", default=ERROR_REPORT_JSON, help="Path for JSON error report")
    ap.add_argument("--loose-schema", action="store_true", help="Relax structured-output schema (if you must)")
    args = ap.parse_args()

    client = OpenAI()  # uses OPENAI_API_KEY

    input_path = Path(args.input)
    out_path = Path(args.out)

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(2)

    articles = load_articles(input_path)
    if not isinstance(articles, list):
        logger.error("Input must be a JSON array of article objects.")
        sys.exit(2)

    # Build JSONL requests + meta map
    records, meta_map = build_jsonl_requests(articles, loose_schema=args.loose_schema)
    write_jsonl(Path(BATCH_INPUT_JSONL), records)

    # Submit or resume
    if args.resume_batch_id:
        logger.info(f"Resuming from batch id: {args.resume_batch_id}")
        batch = poll_batch_until_done(client, args.resume_batch_id, args.poll)
        batch_id = args.resume_batch_id
    else:
        batch_id = upload_and_create_batch(client, Path(BATCH_INPUT_JSONL))
        Path(BATCH_ID_FILE).write_text(batch_id, encoding="utf-8")
        logger.info(f"Saved batch id -> {BATCH_ID_FILE}")
        batch = poll_batch_until_done(client, batch_id, args.poll)

    # Terminal handling
    status = batch.status
    counts = getattr(batch, "request_counts", None)
    logger.info(f"Batch terminal status={status} counts={counts}")

    output_file_id = getattr(batch, "output_file_id", None)
    error_file_id = getattr(batch, "error_file_id", None)

    # Download output if present
    if output_file_id:
        out_bytes = download_file_bytes(client, output_file_id)
        Path(BATCH_OUTPUT_JSONL).write_bytes(out_bytes)
        logger.info(f"Downloaded output -> {BATCH_OUTPUT_JSONL}")
    else:
        logger.warning("No output_file_id present (possibly all items failed).")

    # Download errors and write reports
    error_lines: List[str] = []
    if error_file_id:
        err_bytes = download_file_bytes(client, error_file_id)
        Path(BATCH_ERROR_JSONL).write_bytes(err_bytes)
        logger.info(f"Downloaded errors -> {BATCH_ERROR_JSONL}")
        error_lines = [ln for ln in err_bytes.decode("utf-8", errors="replace").splitlines() if ln.strip()]
    else:
        logger.info("No error_file_id present.")

    # Merge successes
    successes = 0
    parse_failures = 0
    if output_file_id and Path(BATCH_OUTPUT_JSONL).exists():
        articles, successes, parse_failures = merge_results(articles, Path(BATCH_OUTPUT_JSONL))
        out_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"Merged {successes} item(s). Output parse failures: {parse_failures}. -> {out_path}")
    else:
        logger.info("Skip merge: no output file to merge.")

    # Error reports
    if error_lines:
        write_error_reports(
            text_path=Path(ERROR_REPORT_TXT),
            json_path=Path(ERROR_REPORT_JSON),
            error_lines=error_lines,
            meta_map=meta_map,
            batch_id=batch_id,
            counts=counts
        )
    else:
        logger.info("No error lines parsed; not writing error reports.")

    total = len(articles)
    failed_total = 0
    if counts and hasattr(counts, "failed"):
        failed_total = counts.failed
    elif error_lines:
        failed_total = len(error_lines)

    logger.info(
        f"SUMMARY: total={total}, merged_successes={successes}, "
        f"output_parse_failures={parse_failures}, batch_failed_items={failed_total}"
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception(f"Fatal error: {exc}")
        sys.exit(1)
