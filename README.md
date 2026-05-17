# metric-framework

**Why your SQL doesn't match Tableau — and how to fix it.**

An open-source dbt package that gives analytics teams certified metric governance out of the box: KPI calculation templates, automated data quality macros, CI/CD linting rules, and a metric dictionary generator.

## The Problem

You write a SQL query. Tableau shows a different number. Why?

1. **LOD aggregation mismatch** — You averaged all rows. Tableau averaged per-customer first, then averaged those averages.
2. **Missing exclusion filters** — Null scores, zero-duration contacts, test accounts.
3. **Wrong date field** — `survey_date` vs `interaction_date` vs `created_at`.

This package encodes those rules so your team gets it right every time.

## Quick Start

Add to your `packages.yml`:

```yaml
packages:
  - git: "https://github.com/aniketmahurkar/metric-framework.git"
    revision: v0.1.0
```

Then run:

```bash
dbt deps
```

## Features

### 1. Data Quality Tests

Add to your `schema.yml`:

```yaml
models:
  - name: fct_contacts
    tests:
      - has_yesterdays_data:
          date_column: contact_date
      - distribution_drift:
          metric_column: handle_time_seconds
          date_column: contact_date
      - anomaly_zscore:
          metric_column: handle_time_seconds
          date_column: contact_date
          z_threshold: 3
```

| Test | What it does |
|------|-------------|
| `has_yesterdays_data` | Fails if max date < yesterday (freshness) |
| `distribution_drift` | Alerts if current mean deviates >2σ from 30-day baseline |
| `anomaly_zscore` | Flags values with z-score > 3 against rolling window |
| `metric_accuracy` | Compares computed metric to expected value within tolerance |

### 2. KPI Definitions

Define your metrics in YAML with the two-step LOD pattern:

```yaml
kpi:
  name: "Customer Effort Score"
  code: "CES"
  formula: "AVG(effort_score)"
  source_table: "surveys"
  date_field: "survey_date"
  aggregation:
    first_level: "AVG per contact_id"
    second_level: "AVG of daily averages"
  filters:
    - column: "survey_type"
      operator: "="
      value: "post_interaction"
```

### 3. CI/CD Linting

Run in your CI pipeline:

```bash
python linting/check_layer_direction.py .
python linting/check_source_usage.py .
python linting/check_model_length.py . 200
python linting/check_column_descriptions.py .
```

| Rule | What it catches |
|------|----------------|
| `check_layer_direction` | Intermediate models referencing marts |
| `check_source_usage` | Marts using `source()` instead of `ref()` |
| `check_model_length` | Models exceeding N lines |
| `check_column_descriptions` | Schema files with <60% described columns |

### 4. Metric Dictionary Generator

```bash
python scripts/generate_dictionary.py kpi_definitions/ > METRIC_DICTIONARY.md
```

Generates a formatted markdown dictionary from all your KPI YAML files.

## Architecture: The LOD Pattern

Most KPI mismatches come from aggregation order. The correct pattern:

```
Step 1: Compute metric per entity (contact, customer, session)
Step 2: Aggregate Step 1 results over time period
```

**Wrong:** `SELECT AVG(score) FROM surveys WHERE date = '2024-01-01'`

**Right:**
```sql
WITH per_contact AS (
    SELECT contact_id, AVG(score) as contact_score
    FROM surveys
    WHERE date = '2024-01-01'
    GROUP BY contact_id
)
SELECT AVG(contact_score) FROM per_contact
```

This package's KPI schema enforces documenting both levels.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
