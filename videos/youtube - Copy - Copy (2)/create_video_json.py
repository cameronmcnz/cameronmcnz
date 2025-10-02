#!/usr/bin/env python3
import os
import json
import argparse
import re
import time
import csv
from typing import List, Dict, Any, Iterable, Optional, Tuple
from datetime import datetime, timezone
from collections import Counter, defaultdict

from openai import OpenAI

# ==========================
# Config / Constants
# ==========================
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CSV_DEFAULT = "consolidated.csv"
OUTFILE_JSON = "articles.json"
CHECKPOINT_JSONL = "articles.jsonl"

STATE_PATH = "batches_state.json"   # persistent state for recovery
BATCH_COMPLETION_WINDOW = "24h"     # per OpenAI Batch API
POLL_INTERVAL_SECONDS = 60          # how often to poll a batch’s status
MAX_POLL_HOURS = 24                 # hard stop window

# Stable video meta fields
VIDEO_HOST = "youtube"
PUBLISHER_NAME = "certificationExams.pro"
PUBLISHER_LOGO = "/assets/images/logo-512.png"
IN_LANGUAGE = "en"
IS_ACCESSIBLE_FOR_FREE = True

SYSTEM_INSTRUCTIONS = (
    "You are an expert SEO and technical writer with a slightly sarcastic and funny style. "
    "Return only a single valid JSON object with keys: title, description, heading, body, tags. "
    "Do not include any prose before or after the JSON."
)

USER_TEMPLATE_SINGLE = """You will create an informative, easy to read, technical and educational article that is less than 500 words long based on a YouTube video.

Video context:
- Video title: {video_title}
- Video ID: {video_id}
- Publish timestamp: {publish_ts}
- Duration: {duration_hms} ({duration_ms} ms)

Write a compact article that would make sense as a companion to the video topic. Avoid sounding like a transcript. Do not mention the video ID in the article.

Requirements:
- Fields: title, description, heading, body, tags (tags must be an array of exactly 10 strings).
- No colons, no semicolons, no em dashes.
- Title under 60 characters. Use the video title provided as the title. Add a question mark at the end if the title is a question.
- SEO optimized dscription under 155 characters. No colons, no semicolons, no em dashes.
- Heading restates the title in an SEO optimized way. No colons, no semicolons, no em dashes.
- Body is <= 500 words and in valid HTML. Start with:
  * If 'what is' subject -> first sentence is a direct one line definition.
  * If compare, vs, or difference between -> first sentence begins with 'The key difference between...'
  * If tutorial -> begin with a high level overview of what is being taught, then provide an ordered list of steps, and then short short paragraphs that expand each step. Add a summary at the end that recaps what the tutorial was about, but don't use headings or terms like "Finally" or "In conclustion" or any other ChatGPT 'tells.'
- Avoid em dashes, colons, and semicolons anywhere in the text and remove all LLM or chatGPT tells. Do not conclude the body with "Finally" or "In summary" or "In conclusions" or anything else that sounds like an LLM.
- In the body feel free to be slightly sarcastic and funny.
- In the body avoid the word 'it' and instead use a proper term or slightly different way to properly refer to the thing being discussed.
- At the end, add a <h2> or <h3> heading with the word 'Tip' in it and provide some type of insightful tip on the topic.
- Use only simple HTML tags: <p>, <ol>, <li>, <h2>, <h3>, <code>, <strong>, <em>, <a>.
"""

EM_DASH = "\u2014"

# ==========================
# Logging
# ==========================
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def log(msg: str) -> None:
    print(f"[{now_iso()}] {msg}", flush=True)

# ==========================
# Text + JSON helpers
# ==========================
def sanitize_text(s: str) -> str:
    if s is None:
        return s
    s = s.replace(EM_DASH, " ")
    s = s.replace(":", " ")
    s = s.replace(";", " ")
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s

def hard_enforce_limits(obj: Dict[str, Any]) -> Dict[str, Any]:
    obj["title"] = obj.get("title", "")
    obj["description"] = obj.get("description", "")
    obj["heading"] = obj.get("heading", "")
    obj["body"] = obj.get("body", "")
    obj["tags"] = obj.get("tags", [])

    if len(obj["title"]) > 60:
        obj["title"] = obj["title"][:60].rstrip()
    if len(obj["description"]) > 155:
        obj["description"] = obj["description"][:155].rstrip()

    for k in ["title", "description", "heading", "body"]:
        obj[k] = sanitize_text(obj[k])

    words = obj["body"].split()
    if len(words) > 500:
        obj["body"] = " ".join(words[:500])

    cleaned = []
    seen = set()
    for t in obj.get("tags", []):
        t_clean = sanitize_text(str(t))
        key = t_clean.lower()
        if t_clean and key not in seen:
            seen.add(key)
            cleaned.append(t_clean)
    cleaned = cleaned[:10]
    while len(cleaned) < 10:
        cleaned.append(cleaned[-1] if cleaned else "git")
    obj["tags"] = cleaned
    return obj

JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)
def parse_json_lenient(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        pass
    m = JSON_BLOCK_RE.search(text or "")
    if not m:
        raise ValueError("No JSON object found in model output")
    return json.loads(m.group(0))

# ==========================
# File IO helpers
# ==========================
def safe_read_lines(path: str) -> Iterable[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line

def load_checkpoint_items(path: str) -> List[Dict[str, Any]]:
    items = []
    for line in safe_read_lines(path):
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items

def write_checkpoint_item(obj: Dict[str, Any]) -> None:
    with open(CHECKPOINT_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())

def rewrite_outfile_from_checkpoint() -> int:
    items = load_checkpoint_items(CHECKPOINT_JSONL)
    with open(OUTFILE_JSON, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(items)

def read_csv_rows(csv_path: str) -> List[Dict[str, str]]:
    if not os.path.exists(csv_path):
        raise SystemExit(f"CSV file not found: {csv_path}")
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required_cols = {
            "Video ID",
            "Video Title (Original)",
            "Approx Duration (ms)",
            "Video Publish Timestamp",
        }
        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"CSV missing required columns: {', '.join(sorted(missing))}")
        return [row for row in reader]

def get_done_keys_from_checkpoint() -> set[str]:
    done_items = load_checkpoint_items(CHECKPOINT_JSONL)
    done_keys = {it.get("heading") or it.get("title") for it in done_items if isinstance(it, dict)}
    return {k for k in done_keys if k}

# ==========================
# Video metadata helpers
# ==========================
def ms_to_hms(ms: Optional[str]) -> str:
    try:
        ms_int = int(ms)
    except Exception:
        return "unknown"
    total_seconds = ms_int // 1000
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"

def ms_to_iso8601_duration(ms: Optional[str]) -> str:
    try:
        ms_int = int(ms)
    except Exception:
        return ""
    total_seconds = ms_int // 1000
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    out = "PT"
    if h > 0:
        out += f"{h}H"
    if m > 0 or h > 0:
        out += f"{m}M"
    out += f"{s}S"
    return out

def normalize_upload_date(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    if s.endswith("Z"):
        return s[:-1] + "+00:00"
    if re.search(r"[+-]\d{2}:\d{2}$", s):
        return s
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", s):
        return s + "+00:00"
    return s

def build_video_meta(row: Dict[str, str]) -> Dict[str, Any]:
    vid = (row.get("Video ID") or "").strip()
    publish_ts_raw = (row.get("Video Publish Timestamp") or "").strip()
    duration_ms_raw = (row.get("Approx Duration (ms)") or "").strip()
    upload_date = normalize_upload_date(publish_ts_raw)
    duration_iso = ms_to_iso8601_duration(duration_ms_raw)
    return {
        "video_host": VIDEO_HOST,
        "video_id": vid,
        "upload_date": upload_date,
        "duration": duration_iso,
        "thumbnail_url": f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" if vid else "",
        "content_url": f"https://youtu.be/{vid}" if vid else "",
        "embed_url": f"https://www.youtube.com/embed/{vid}" if vid else "",
        "publisher_name": PUBLISHER_NAME,
        "publisher_logo": PUBLISHER_LOGO,
        "in_language": IN_LANGUAGE,
        "is_accessible_for_free": IS_ACCESSIBLE_FOR_FREE,
    }

# ==========================
# Batch state
# ==========================
def load_state() -> Dict[str, Any]:
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"batches": [], "rows_meta": {}}

def save_state(state: Dict[str, Any]) -> None:
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)

# ==========================
# OpenAI Batch helpers
# ==========================
def build_request_body_for_row(row: Dict[str, str], model: str) -> Dict[str, Any]:
    video_title = (row.get("Video Title (Original)") or "").strip()
    video_id = (row.get("Video ID") or "").strip()
    publish_ts = (row.get("Video Publish Timestamp") or "").strip()
    duration_ms = (row.get("Approx Duration (ms)") or "").strip()
    duration_hms = ms_to_hms(duration_ms)

    prompt = USER_TEMPLATE_SINGLE.format(
        video_title=video_title,
        video_id=video_id,
        publish_ts=publish_ts,
        duration_hms=duration_hms,
        duration_ms=duration_ms or "unknown"
    )
    # Hardened: force JSON object output and cap tokens
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1,
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 4000
    }

def write_jsonl_requests(rows: List[Dict[str, str]], start_idx: int, model: str, path: str) -> List[str]:
    custom_ids = []
    with open(path, "w", encoding="utf-8") as f:
        for i, row in enumerate(rows):
            idx = start_idx + i
            cid = str(idx)
            body = build_request_body_for_row(row, model)
            rec = {
                "custom_id": cid,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": body,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            custom_ids.append(cid)
    return custom_ids

def parse_batch_output_line(line: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    obj = json.loads(line)
    cid = str(obj.get("custom_id", ""))
    resp = obj.get("response")
    if resp and isinstance(resp, dict) and resp.get("status_code") == 200:
        body = resp.get("body", {})
        choices = (body or {}).get("choices") or []
        if not choices:
            return cid, None, "No choices in response body"
        content = choices[0].get("message", {}).get("content", "")
        try:
            article = parse_json_lenient(content)
            return cid, article, None
        except Exception as e:
            return cid, None, f"Invalid JSON in content: {e}"
    err = obj.get("error") or {}
    if err:
        # A Batch "error file" entry (not per-item HTTP) will land here when we read the error file.
        # err might contain { "message": "...", "code": "...", ... }
        msg = err.get("message") if isinstance(err, dict) else str(err)
        return cid, None, msg or "API error"
    if resp and resp.get("status_code") and resp.get("status_code") != 200:
        return cid, None, f"Non-200 status: {resp.get('status_code')}"
    return cid, None, "Unknown output format"

# ==========================
# Reconcile + Attach
# ==========================
def reconcile_batches_from_api(client: OpenAI, state: Dict[str, Any]) -> None:
    changed = False
    for b in state.get("batches", []):
        bid = b.get("batch_id")
        if not bid:
            continue
        try:
            bj = client.batches.retrieve(bid)
        except Exception as e:
            log(f"[WARN] reconcile: failed to retrieve {bid}: {e}")
            continue
        b["status"] = bj.status
        b["output_file_id"] = getattr(bj, "output_file_id", b.get("output_file_id"))
        b["error_file_id"]  = getattr(bj, "error_file_id",  b.get("error_file_id"))
        changed = True
    if changed:
        save_state(state)

def attach_remote_batches(client: OpenAI, state: Dict[str, Any], limit: int = 200) -> None:
    try:
        lst = client.batches.list(limit=limit)
    except Exception as e:
        log(f"[WARN] attach_remote: cannot list batches: {e}")
        return

    have = {b["batch_id"] for b in state.get("batches", []) if b.get("batch_id")}
    added = 0
    for bj in getattr(lst, "data", []) or []:
        bid = bj.id
        if bid in have:
            continue
        entry = {
            "batch_id": bid,
            "input_file_id": getattr(bj, "input_file_id", None),
            "status": bj.status,
            "created_at": int(time.time()),
            "size": None,
            "start_cid": None,
            "end_cid": None,
            "output_file_id": getattr(bj, "output_file_id", None),
            "error_file_id": getattr(bj, "error_file_id", None),
            "processed": False,
            "retry_parent": None,
        }
        state["batches"].append(entry)
        added += 1
    if added:
        save_state(state)
        log(f"attach_remote: added {added} remote batch(es) to local state.")
    else:
        log("attach_remote: no new remote batches found.")

# ==========================
# Diagnostics for errors
# ==========================
def summarize_error_file(text: str) -> Dict[str, Any]:
    reasons = Counter()
    samples = defaultdict(list)
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        cid = str(obj.get("custom_id", ""))
        err = obj.get("error") or {}
        msg = err.get("message") if isinstance(err, dict) else str(err)
        key = (err.get("code") if isinstance(err, dict) else None) or (msg[:80] if msg else "unknown")
        reasons[key] += 1
        if len(samples[key]) < 3:
            samples[key].append({"cid": cid, "message": msg})
    return {"counts": reasons.most_common(), "samples": {k: v for k, v in samples.items()}}

def print_error_summary(prefix: str, summary: Dict[str, Any]) -> None:
    counts = summary.get("counts") or []
    samples = summary.get("samples") or {}
    if not counts:
        log(f"{prefix}: no structured errors to summarize.")
        return
    log(f"{prefix}: top reasons:")
    for reason, n in counts[:5]:
        log(f"  - {n}× {reason}")
        for ex in samples.get(reason, [])[:2]:
            log(f"      example cid={ex['cid']}: {ex['message']}")

# ==========================
# Batch creation
# ==========================
def create_batches_from_csv(client: OpenAI, csv_path: str, model: str, batch_size: int, state: Dict[str, Any], retry_failures: bool) -> None:
    all_rows = read_csv_rows(csv_path)
    done_keys = get_done_keys_from_checkpoint()

    pending_rows = []
    for row in all_rows:
        title = (row.get("Video Title (Original)") or "").strip()
        if title and title not in done_keys:
            pending_rows.append(row)

    if not pending_rows:
        log("No new rows to submit. Skipping batch creation.")
        return

    start_global = len(state.get("rows_meta", {}))
    created = 0

    for offset in range(0, len(pending_rows), batch_size):
        chunk = pending_rows[offset: offset + batch_size]
        tmp_jsonl = f"batch_input_{start_global}.jsonl"
        _ = write_jsonl_requests(chunk, start_idx=start_global, model=model, path=tmp_jsonl)

        for i, row in enumerate(chunk):
            cid = str(start_global + i)
            state["rows_meta"][cid] = row

        log(f"Uploading input file {tmp_jsonl} for {len(chunk)} items...")
        up = client.files.create(file=open(tmp_jsonl, "rb"), purpose="batch")
        input_file_id = up.id

        log("Creating Batch job...")
        bj = client.batches.create(
            input_file_id=input_file_id,
            endpoint="/v1/chat/completions",
            completion_window=BATCH_COMPLETION_WINDOW,
        )
        state["batches"].append({
            "batch_id": bj.id,
            "input_file_id": input_file_id,
            "status": bj.status,
            "created_at": int(time.time()),
            "size": len(chunk),
            "start_cid": start_global,
            "end_cid": start_global + len(chunk) - 1,
            "output_file_id": None,
            "error_file_id": None,
            "processed": False,
            "retry_parent": None,
        })
        save_state(state)
        created += 1
        start_global += len(chunk)

    log(f"Created {created} batch job(s). State saved to {STATE_PATH}.")

# ==========================
# Direct fallback (non-batch) for failures
# ==========================
def direct_fallback_for_cids(client: OpenAI, state: Dict[str, Any], cids: List[str], model: str) -> int:
    """Generate outputs immediately for failed items using normal Chat Completions."""
    appended = 0
    for cid in cids:
        row = state["rows_meta"].get(cid)
        if not row:
            continue
        body = build_request_body_for_row(row, model)
        try:
            resp = client.chat.completions.create(**body)
            content = resp.choices[0].message.content
            article = parse_json_lenient(content)
            article = hard_enforce_limits(article)
            article.update(build_video_meta(row))
            write_checkpoint_item(article)
            appended += 1
        except Exception as e:
            log(f"[fallback] cid={cid} failed: {e}")
    if appended:
        total = rewrite_outfile_from_checkpoint()
        log(f"[fallback] appended {appended} items. File total now {total}.")
    return appended

# ==========================
# Polling + Processing
# ==========================
def poll_and_process_batches(client: OpenAI, state: Dict[str, Any], max_hours: int, interval_sec: int, retry_failures: bool, fallback_direct: bool, model: str) -> None:
    start_time = time.time()
    while True:
        reconcile_batches_from_api(client, state)

        remaining = [b for b in state["batches"] if not b.get("processed")]
        if not remaining:
            log("All batches processed.")
            break

        elapsed_h = (time.time() - start_time) / 3600.0
        if elapsed_h > max_hours:
            log(f"Reached max polling window of {max_hours} hours; exiting.")
            break

        for b in remaining:
            bid = b["batch_id"]
            status = b.get("status")
            log(f"Batch {bid}: status={status} size={b.get('size')} cid_range=[{b.get('start_cid')},{b.get('end_cid')}]")

            if status == "completed":
                appended, failed_cids = process_completed_batch(client, state, b)
                # Decide recovery path for failures
                if failed_cids:
                    if fallback_direct:
                        log(f"Batch {bid}: attempting direct fallback for {len(failed_cids)} failed item(s).")
                        direct_fallback_for_cids(client, state, failed_cids, model=model)
                        # mark processed regardless; we've handled what we could now
                        b["processed"] = True
                        save_state(state)
                    elif retry_failures:
                        log(f"Batch {bid}: re-queuing {len(failed_cids)} failed item(s) into a new batch.")
                        retry_batch_from_specific_cids(client, state, failed_cids, parent=b, model=model)
                        b["processed"] = True
                        save_state(state)
                    else:
                        log(f"Batch {bid}: {len(failed_cids)} failed item(s). Use --retry-failures or --fallback-direct to handle them.")
                        b["processed"] = True
                        save_state(state)
                else:
                    b["processed"] = True
                    save_state(state)

            elif status in ("failed", "expired", "canceled"):
                log(f"Batch {bid} ended with status {status}.")
                # There is likely an error_file_id; try to move them forward
                failed_cids = get_failed_cids_from_error_file(client, b.get("error_file_id"))
                if failed_cids:
                    if fallback_direct:
                        log(f"Batch {bid}: direct fallback for {len(failed_cids)} item(s) after {status}.")
                        direct_fallback_for_cids(client, state, failed_cids, model=model)
                    elif retry_failures:
                        retry_batch_from_specific_cids(client, state, failed_cids, parent=b, model=model)
                b["processed"] = True
                save_state(state)
            # else: validating/queued/in_progress/finalizing -> wait

        time.sleep(interval_sec)

def get_failed_cids_from_error_file(client: OpenAI, err_id: Optional[str]) -> List[str]:
    if not err_id:
        return []
    try:
        err_resp = client.files.content(err_id)
        err_text = getattr(err_resp, "text", None) or err_resp.read().decode("utf-8", errors="replace")
    except Exception:
        return []
    failed_cids: List[str] = []
    for ln in err_text.splitlines():
        try:
            obj = json.loads(ln)
            if "custom_id" in obj:
                failed_cids.append(str(obj["custom_id"]))
        except Exception:
            continue
    return failed_cids

def process_completed_batch(client: OpenAI, state: Dict[str, Any], binfo: Dict[str, Any]) -> Tuple[int, List[str]]:
    """
    Returns (appended_count, failed_cids)
    - If output file missing but error file exists, summarize and return failed cids.
    """
    bid = binfo["batch_id"]
    out_id = binfo.get("output_file_id")
    err_id = binfo.get("error_file_id")

    appended = 0
    failed_cids: List[str] = []

    # Output
    if out_id:
        log(f"Downloading output for batch {bid} (file {out_id})...")
        try:
            content_resp = client.files.content(out_id)
            content = getattr(content_resp, "text", None) or content_resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            log(f"[WARN] Could not download output file {out_id}: {e}")
            content = ""

        for ln in (content or "").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            cid, article, err = parse_batch_output_line(ln)
            if article is None:
                # Some providers echo per-line errors into output file; treat as failure for this cid
                log(f"[WARN] Batch {bid} cid={cid} parse issue in output: {err}")
                if cid:
                    failed_cids.append(cid)
                continue

            row = state["rows_meta"].get(str(cid), {}) or {}
            article = hard_enforce_limits(article)
            article.update(build_video_meta(row))
            write_checkpoint_item(article)
            appended += 1

        if appended:
            total = rewrite_outfile_from_checkpoint()
            log(f"Batch {bid}: appended {appended} items. File total now {total}.")

    # Errors
    if err_id:
        try:
            err_resp = client.files.content(err_id)
            err_text = getattr(err_resp, "text", None) or err_resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            log(f"[WARN] Could not download error file {err_id}: {e}")
            err_text = ""

        if err_text:
            summary = summarize_error_file(err_text)
            print_error_summary(f"Batch {bid} error summary", summary)
            # Collect failed cids (even if some succeeded)
            for ln in err_text.splitlines():
                try:
                    obj = json.loads(ln)
                    if "custom_id" in obj:
                        failed_cids.append(str(obj["custom_id"]))
                except Exception:
                    continue

    # Deduplicate failed cids
    failed_cids = sorted(set(failed_cids))
    if failed_cids:
        log(f"Batch {bid}: {len(failed_cids)} failed item(s).")
    return appended, failed_cids

# ==========================
# Retry helpers
# ==========================
def retry_batch_from_specific_cids(client: OpenAI, state: Dict[str, Any], failed_cids: List[str], parent: Dict[str, Any], model: str) -> None:
    failed_rows: List[Dict[str, str]] = []
    for cid in failed_cids:
        row = state["rows_meta"].get(cid)
        if row:
            failed_rows.append(row)
    if not failed_rows:
        log("retry: no rows available for failed cids; skipping.")
        return

    start_idx = max((int(k) for k in state["rows_meta"].keys()), default=-1) + 1
    tmp_jsonl = f"batch_retry_{start_idx}.jsonl"
    write_jsonl_requests(failed_rows, start_idx=start_idx, model=model, path=tmp_jsonl)

    # remap new cids -> same rows
    for i, row in enumerate(failed_rows):
        cid = str(start_idx + i)
        state["rows_meta"][cid] = row

    up = client.files.create(file=open(tmp_jsonl, "rb"), purpose="batch")
    bj = client.batches.create(
        input_file_id=up.id,
        endpoint="/v1/chat/completions",
        completion_window=BATCH_COMPLETION_WINDOW,
    )
    state["batches"].append({
        "batch_id": bj.id,
        "input_file_id": up.id,
        "status": bj.status,
        "created_at": int(time.time()),
        "size": len(failed_rows),
        "start_cid": start_idx,
        "end_cid": start_idx + len(failed_rows) - 1,
        "output_file_id": None,
        "error_file_id": None,
        "processed": False,
        "retry_parent": parent["batch_id"],
    })
    save_state(state)
    log(f"Retry batch {bj.id} created for {len(failed_rows)} failed item(s).")

# ==========================
# CLI / Main
# ==========================
def main():
    parser = argparse.ArgumentParser(
        description="Create and monitor OpenAI Batch jobs for CSV rows, with persistent batch_id, auto-recovery, diagnostics, and progressive output."
    )
    parser.add_argument("--csvfile", default=CSV_DEFAULT,
                        help=f"CSV with 'Video ID','Video Title (Original)','Approx Duration (ms)','Video Publish Timestamp'")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model (default: {DEFAULT_MODEL})")
    parser.add_argument("--batch-size", type=int, default=200, help="Rows per batch JSONL (default: 200)")
    parser.add_argument("--retry-failures", action="store_true", help="Requeue failed items into a new batch automatically")
    parser.add_argument("--fallback-direct", action="store_true", help="Immediately convert failed items with direct API calls (non-batch) and write results")
    parser.add_argument("--no-create", action="store_true", help="Do not create new batches; only poll/process existing state")
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL_SECONDS, help="Polling interval seconds (default: 60)")
    parser.add_argument("--max-hours", type=int, default=MAX_POLL_HOURS, help="Max hours to poll before exiting (default: 24)")
    parser.add_argument("--attach-remote", action="store_true", help="Fetch remote batches from API and merge into local state before polling")

    args = parser.parse_args()

    if not OPENAI_API_KEY:
        raise SystemExit("OPENAI_API_KEY not set")

    client = OpenAI(api_key=OPENAI_API_KEY)
    state = load_state()

    try:
        if args.attach_remote:
            attach_remote_batches(client, state)

        reconcile_batches_from_api(client, state)

        if not args.no_create:
            create_batches_from_csv(client, args.csvfile, args.model, args.batch_size, state, args.retry_failures)

        poll_and_process_batches(
            client=client,
            state=state,
            max_hours=args.max_hours,
            interval_sec=args.poll_interval,
            retry_failures=args.retry_failures,
            fallback_direct=args.fallback_direct,
            model=args.model
        )

    except KeyboardInterrupt:
        total = rewrite_outfile_from_checkpoint()
        log(f"\nInterrupted. Synced {total} items to {OUTFILE_JSON}. Batches state is saved at {STATE_PATH}.")
    except Exception as e:
        total = rewrite_outfile_from_checkpoint()
        log(f"\nError: {e}\nRecovered {total} items into {OUTFILE_JSON}. State saved at {STATE_PATH}.")
    else:
        total = rewrite_outfile_from_checkpoint()
        log(f"Done. Wrote {total} items to {OUTFILE_JSON}. Batch state retained at {STATE_PATH} for audit.")

if __name__ == "__main__":
    main()
