{% test metric_accuracy(model, metric_column, expected_value, tolerance=0.01) %}
/*
  Compares a computed metric to an expected value within a tolerance (proportion).
  Useful for validating that a KPI matches a known-good source (e.g., Tableau dashboard).
*/
select
    {{ metric_column }} as actual_value,
    {{ expected_value }} as expected_value,
    abs({{ metric_column }} - {{ expected_value }}) / nullif(abs({{ expected_value }}), 0) as pct_diff
from {{ model }}
where abs({{ metric_column }} - {{ expected_value }}) / nullif(abs({{ expected_value }}), 0) > {{ tolerance }}
{% endtest %}
