#!/usr/bin/env python3
"""
Trim windmills.json so only up to 2 records remain per unique project name.

Behavior:
- Create a timestamped backup: windmills-backup-YYYYMMDD-HHMMSS.json
- Read windmills.json (expects a JSON array of objects)
- Keep only the first 2 occurrences of each unique project
- Write results back to windmills.json (overwrite)
"""

import json
import os
from datetime import datetime

INPUT_FILE = "windmills.json"

def backup_file(path):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{os.path.splitext(path)[0]}-backup-{timestamp}.json"
    os.rename(path, backup_name)
    print(f"✅ Backup created: {backup_name}")
    return backup_name

def trim_duplicates(path):
    # Read backup file
    with open(path, "r", encoding="utf-8") as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return

    if not isinstance(records, list):
        print("❌ Expected a JSON array at top level.")
        return

    seen = {}
    trimmed = []

    for rec in records:
        project = rec.get("project", "").strip()
        seen[project] = seen.get(project, 0) + 1
        if seen[project] <= 2:
            trimmed.append(rec)

    print(f"✂️ Trimmed from {len(records)} → {len(trimmed)} records.")

    # Write cleaned file
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(trimmed, f, indent=4, ensure_ascii=False)
    print(f"✅ Cleaned file written to {INPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
    else:
        backup = backup_file(INPUT_FILE)
        trim_duplicates(backup)
