#!/usr/bin/env python3
"""Warns if any SQL model exceeds a configurable line limit."""
import sys
from pathlib import Path

MAX_LINES = 200

def check_model_length(project_root: str, max_lines: int = MAX_LINES) -> list[str]:
    warnings = []
    models_path = Path(project_root) / "models"
    if not models_path.exists():
        return warnings

    for sql_file in models_path.rglob("*.sql"):
        line_count = len(sql_file.read_text().splitlines())
        if line_count > max_lines:
            warnings.append(f"{sql_file.name}: {line_count} lines (max {max_lines})")
    return warnings

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    max_l = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_LINES
    warnings = check_model_length(root, max_l)
    for w in warnings:
        print(f"WARNING: {w}")
    sys.exit(1 if warnings else 0)
