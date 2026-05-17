#!/usr/bin/env python3
"""Ensures intermediate models do not reference marts models (wrong layer direction)."""
import re
import sys
from pathlib import Path

def check_layer_direction(project_root: str) -> list[str]:
    errors = []
    intermediate_path = Path(project_root) / "models" / "intermediate"
    if not intermediate_path.exists():
        return errors

    ref_pattern = re.compile(r"{{\s*ref\(['\"](\w+)['\"]\)\s*}}")

    for sql_file in intermediate_path.rglob("*.sql"):
        content = sql_file.read_text()
        refs = ref_pattern.findall(content)
        for ref_name in refs:
            if ref_name.startswith("mart_") or ref_name.startswith("fct_") or ref_name.startswith("dim_"):
                errors.append(f"{sql_file.name}: intermediate model refs marts model '{ref_name}'")
    return errors

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    errors = check_layer_direction(root)
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1 if errors else 0)
