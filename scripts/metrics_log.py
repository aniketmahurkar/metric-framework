#!/usr/bin/env python3
"""Tracks KPI validation runs in a JSONL log for cross-run meta-analysis.

Each run appends a structured entry enabling:
- Trend detection across validation runs
- Recurring failure identification
- Drift monitoring over time
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("metrics_log.jsonl")


def log_run(kpi_dir: str, results: dict):
    """Append a validation run entry to the metrics log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kpi_dir": kpi_dir,
        "kpis_validated": results.get("total", 0),
        "errors": results.get("errors", 0),
        "warnings": results.get("warnings", 0),
        "failed_kpis": results.get("failed_kpis", []),
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def analyze_log(min_consecutive: int = 3) -> list[str]:
    """Find KPIs that have failed N+ consecutive runs (recurring flags)."""
    if not LOG_PATH.exists():
        return []

    entries = [json.loads(line) for line in LOG_PATH.read_text().splitlines() if line.strip()]
    if not entries:
        return []

    # Track consecutive failures per KPI
    streak: dict[str, int] = {}
    alerts = []

    for entry in entries:
        failed = set(entry.get("failed_kpis", []))
        for kpi in list(streak.keys()):
            if kpi in failed:
                streak[kpi] += 1
            else:
                streak.pop(kpi)
        for kpi in failed:
            if kpi not in streak:
                streak[kpi] = 1

    for kpi, count in streak.items():
        if count >= min_consecutive:
            alerts.append(f"{kpi}: failed {count} consecutive runs")

    return alerts


if __name__ == "__main__":
    alerts = analyze_log()
    if alerts:
        print("⚠️  Recurring failures detected:")
        for a in alerts:
            print(f"  - {a}")
    else:
        print("✓ No recurring failures in metrics log")
