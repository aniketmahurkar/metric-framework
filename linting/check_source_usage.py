#!/usr/bin/env python3
"""Ensures marts models use ref() not source() — marts should reference staging/intermediate."""
import re
import sys
from pathlib import Path

def check_source_usage(project_root: str) -> list[str]:
    errors = []
    marts_path = Path(project_root) / "models" / "marts"
    if not marts_path.exists():
        return errors

    source_pattern = re.compile(r"{{\s*source\(")

    for sql_file in marts_path.rglob("*.sql"):
        content = sql_file.read_text()
        if source_pattern.search(content):
            errors.append(f"{sql_file.name}: marts model uses source() directly")
    return errors

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    errors = check_source_usage(root)
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1 if errors else 0)
