#!/usr/bin/env python3
import os
import json
import argparse
import re
import time
from typing import List, Dict, Any, Iterable

# Works with older SDKs that expose client.chat.completions.create
# pip install --upgrade openai  (optional)
from openai import OpenAI

# ----------------------------
# Config
# ----------------------------
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
INFILE_DEFAULT = "articles.txt"
OUTFILE_JSON = "articles.json"      # main pretty array for Jekyll
CHECKPOINT_JSONL = "articles.jsonl" # append-only log for recovery

SYSTEM_INSTRUCTIONS = (
    "You are an expert SEO and technical writer with a slightly sarcastic and funny style. "
    "Return only a single valid JSON object with keys: "
    "title, description, heading, body, tags. "
    "Do not include any prose before or after the JSON."
)

USER_TEMPLATE = """You will generate an SEO package for the article name below.

Article name:
{article_name}

Requirements:
- Fields: title, description, heading, body, tags (tags must be an array of exactly 10 strings).
- Title under 60 characters. No colons, no semicolons, no em dashes.
- Description under 155 characters. No colons, no semicolons, no em dashes.
- Heading is an H1 restating the title. No colons, no semicolons, no em dashes.
- Body is <= 500 words and in valid HTML. Start with:
  * If 'what is' subject -> first sentence is a direct one line definition.
  * If compare, vs, or difference between -> first sentence begins with 'The key difference between...'
  * If tutorial -> begin with a one line task summary, then an ordered list of steps, then short paragraphs that expand each step.
- Avoid em dashes, colons, and semicolons anywhere in the text and remove all LLM or chatGPT tells. Do not conclude the body with "Finally" or "In summary" or "In conclusions" or anything else that sounds like an LLM.
- In the body feel free to be slightly sarcastic and funny.
- In the body avoid the word 'it' and instead use a proper term or slightly different way to properly refer to the thing being discussed.
- Use only simple HTML tags: <p>, <ol>, <li>, <h2>, <h3>, <code>, <strong>, <em>, <a>.
- Return only a single JSON object and nothing else.
"""

# ----------------------------
# Helpers
# ----------------------------

EM_DASH = "\u2014"

def sanitize_text(s: str) -> str:
    if s is None:
        return s
    # Remove em dashes, colons, semicolons
    s = s.replace(EM_DASH, " ")
    s = s.replace(":", " ")
    s = s.replace(";", " ")
    # Collapse multiple spaces
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s

def hard_enforce_limits(obj: Dict[str, Any]) -> Dict[str, Any]:
    # Length caps
    obj["title"] = obj.get("title", "")
    obj["description"] = obj.get("description", "")
    obj["heading"] = obj.get("heading", "")
    obj["body"] = obj.get("body", "")
    obj["tags"] = obj.get("tags", [])

    if len(obj["title"]) > 60:
        obj["title"] = obj["title"][:60].rstrip()
    if len(obj["description"]) > 155:
        obj["description"] = obj["description"][:155].rstrip()

    # Sanitize forbidden punctuation
    for k in ["title", "description", "heading", "body"]:
        obj[k] = sanitize_text(obj[k])

    # Body max ~500 words
    words = obj["body"].split()
    if len(words) > 500:
        obj["body"] = " ".join(words[:500])

    # Tags cleaned, deduped, exactly 10
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

def safe_read_lines(path: str) -> Iterable[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield line

def load_checkpoint_items(path: str) -> List[Dict[str, Any]]:
    items = []
    for line in safe_read_lines(path):
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            # ignore a corrupt tail line
            continue
    return items

def write_checkpoint_item(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())

def rewrite_outfile_from_checkpoint(checkpoint_path: str, outfile_path: str) -> int:
    items = load_checkpoint_items(checkpoint_path)
    with open(outfile_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(items)

JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)

def parse_json_lenient(text: str) -> Dict[str, Any]:
    """
    Try strict json.loads first. If that fails, extract the first {...} block
    and parse it. Raises if nothing valid found.
    """
    try:
        return json.loads(text)
    except Exception:
        pass
    m = JSON_BLOCK_RE.search(text or "")
    if not m:
        raise ValueError("No JSON object found in model output")
    snippet = m.group(0)
    return json.loads(snippet)

def call_openai_chat(client: OpenAI, article_name: str, model: str) -> Dict[str, Any]:
    prompt = USER_TEMPLATE.format(article_name=article_name)
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                    {"role": "user", "content": prompt}
                ],
                temperature=1
            )
            content = resp.choices[0].message.content
            data = parse_json_lenient(content)
            return data
        except Exception as e:
            if attempt == max_retries:
                raise
            time.sleep(1.5 * attempt)

def generate_and_stream(titles: List[str], model: str) -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Already-done set for resume
    done_items = load_checkpoint_items(CHECKPOINT_JSONL)
    done_keys = {it.get("heading") or it.get("title") for it in done_items if isinstance(it, dict)}
    done_keys = {k for k in done_keys if k}

    for raw_title in titles:
        key = raw_title.strip()
        if not key:
            continue
        if key in done_keys:
            print(f"SKIP already generated: {key}")
            continue

        print(f"Generating: {key}")
        data = call_openai_chat(client, key, model)
        data = hard_enforce_limits(data)

        # Incremental append to checkpoint, then rewrite pretty JSON
        write_checkpoint_item(CHECKPOINT_JSONL, data)
        count = rewrite_outfile_from_checkpoint(CHECKPOINT_JSONL, OUTFILE_JSON)
        print(f"Appended and synced. Total items: {count}")

def load_titles(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]

def main():
    parser = argparse.ArgumentParser(
        description="Generate SEO JSON packs incrementally with recovery (chat.completions compatible)."
    )
    parser.add_argument(
        "titles",
        nargs="*",
        help=f"Article names. If omitted, defaults to {INFILE_DEFAULT}."
    )
    parser.add_argument(
        "--infile",
        help=f"Path to a text file with one article name per line. Default: {INFILE_DEFAULT}"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model. Default: {DEFAULT_MODEL}"
    )
    args = parser.parse_args()

    # Titles source priority: CLI args > --infile > articles.txt
    if args.titles:
        titles = [t for t in args.titles if t.strip()]
    else:
        infile = args.infile or INFILE_DEFAULT
        if os.path.exists(infile):
            titles = load_titles(infile)
        else:
            raise SystemExit(f"No titles provided and {infile} not found.")

    try:
        generate_and_stream(titles, args.model)
    except KeyboardInterrupt:
        total = rewrite_outfile_from_checkpoint(CHECKPOINT_JSONL, OUTFILE_JSON)
        print(f"\nInterrupted. Wrote {total} items to {OUTFILE_JSON}. Check {CHECKPOINT_JSONL} to resume.")
    except Exception as e:
        total = rewrite_outfile_from_checkpoint(CHECKPOINT_JSONL, OUTFILE_JSON)
        print(f"\nError: {e}\nRecovered {total} items into {OUTFILE_JSON}. You can rerun to resume.")
    else:
        total = rewrite_outfile_from_checkpoint(CHECKPOINT_JSONL, OUTFILE_JSON)
        print(f"Done. Wrote {total} items to {OUTFILE_JSON}")
        print(f"Checkpoint retained at {CHECKPOINT_JSONL} for resume if needed.")

if __name__ == "__main__":
    main()
