#!/usr/bin/env python3
"""Enforces that at least 60% of columns in schema.yml have descriptions."""
import sys
from pathlib import Path
import yaml

THRESHOLD = 0.6

def check_column_descriptions(project_root: str, threshold: float = THRESHOLD) -> list[str]:
    warnings = []
    models_path = Path(project_root) / "models"
    if not models_path.exists():
        return warnings

    for yml_file in models_path.rglob("*.yml"):
        try:
            data = yaml.safe_load(yml_file.read_text())
        except Exception:
            continue
        if not data or "models" not in data:
            continue
        for model in data["models"]:
            columns = model.get("columns", [])
            if not columns:
                continue
            described = sum(1 for c in columns if c.get("description"))
            ratio = described / len(columns)
            if ratio < threshold:
                warnings.append(
                    f"{yml_file.name} → {model['name']}: "
                    f"{described}/{len(columns)} columns described ({ratio:.0%} < {threshold:.0%})"
                )
    return warnings

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    warnings = check_column_descriptions(root)
    for w in warnings:
        print(f"WARNING: {w}")
    sys.exit(1 if warnings else 0)
