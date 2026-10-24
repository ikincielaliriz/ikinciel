#!/usr/bin/env python3
"""Validate FAQ JSON files and check for duplicate IDs/questions."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REQUIRED = {
    "id", "language", "category", "question", "answer", "keywords",
    "intent", "audience", "related_questions", "source_url",
    "last_updated", "review_status"
}
VALID_STATUSES = {"draft_review_required", "reviewed", "approved", "archived"}
errors = []
all_ids = {}
all_questions = {}
count = 0

for path in sorted(DATA_DIR.glob("*.json")):
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        continue
    if not isinstance(records, list):
        errors.append(f"{path.relative_to(ROOT)}: top-level JSON must be an array")
        continue
    for index, record in enumerate(records):
        count += 1
        loc = f"{path.relative_to(ROOT)}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{loc}: record must be an object")
            continue
        missing = REQUIRED - set(record)
        if missing:
            errors.append(f"{loc}: missing fields: {', '.join(sorted(missing))}")
            continue
        for field in ("id", "language", "category", "question", "answer", "intent"):
            if not isinstance(record[field], str) or not record[field].strip():
                errors.append(f"{loc}: {field} must be a non-empty string")
        if record["language"] != "tr":
            errors.append(f"{loc}: language must be 'tr'")
        if not isinstance(record["keywords"], list) or not record["keywords"]:
            errors.append(f"{loc}: keywords must be a non-empty array")
        if not isinstance(record["audience"], list) or not record["audience"] or not set(record["audience"]).issubset({"bireysel", "kurumsal"}):
            errors.append(f"{loc}: audience must contain bireysel and/or kurumsal")
        if record["review_status"] not in VALID_STATUSES:
            errors.append(f"{loc}: invalid review_status")
        rid = record["id"]
        if rid in all_ids:
            errors.append(f"{loc}: duplicate id {rid} (also in {all_ids[rid]})")
        else:
            all_ids[rid] = loc
        normalized_question = " ".join(record["question"].casefold().split())
        if normalized_question in all_questions:
            errors.append(f"{loc}: duplicate question (also in {all_questions[normalized_question]})")
        else:
            all_questions[normalized_question] = loc

print(f"Checked {count} FAQ record(s).")
if errors:
    print(f"Found {len(errors)} issue(s):")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Basic validation passed.")
