#!/usr/bin/env python3
"""Validates KPI definition files against the schema and checks for common errors."""
import sys
from pathlib import Path
import yaml

REQUIRED_FIELDS = ["name", "code", "formula", "source_table", "date_field"]
VALID_OPERATORS = ["=", "!=", ">", "<", ">=", "<=", "in", "not_in", "is_null", "is_not_null"]
VALID_GRAINS = ["daily", "weekly", "monthly"]

# Tolerance bands per metric type for validation
TOLERANCE_BANDS = {
    "percentage": 0.02,    # ±2 percentage points
    "score": 0.05,         # ±0.05 absolute
    "count": 0.05,         # ±5% relative
    "duration": 0.05,      # ±5% relative
    "rate": 0.02,          # ±2 percentage points
}


def validate_kpi(kpi: dict, filename: str) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if not kpi.get(field):
            errors.append(f"{filename}: missing required field '{field}'")

    if kpi.get("grain") and kpi["grain"] not in VALID_GRAINS:
        errors.append(f"{filename}: invalid grain '{kpi['grain']}' (must be {VALID_GRAINS})")

    for f in kpi.get("filters", []):
        if f.get("operator") and f["operator"] not in VALID_OPERATORS:
            errors.append(f"{filename}: invalid filter operator '{f['operator']}'")

    agg = kpi.get("aggregation", {})
    if agg and not agg.get("first_level"):
        errors.append(f"{filename}: aggregation defined but missing 'first_level' (LOD pattern)")

    return errors


def validate_all(kpi_dir: str) -> list[str]:
    errors = []
    kpi_path = Path(kpi_dir)
    yml_files = [f for f in kpi_path.rglob("*.yml") if f.name != "kpi_schema.yml"]

    if not yml_files:
        errors.append(f"No KPI definition files found in {kpi_dir}")
        return errors

    codes_seen = set()
    for yml_file in yml_files:
        try:
            data = yaml.safe_load(yml_file.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{yml_file.name}: invalid YAML: {e}")
            continue

        if not data or "kpi" not in data:
            errors.append(f"{yml_file.name}: missing top-level 'kpi' key")
            continue

        kpi = data["kpi"]
        errors.extend(validate_kpi(kpi, yml_file.name))

        code = kpi.get("code", "")
        if code in codes_seen:
            errors.append(f"{yml_file.name}: duplicate KPI code '{code}'")
        codes_seen.add(code)

    return errors


if __name__ == "__main__":
    kpi_dir = sys.argv[1] if len(sys.argv) > 1 else "kpi_definitions"
    errors = validate_all(kpi_dir)
    for e in errors:
        print(f"ERROR: {e}")
    if not errors:
        print(f"✓ All KPI definitions valid ({kpi_dir})")
    sys.exit(1 if errors else 0)
