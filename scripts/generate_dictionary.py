#!/usr/bin/env python3
"""Reads all kpi_definitions/*.yml files and generates a formatted markdown dictionary."""
import sys
from pathlib import Path
import yaml

def generate_dictionary(kpi_dir: str) -> str:
    kpi_path = Path(kpi_dir)
    yml_files = sorted(kpi_path.rglob("*.yml"))
    yml_files = [f for f in yml_files if f.name != "kpi_schema.yml"]

    lines = ["# Metric Dictionary", "", "Auto-generated from KPI definition files.", ""]

    for yml_file in yml_files:
        try:
            data = yaml.safe_load(yml_file.read_text())
        except Exception:
            continue
        if not data or "kpi" not in data:
            continue

        kpi = data["kpi"]
        lines.append(f"## {kpi.get('name', 'Unknown')} ({kpi.get('code', '')})")
        lines.append("")
        lines.append(f"**Description:** {kpi.get('description', 'N/A')}")
        lines.append("")
        lines.append(f"**Formula:** `{kpi.get('formula', 'N/A')}`")
        lines.append("")
        lines.append(f"**Source Table:** `{kpi.get('source_table', 'N/A')}`")
        lines.append(f"**Date Field:** `{kpi.get('date_field', 'N/A')}`")
        lines.append(f"**Grain:** {kpi.get('grain', 'N/A')}")
        lines.append("")

        agg = kpi.get("aggregation", {})
        if agg:
            lines.append("**Aggregation Pattern:**")
            lines.append(f"- First level: {agg.get('first_level', 'N/A')}")
            lines.append(f"- Second level: {agg.get('second_level', 'N/A')}")
            lines.append("")

        filters = kpi.get("filters", [])
        if filters:
            lines.append("**Filters:**")
            for f in filters:
                lines.append(f"- `{f.get('column', '')}` {f.get('operator', '')} `{f.get('value', '')}`")
            lines.append("")

        gotchas = kpi.get("gotchas", [])
        if gotchas:
            lines.append("**⚠️ Gotchas:**")
            for g in gotchas:
                lines.append(f"- {g}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    kpi_dir = sys.argv[1] if len(sys.argv) > 1 else "kpi_definitions"
    output = generate_dictionary(kpi_dir)
    print(output)
