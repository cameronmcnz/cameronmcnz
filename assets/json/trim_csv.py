#!/usr/bin/env python3
"""
Trim windmills.csv so only up to 2 records remain per unique project name.

Behavior:
- Create a timestamped backup: windmills-backup-YYYYMMDD-HHMMSS.csv
- Read windmills.csv (expects header row)
- Keep only the first 2 occurrences of each unique project
- Write results back to windmills.csv (overwrite)
"""

import csv
import os
from datetime import datetime

INPUT_FILE = "windmills.csv"

def backup_file(path):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{os.path.splitext(path)[0]}-backup-{timestamp}.csv"
    os.rename(path, backup_name)
    print(f"✅ Backup created: {backup_name}")
    return backup_name

def trim_duplicates(path):
    # Read backup
    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        if not reader:
            print("⚠️ No records found.")
            return

    header = reader[0].keys()
    seen = {}
    trimmed = []

    for row in reader:
        project = row.get("project", "").strip()
        seen[project] = seen.get(project, 0) + 1
        if seen[project] <= 2:
            trimmed.append(row)

    print(f"✂️ Trimmed from {len(reader)} → {len(trimmed)} records.")

    # Write new cleaned file
    with open(INPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(trimmed)
    print(f"✅ Cleaned file written to {INPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
    else:
        backup = backup_file(INPUT_FILE)
        trim_duplicates(backup)
