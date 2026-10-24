#!/usr/bin/env python3
"""Validate FAQ JSON records, category index consistency, and optional JSON Schema rules.

Run from any directory:
    python3 validate.py

The core checks use only the Python standard library. If the optional
'jsonschema' package is installed, each record is also checked against
schema.json (JSON Schema Draft 2020-12).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
INDEX_PATH = ROOT / "index.json"
SCHEMA_PATH = ROOT / "schema.json"

REQUIRED_FIELDS = {
    "id", "language", "category", "question", "answer", "keywords",
    "intent", "audience", "related_questions", "source_url",
    "last_updated", "review_status",
}
VALID_STATUSES = {"draft_review_required", "reviewed", "approved", "archived"}
VALID_AUDIENCES = {"bireysel", "kurumsal"}
ID_PATTERN = re.compile(r"^IKN-[A-Z0-9]+-[0-9]{3}$")
CATEGORY_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
errors: list[str] = []
warnings: list[str] = []


def load_json(path: Path):
    """Load UTF-8 JSON and report parse errors without a traceback."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: file not found")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: file is not valid UTF-8: {exc}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        )
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot read file: {exc}")
    return None


def is_nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_string_list(value, label: str, *, allow_empty: bool = True) -> bool:
    """Check an array of unique, non-empty strings; return whether it is valid."""
    if not isinstance(value, list):
        errors.append(f"{label}: must be an array")
        return False
    if not allow_empty and not value:
        errors.append(f"{label}: must contain at least one item")
    valid = True
    seen = set()
    for i, item in enumerate(value):
        item_label = f"{label}[{i}]"
        if not is_nonempty_string(item):
            errors.append(f"{item_label}: must be a non-empty string")
            valid = False
            continue
        normalized = " ".join(item.casefold().split())
        if normalized in seen:
            errors.append(f"{item_label}: duplicate item {item!r}")
            valid = False
        seen.add(normalized)
    return valid


def validate_record(record, label: str, expected_category: str | None = None):
    if not isinstance(record, dict):
        errors.append(f"{label}: record must be an object")
        return

    missing = REQUIRED_FIELDS - set(record)
    extra = set(record) - REQUIRED_FIELDS
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{label}: unknown fields: {', '.join(sorted(extra))}")

    for field in ("id", "language", "category", "question", "answer", "intent"):
        if field in record and not is_nonempty_string(record[field]):
            errors.append(f"{label}: {field} must be a non-empty string")

    rid = record.get("id")
    if is_nonempty_string(rid) and not ID_PATTERN.fullmatch(rid):
        errors.append(f"{label}: id must match IKN-<GROUP>-<3 digits> (got {rid!r})")

    if record.get("language") != "tr":
        errors.append(f"{label}: language must be 'tr'")

    category = record.get("category")
    if is_nonempty_string(category):
        if not CATEGORY_ID_PATTERN.fullmatch(category):
            errors.append(f"{label}: category must be a lowercase snake_case identifier")
        if expected_category and category != expected_category:
            errors.append(
                f"{label}: category {category!r} does not match index category {expected_category!r}"
            )

    question = record.get("question")
    if is_nonempty_string(question) and len(question.strip()) < 10:
        errors.append(f"{label}: question must be at least 10 characters")

    answer = record.get("answer")
    if is_nonempty_string(answer) and len(answer.strip()) < 80:
        errors.append(f"{label}: answer must be at least 80 characters")

    if "keywords" in record:
        check_string_list(record["keywords"], f"{label}.keywords", allow_empty=False)

    audience = record.get("audience")
    if not isinstance(audience, list) or not audience:
        errors.append(f"{label}: audience must be a non-empty array")
    else:
        if any(item not in VALID_AUDIENCES for item in audience):
            errors.append(
                f"{label}: audience values must be from {sorted(VALID_AUDIENCES)}"
            )
        if len(audience) != len(set(audience)):
            errors.append(f"{label}: audience contains duplicate values")

    if "related_questions" in record:
        related = record["related_questions"]
        if check_string_list(related, f"{label}.related_questions"):
            for i, item in enumerate(related):
                if len(item.strip()) < 10:
                    errors.append(
                        f"{label}.related_questions[{i}]: must be at least 10 characters"
                    )

    source_url = record.get("source_url")
    if source_url is not None:
        if not is_nonempty_string(source_url):
            errors.append(f"{label}: source_url must be a valid URL string or null")
        else:
            parsed = urlparse(source_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{label}: source_url must use http:// or https://")

    updated = record.get("last_updated")
    if not is_nonempty_string(updated):
        errors.append(f"{label}: last_updated must be a YYYY-MM-DD date")
    else:
        try:
            if date.fromisoformat(updated).isoformat() != updated:
                raise ValueError("date is not in YYYY-MM-DD form")
        except ValueError:
            errors.append(f"{label}: last_updated must be a valid YYYY-MM-DD date")

    if record.get("review_status") not in VALID_STATUSES:
        errors.append(
            f"{label}: review_status must be one of {sorted(VALID_STATUSES)}"
        )


def main() -> int:
    index = load_json(INDEX_PATH)
    schema = load_json(SCHEMA_PATH)

    if index is not None and not isinstance(index, dict):
        errors.append("index.json: top-level value must be an object")
        index = None
    if schema is not None and not isinstance(schema, dict):
        errors.append("schema.json: top-level value must be an object")
        schema = None

    categories = {}
    if index is not None:
        raw_categories = index.get("categories")
        if not isinstance(raw_categories, list):
            errors.append("index.json: categories must be an array")
            raw_categories = []
        seen_category_ids = set()
        seen_files = set()
        for i, category in enumerate(raw_categories):
            label = f"index.json.categories[{i}]"
            if not isinstance(category, dict):
                errors.append(f"{label}: category must be an object")
                continue
            cid = category.get("id")
            file_name = category.get("file")
            if not is_nonempty_string(cid) or not CATEGORY_ID_PATTERN.fullmatch(cid):
                errors.append(f"{label}.id: must be a lowercase snake_case identifier")
                continue
            if cid in seen_category_ids:
                errors.append(f"{label}: duplicate category id {cid!r}")
            seen_category_ids.add(cid)
            if not is_nonempty_string(file_name):
                errors.append(f"{label}.file: must be a non-empty relative path")
                continue
            file_path = Path(file_name)
            if file_path.is_absolute() or ".." in file_path.parts:
                errors.append(f"{label}.file: must stay inside the repository")
                continue
            if file_name in seen_files:
                errors.append(f"{label}: duplicate category file {file_name!r}")
            seen_files.add(file_name)
            planned = category.get("planned_count")
            current = category.get("current_count")
            if not isinstance(planned, int) or isinstance(planned, bool) or planned < 0:
                errors.append(f"{label}.planned_count: must be a non-negative integer")
            if not isinstance(current, int) or isinstance(current, bool) or current < 0:
                errors.append(f"{label}.current_count: must be a non-negative integer")
            status = category.get("status")
            if not is_nonempty_string(status):
                errors.append(f"{label}.status: must be a non-empty string")
            categories[cid] = category

        planned_total = index.get("planned_faq_count")
        declared_total = index.get("current_faq_count")
        if not isinstance(planned_total, int) or isinstance(planned_total, bool) or planned_total < 0:
            errors.append("index.json.planned_faq_count: must be a non-negative integer")
        if not isinstance(declared_total, int) or isinstance(declared_total, bool) or declared_total < 0:
            errors.append("index.json.current_faq_count: must be a non-negative integer")

        if isinstance(planned_total, int) and all(
            isinstance(c.get("planned_count"), int) and not isinstance(c.get("planned_count"), bool)
            for c in categories.values()
        ):
            category_planned = sum(c["planned_count"] for c in categories.values())
            if category_planned != planned_total:
                errors.append(
                    f"index.json: planned_faq_count is {planned_total}, "
                    f"but category totals add up to {category_planned}"
                )

    all_ids = {}
    all_questions = {}
    actual_counts = {}
    total_records = 0

    # Validate every JSON file in data/, including files not yet listed in index.json.
    if DATA_DIR.exists():
        data_files = sorted(DATA_DIR.glob("*.json"))
    else:
        errors.append("data/: directory not found")
        data_files = []

    indexed_files = {
        category.get("file"): category
        for category in categories.values()
        if is_nonempty_string(category.get("file"))
    }

    for path in data_files:
        relative = path.relative_to(ROOT).as_posix()
        records = load_json(path)
        if records is None:
            continue
        if not isinstance(records, list):
            errors.append(f"{relative}: top-level JSON must be an array")
            continue

        indexed_category = indexed_files.get(relative)
        if indexed_category is None:
            warnings.append(f"{relative}: file is not referenced by index.json")
        expected_category = indexed_category.get("id") if indexed_category else None
        actual_counts[relative] = len(records)
        total_records += len(records)

        for i, record in enumerate(records):
            label = f"{relative}[{i}]"
            validate_record(record, label, expected_category)
            if not isinstance(record, dict):
                continue

            rid = record.get("id")
            if is_nonempty_string(rid):
                if rid in all_ids:
                    errors.append(f"{label}: duplicate id {rid!r} (also in {all_ids[rid]})")
                else:
                    all_ids[rid] = label

            question = record.get("question")
            if is_nonempty_string(question):
                normalized = " ".join(question.casefold().split())
                if normalized in all_questions:
                    errors.append(
                        f"{label}: duplicate question (also in {all_questions[normalized]})"
                    )
                else:
                    all_questions[normalized] = label

    # Cross-check each index count and make sure indexed non-empty categories exist.
    for file_name, category in indexed_files.items():
        path = ROOT / file_name
        declared = category.get("current_count")
        actual = actual_counts.get(file_name)
        if actual is None:
            if isinstance(declared, int) and declared > 0:
                errors.append(
                    f"index.json: {file_name} declares {declared} records but the file is missing"
                )
            elif not path.exists():
                warnings.append(f"index.json: planned file not created yet: {file_name}")
        elif isinstance(declared, int) and not isinstance(declared, bool) and declared != actual:
            errors.append(
                f"index.json: {file_name} current_count is {declared}, actual count is {actual}"
            )

    if index is not None:
        declared_total = index.get("current_faq_count")
        if isinstance(declared_total, int) and not isinstance(declared_total, bool):
            if declared_total != total_records:
                errors.append(
                    f"index.json: current_faq_count is {declared_total}, "
                    f"but data files contain {total_records} records"
                )

    # Full Draft 2020-12 validation is enabled when jsonschema is installed.
    if schema is not None:
        try:
            from jsonschema import Draft202012Validator, FormatChecker
        except ImportError:
            warnings.append(
                "Optional JSON Schema validation skipped (install with: "
                "python3 -m pip install 'jsonschema[format]'). "
                "Built-in checks still ran."
            )
        else:
            try:
                Draft202012Validator.check_schema(schema)
                validator = Draft202012Validator(schema, format_checker=FormatChecker())
                for path in data_files:
                    records = load_json(path)
                    if not isinstance(records, list):
                        continue
                    for i, record in enumerate(records):
                        for issue in validator.iter_errors(record):
                            location = ".".join(str(part) for part in issue.absolute_path)
                            suffix = f".{location}" if location else ""
                            errors.append(
                                f"{path.relative_to(ROOT).as_posix()}[{i}]{suffix}: "
                                f"schema validation: {issue.message}"
                            )
            except Exception as exc:
                errors.append(f"schema.json: could not validate schema/data: {exc}")

    print(f"Checked {total_records} FAQ record(s) across {len(data_files)} data file(s).")
    print(f"Found {len(categories)} indexed category/categories.")
    if warnings:
        print(f"Warnings: {len(warnings)}")
        for warning in warnings:
            print(f"- WARNING: {warning}")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors:
            print(f"- ERROR: {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
