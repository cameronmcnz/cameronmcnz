#!/usr/bin/env python3
"""
Batch-generate SEO titles and headings for articles.json using OpenAI Batch + Responses API.

- Model: gpt-5-mini
- Temperature: 1.0
- Uses Structured Outputs (JSON schema) to get {new_title, new_heading}
- Batch completion window: 24h
- Poll interval: 100 seconds
- Writes merged output to: articles-seo.json
- Logs to: batch_seo_titles.log and stdout

Prereqs:
  pip install openai==1.*  (new SDK)
  export OPENAI_API_KEY=...
"""

import argparse
import html
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

from openai import OpenAI
from openai._exceptions import OpenAIError

# ---------- Constants ----------
MODEL = "gpt-5-mini"  # cost-efficient for well-defined tasks
TEMPERATURE = 1.0
POLL_SECONDS = 100
COMPLETION_WINDOW = "24h"  # Batch API window
BATCH_INPUT_JSONL = "openai-batch-input.jsonl"
BATCH_ID_FILE = "openai-batch-id.txt"
BATCH_OUTPUT_JSON = "openai-batch-output.jsonl"
OUTPUT_FILE = "articles-seo.json"
LOG_FILE = "batch_seo_titles.log"

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
    # Unescape HTML entities and remove tags
    text = re.sub(r"<[^>]+>", " ", html.unescape(html_text))
    # Collapse whitespace
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

def build_jsonl_requests(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build /v1/responses batch requests in JSONL format.
    Each line must be: {"custom_id": "...", "method": "POST", "url": "/v1/responses", "body": {...}}
    """
    schema = {
        "name": "seo_result",
        "schema": {
            "type": "object",
            "properties": {
                "new_title": {"type": "string"},
                "new_heading": {"type": "string"}
            },
            "required": ["new_title", "new_heading"],
            "additionalProperties": False
        },
        "strict": True,
    }

    records = []
    for idx, art in enumerate(articles):
        custom_id = f"article_{idx}"
        prompt = make_prompt(art)

        # Body for Responses API call
        body_common = {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "response_format": {"type": "json_schema", "json_schema": schema},
            # We'll set tokens in submit step with a fallback mechanism.
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }

        records.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/responses",
            "body": body_common
        })
    return records

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def safely_set_token_limit(body: Dict[str, Any], use_completion_tokens: bool) -> None:
    """
    Respect user's requirement to use max_completion_tokens (not max_tokens).
    We set either max_completion_tokens or, on fallback later, max_output_tokens.
    """
    if use_completion_tokens:
        body["max_completion_tokens"] = 3000
    else:
        # Fallback if API rejects the above (we flip later and re-upload).
        body["max_output_tokens"] = 3000

def inject_token_param(jsonl_path: Path, use_completion_tokens: bool) -> None:
    """Inject the appropriate token param into each JSONL body."""
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
    # Upload batch input file
    up = client.files.create(file=jsonl_path.open("rb"), purpose="batch")
    input_file_id = up.id
    logger.info(f"Uploaded JSONL file. file_id={input_file_id}")

    # Create batch job for /v1/responses with a 24h window
    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/responses",
        completion_window=COMPLETION_WINDOW,
    )
    logger.info(f"Created batch. id={batch.id} status={batch.status}")
    return batch.id

def poll_batch_until_done(client: OpenAI, batch_id: str) -> Any:
    """Poll every POLL_SECONDS until batch is completed/failed/expired/cancelled."""
    terminal = {"completed", "failed", "cancelled", "expired"}
    while True:
        batch = client.batches.retrieve(batch_id)
        logger.info(f"Batch {batch.id}: status={batch.status} "
                    f"counts={getattr(batch, 'request_counts', None)}")
        if batch.status in terminal:
            return batch
        time.sleep(POLL_SECONDS)

def download_file(client: OpenAI, file_id: str, to_path: Path) -> None:
    content = client.files.content(file_id)
    # For new SDK, .content(file_id) returns a stream-like object with .read()
    data = content.read()
    to_path.write_bytes(data)
    logger.info(f"Downloaded file {file_id} -> {to_path}")

def load_articles(path: Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))

def merge_results(articles: List[Dict[str, Any]], output_jsonl: Path) -> List[Dict[str, Any]]:
    """
    The output JSONL contains one line per request with `custom_id` and a `response` payload.
    We map custom_id back to index and attach seo_title/seo_heading.
    """
    # Map custom_id -> (new_title, new_heading)
    mapping: Dict[str, Dict[str, str]] = {}

    with output_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            custom_id = obj.get("custom_id")

            # The Responses API output structure:
            # obj["response"]["output"][0]["content"][0]["text"]
            # but since we used Structured Outputs JSON, it should be JSON text we can parse.
            try:
                resp = obj["response"]
                outputs = resp.get("output", [])
                if not outputs:
                    logger.warning(f"No outputs for {custom_id}")
                    continue
                first = outputs[0]
                content = first.get("content", [])
                if not content:
                    logger.warning(f"No content for {custom_id}")
                    continue
                text_piece = content[0].get("text", "").strip()
                data = json.loads(text_piece)
                new_title = (data.get("new_title") or "").strip()
                new_heading = (data.get("new_heading") or "").strip()
                if new_title and new_heading:
                    mapping[custom_id] = {"seo_title": new_title, "seo_heading": new_heading}
                else:
                    logger.warning(f"Incomplete JSON for {custom_id}: {text_piece[:120]}...")
            except Exception as e:
                logger.exception(f"Failed parsing output for {custom_id}: {e}")

    # Merge back into articles by index derived from custom_id
    for idx, art in enumerate(articles):
        cid = f"article_{idx}"
        if cid in mapping:
            art["seo_title"] = mapping[cid]["seo_title"]
            art["seo_heading"] = mapping[cid]["seo_heading"]
        else:
            logger.warning(f"No SEO result for {cid}; leaving article unchanged.")
    return articles

def main():
    global POLL_SECONDS
    ap = argparse.ArgumentParser(description="Batch-generate SEO titles/headings for articles.json")
    ap.add_argument("--input", "-i", default="articles.json", help="Path to articles.json")
    ap.add_argument("--out", "-o", default=OUTPUT_FILE, help="Path to write merged JSON")
    ap.add_argument("--poll", type=int, default=POLL_SECONDS, help="Poll interval seconds (default 100)")
    ap.add_argument("--resume-batch-id", default=None, help="If set, skip creation and resume polling an existing batch id")
    args = ap.parse_args()

    client = OpenAI()  # uses OPENAI_API_KEY

    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(2)

    articles = load_articles(input_path)
    if not isinstance(articles, list):
        logger.error("articles.json must contain an array of article records.")
        sys.exit(2)

    # Build JSONL requests
    requests = build_jsonl_requests(articles)
    jsonl_path = Path(BATCH_INPUT_JSONL)
    write_jsonl(jsonl_path, requests)

    # Inject preferred token param (max_completion_tokens). If API rejects later, we retry with fallback param.
    inject_token_param(jsonl_path, use_completion_tokens=True)

    batch_id = args.resume_batch_id
    fallback_used = False

    def submit(jsonl_file: Path) -> str:
        bid = upload_and_create_batch(client, jsonl_file)
        Path(BATCH_ID_FILE).write_text(bid, encoding="utf-8")
        logger.info(f"Saved batch id to {BATCH_ID_FILE}")
        return bid

    # Submit or resume
    if batch_id:
        logger.info(f"Resuming from batch id: {batch_id}")
    else:
        try:
            batch_id = submit(jsonl_path)
        except OpenAIError as e:
            # Heuristic: some orgs may have Responses API variant expecting max_output_tokens
            logger.warning(f"Initial submit failed; will retry with max_output_tokens. Error: {e}")
            # Re-inject with fallback param
            inject_token_param(jsonl_path, use_completion_tokens=False)
            batch_id = submit(jsonl_path)
            fallback_used = True

    # Poll until done
    
    POLL_SECONDS = args.poll
    batch = poll_batch_until_done(client, batch_id)

    # Handle terminal states
    if batch.status != "completed":
        logger.error(f"Batch ended in status={batch.status}. "
                     f"errors={getattr(batch, 'errors', None)}")
        sys.exit(3)

    # Download output
    if not getattr(batch, "output_file_id", None):
        logger.error("Batch completed but no output_file_id present.")
        sys.exit(4)

    download_file(client, batch.output_file_id, Path(BATCH_OUTPUT_JSON))

    # Merge
    merged = merge_results(articles, Path(BATCH_OUTPUT_JSON))
    Path(args.out).write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Wrote merged output to {args.out}")

    if fallback_used:
        logger.info("NOTE: The API rejected max_completion_tokens; "
                    "we fell back to max_output_tokens=3000 for compatibility.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception(f"Fatal error: {exc}")
        sys.exit(1)
