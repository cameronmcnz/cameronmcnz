#!/usr/bin/env python3
"""
Batch-generate SEO titles and headings for articles.json using OpenAI Batch + Responses API,
with extensive diagnostics and per-item error reporting.

- API: /v1/responses (Batch API)
- Model: gpt-5-mini
- Temperature: 1.0
- Structured Outputs (JSON schema) -> {new_title, new_heading, new_body? (optional)}
- Batch completion window: 24h
- Poll interval: configurable (default 100 seconds)
- Writes merged output: articles-funny.json
- Writes error reports: errors_report.txt / errors_report.json / (optional) errors_report.tsv
- Logs: batch_seo_titles.log and stdout

Prereqs:
  pip install openai==1.*  (new SDK)
  export OPENAI_API_KEY=...

Notes:
- "All failed" batches often indicate a parameter mismatch or schema reject. This script
  automatically tries token param fallback (max_completion_tokens -> max_output_tokens).
- Use --loose-schema to relax strictness and identify validation edge cases.
"""

import argparse
import csv
import html
import json
import logging
import os
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
ERROR_REPORT_TSV = None   # set by CLI if you want TSV too

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
    """Remove HTML tags and return first N words (normalized spaces)."""
    if not html_text:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(html_text))
    words = re.findall(r"\S+", text)
    return " ".join(words[:max_words])

def make_prompt(article: Dict[str, Any]) -> str:
    title = (article.get("title") or "").strip()
    tags = article.get("tags") or []
    body_300 = strip_html_to_words(article.get("body") or "", 300)

    # Build explicit instructions to ensure uniqueness & SEO focus
    prompt = f"""
You are an expert SEO editor.

Task:
- Propose TWO fields for this article:
  1) "new_title": An SEO-optimized, clickworthy title DIFFERENT from the original title (avoid duplicates and near-duplicates). Prefer 55–65 characters when natural. Include strong primary keywords derived from the content and tags, but avoid keyword stuffing.
  2) "new_heading": A distinct, complementary H1-style heading (not a paraphrase of the title). Aim 60–80 characters naturally. Target secondary or long-tail variants.

Rules:
- DO NOT repeat or trivially rephrase the original title.
- Keep language clear, specific, and human-sounding (no brackets like [Guide] unless justified).
- Avoid superlatives unless the content truly supports them.
- Keep brand terms only if clearly useful for search intent.
- American English.
- Return ONLY JSON via the provided schema.
- Do not use em-dashes, colons or semi-colons in the title or heading, but proper sentence structure instead.

Original:
- Original Title: {title}
- Tags: {", ".join(tags)}
- First 300 words of body (HTML stripped):
{body_300}
"""
    return prompt.strip()

def build_schema(loose: bool) -> Dict[str, Any]:
    schema = {
        "name": "seo_result",
        "schema": {
            "type": "object",
            "properties": {
                "new_title": {"type": "string"},
                "new_heading": {"type": "string"},
                # optional, but model may return it; keep in schema if desired
                "new_body": {"type": "string"},
            },
            "required": ["new_title", "new_heading"],
        },
        "strict": not loose,  # strict for default; relaxed with --loose-schema
    }
    if not loose:
        # lock down to required + optional only
        schema["schema"]["additionalProperties"] = False
    return schema

def build_jsonl_requests(articles: List[Dict[str, Any]], loose_schema: bool) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Build /v1/responses batch requests in JSONL format.
    Returns (records, meta_map) where:
      - records: list of JSONL request objects
      - meta_map: custom_id -> metadata (index, original title), for error reports
    """
    schema = build_schema(loose_schema)

    records = []
    meta = {}
    for idx, art in enumerate(articles):
        custom_id = f"article_{idx}"
        prompt = make_prompt(art)

        body = {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "response_format": {"type": "json_schema", "json_schema": schema},
            "input": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        }
        records.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/responses",
            "body": body
        })
        meta[custom_id] = {
            "index": idx,
            "original_title": (art.get("title") or "").strip()
        }
    return records, meta

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def safely_set_token_limit(body: Dict[str, Any], use_completion_tokens: bool) -> None:
    """
    Some orgs expect max_completion_tokens, others max_output_tokens on /v1/responses.
    Start with max_completion_tokens; on failure, reupload with max_output_tokens.
    """
    # First remove both (avoid duplicates on reinjection)
    body.pop("max_completion_tokens", None)
    body.pop("max_output_tokens", None)

    if use_completion_tokens:
        body["max_completion_tokens"] = 3000
    else:
        body["max_output_tokens"] = 3000

def inject_token_param(jsonl_path: Path, use_completion_tokens: bool) -> None:
    lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        obj = json.loads(line)
        body = obj.get("body", {})
        safely_set_token_limit(body, use_completion_tokens)
        obj["body"] = body
        new_lines.append(json.dumps(obj, ensure_ascii=False))
    jsonl_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

def upload_and_create_batch(client: OpenAI, jsonl_path: Path) -> str:
    up = client.files.create(file=jsonl_path.open("rb"), purpose="batch")
    input_file_id = up.id
    logger.info(f"Uploaded JSONL file. file_id={input_file_id}")

    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/responses",
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
    # SDK returns a stream-like object; try .read() if .text missing
    return getattr(resp, "read", lambda: getattr(resp, "text", "").encode("utf-8"))()

def load_articles(path: Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))

def parse_responses_output_line(line: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """
    Returns (custom_id, parsed_json_or_none, error_or_none) for an output line.
    For /v1/responses success lines, JSON is under response.output[0].content[0].text.
    """
    obj = json.loads(line)
    cid = obj.get("custom_id") or ""
    try:
        resp = obj["response"]
        outputs = resp.get("output", [])
        if not outputs:
            return cid, None, "No outputs"
        content = outputs[0].get("content", [])
        if not content:
            return cid, None, "No content"
        text_piece = content[0].get("text", "")
        data = json.loads(text_piece)
        return cid, data, None
    except Exception as e:
        return cid, None, f"parse error: {e}"

def merge_results(articles: List[Dict[str, Any]], output_jsonl: Path) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    Merge success lines into article objects.
    Returns (merged_articles, successes, parse_failures_in_output_file)
    """
    mapping: Dict[str, Dict[str, Any]] = {}
    parse_fail = 0
    success = 0

    with output_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            cid, data, err = parse_responses_output_line(line)
            if err:
                logger.warning(f"Output parse issue for {cid}: {err}")
                parse_fail += 1
                continue
            new_title = (data.get("new_title") or "").strip()
            new_heading = (data.get("new_heading") or "").strip()
            if new_title and new_heading:
                mapping[cid] = {"seo_title": new_title, "seo_heading": new_heading}
                success += 1
            else:
                parse_fail += 1
                logger.warning(f"Incomplete JSON for {cid}.")

    for idx, art in enumerate(articles):
        cid = f"article_{idx}"
        if cid in mapping:
            art["seo_title"] = mapping[cid]["seo_title"]
            art["seo_heading"] = mapping[cid]["seo_heading"]
    return articles, success, parse_fail

# ---------- Error reporting ----------
def parse_error_line(line: str) -> Dict[str, Any]:
    """
    Batch error JSONL line format (typical):
      {"custom_id":"article_0","error":{"message":"...","code":"...","type":"..."}}
    """
    obj = json.loads(line)
    cid = obj.get("custom_id")
    err = obj.get("error") or {}
    return {
        "custom_id": cid,
        "message": (err.get("message") if isinstance(err, dict) else str(err)) or "",
        "code": (err.get("code") if isinstance(err, dict) else None),
        "type": (err.get("type") if isinstance(err, dict) else None),
        # Some providers may echo response status:
        "status": (obj.get("response", {}) or {}).get("status_code"),
    }

def build_error_summary(error_lines: List[str]) -> Tuple[List[Dict[str, Any]], List[Tuple[str, int]], Dict[str, List[Dict[str, Any]]]]:
    """
    Returns:
      - parsed list of {custom_id, message, code, type, status}
      - top reason counts (message prefix or code)
      - samples per reason (up to 3)
    """
    parsed = []
    bucket = Counter()
    samples = defaultdict(list)

    for ln in error_lines:
        if not ln.strip():
            continue
        rec = parse_error_line(ln)
        parsed.append(rec)
        reason_key = rec.get("code") or (rec.get("message")[:120] if rec.get("message") else "unknown")
        bucket[reason_key] += 1
        if len(samples[reason_key]) < 3:
            samples[reason_key].append(rec)

    top = bucket.most_common()
    return parsed, top, samples

def write_error_reports(
    text_path: Path,
    json_path: Path,
    tsv_path: Optional[Path],
    error_lines: List[str],
    meta_map: Dict[str, Dict[str, Any]],
    batch_id: str,
    counts: Any
) -> None:
    """
    Write:
      - Text report (human)
      - JSON report (machine)
      - TSV (optional)
    Include meta (index + original title) if available.
    """
    parsed, top, samples = build_error_summary(error_lines)

    # Text report
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

    # JSON report
    json_blob = {
        "batch_id": batch_id,
        "request_counts": counts if isinstance(counts, dict) else str(counts),
        "summary_top_reasons": top,
        "errors": [
            {
                **rec,
                "index": meta_map.get(rec.get("custom_id") or "", {}).get("index"),
                "original_title": meta_map.get(rec.get("custom_id") or "", {}).get("original_title"),
            }
            for rec in parsed
        ],
    }
    json_path.write_text(json.dumps(json_blob, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Wrote error JSON report -> {json_path}")

    # TSV report (optional)
    if tsv_path:
        with tsv_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["custom_id", "index", "original_title", "code", "type", "status", "message"])
            for rec in parsed:
                md = meta_map.get(rec.get("custom_id") or "", {})
                w.writerow([
                    rec.get("custom_id"),
                    md.get("index"),
                    md.get("original_title"),
                    rec.get("code"),
                    rec.get("type"),
                    rec.get("status"),
                    rec.get("message"),
                ])
        logger.info(f"Wrote error TSV report -> {tsv_path}")

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(description="Batch-generate SEO titles/headings for articles.json (Responses Batch) with diagnostics.")
    ap.add_argument("--input", "-i", default="articles.json", help="Path to input articles.json")
    ap.add_argument("--out", "-o", default=OUTPUT_FILE, help="Path to write merged JSON")
    ap.add_argument("--poll", type=int, default=DEFAULT_POLL_SECONDS, help="Poll interval seconds (default 100)")
    ap.add_argument("--resume-batch-id", default=None, help="If set, skip creation and resume polling an existing batch id")
    ap.add_argument("--error-report", default=ERROR_REPORT_TXT, help="Path for text error report")
    ap.add_argument("--error-report-json", default=ERROR_REPORT_JSON, help="Path for JSON error report")
    ap.add_argument("--error-report-tsv", default=None, help="Optional TSV path for per-item errors")
    ap.add_argument("--loose-schema", action="store_true", help="Relax structured-output schema (helpful for debugging mass failures)")
    args = ap.parse_args()

    client = OpenAI()  # uses OPENAI_API_KEY

    # Files / paths
    input_path = Path(args.input)
    out_path = Path(args.out)
    jsonl_path = Path(BATCH_INPUT_JSONL)
    err_txt_path = Path(args.error_report)
    err_json_path = Path(args.error_report_json)
    err_tsv_path = Path(args.error_report_tsv) if args.error_report_tsv else None

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(2)

    # Load articles
    articles = load_articles(input_path)
    if not isinstance(articles, list):
        logger.error("Input must be a JSON array of article objects.")
        sys.exit(2)

    # Build JSONL requests and meta mapping for error reports
    records, meta_map = build_jsonl_requests(articles, loose_schema=args.loose_schema)
    write_jsonl(jsonl_path, records)

    # Inject token param (start with max_completion_tokens; retry with max_output_tokens if rejected)
    inject_token_param(jsonl_path, use_completion_tokens=True)

    # Submit or resume
    batch_id = args.resume_batch_id
    fallback_used = False

    def submit(_jsonl_path: Path) -> str:
        bid = upload_and_create_batch(client, _jsonl_path)
        Path(BATCH_ID_FILE).write_text(bid, encoding="utf-8")
        logger.info(f"Saved batch id -> {BATCH_ID_FILE}")
        return bid

    if batch_id:
        logger.info(f"Resuming from batch id: {batch_id}")
    else:
        try:
            batch_id = submit(jsonl_path)
        except OpenAIError as e:
            logger.warning(f"Initial submit failed; retrying with max_output_tokens. Error: {e}")
            inject_token_param(jsonl_path, use_completion_tokens=False)
            batch_id = submit(jsonl_path)
            fallback_used = True

    # Poll until terminal state
    batch = poll_batch_until_done(client, batch_id, args.poll)

    # Terminal handling
    status = batch.status
    counts = getattr(batch, "request_counts", None)
    logger.info(f"Batch terminal status={status} counts={counts}")

    # Download any files present
    output_file_id = getattr(batch, "output_file_id", None)
    error_file_id = getattr(batch, "error_file_id", None)

    if output_file_id:
        out_bytes = download_file_bytes(client, output_file_id)
        Path(BATCH_OUTPUT_JSONL).write_bytes(out_bytes)
        logger.info(f"Downloaded output -> {BATCH_OUTPUT_JSONL}")
    else:
        logger.warning("No output_file_id present (all items may have failed).")

    error_lines: List[str] = []
    if error_file_id:
        err_bytes = download_file_bytes(client, error_file_id)
        Path(BATCH_ERROR_JSONL).write_bytes(err_bytes)
        logger.info(f"Downloaded errors -> {BATCH_ERROR_JSONL}")
        # parse lines for reporting
        error_lines = [ln for ln in err_bytes.decode("utf-8", errors="replace").splitlines() if ln.strip()]
    else:
        logger.info("No error_file_id present.")

    # If we have successes, merge them into the articles
    successes = 0
    parse_failures = 0
    if output_file_id and Path(BATCH_OUTPUT_JSONL).exists():
        articles, successes, parse_failures = merge_results(articles, Path(BATCH_OUTPUT_JSONL))
        out_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"Merged {successes} item(s) from output. Parse-failed in output file: {parse_failures}. Wrote -> {out_path}")
    else:
        logger.info("Skip merge: no output file to merge.")

    # Always produce error reports if there are error lines
    if error_lines:
        write_error_reports(
            text_path=err_txt_path,
            json_path=err_json_path,
            tsv_path=err_tsv_path,
            error_lines=error_lines,
            meta_map=meta_map,
            batch_id=batch_id,
            counts=counts
        )
    else:
        logger.info("No error lines parsed; not writing error reports.")

    if fallback_used:
        logger.info("NOTE: The API rejected max_completion_tokens; used max_output_tokens=3000 instead.")

    # Final summary to logs
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

    # Helpful next steps when all failed
    if successes == 0 and failed_total >= total:
        logger.warning(
            "All items appear to have failed. Try:\n"
            "  - --loose-schema (relax structured outputs)\n"
            "  - shorter prompts (reduce input size)\n"
            "  - smaller batches (if you split outside of Batch API)\n"
            "  - verify your org/endpoint expects max_output_tokens vs max_completion_tokens\n"
        )

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception(f"Fatal error: {exc}")
        sys.exit(1)
