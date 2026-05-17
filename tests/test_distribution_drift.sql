{% test distribution_drift(model, metric_column, date_column, lookback_days=30, threshold_std=2) %}
/*
  Compares today's metric distribution to a baseline (last N days).
  Alerts if the current mean deviates by more than threshold_std standard deviations.
*/
with baseline as (
    select
        avg({{ metric_column }}) as baseline_mean,
        stddev({{ metric_column }}) as baseline_stddev
    from {{ model }}
    where {{ date_column }} >= current_date - interval '{{ lookback_days }} days'
      and {{ date_column }} < current_date
),
current_period as (
    select
        avg({{ metric_column }}) as current_mean
    from {{ model }}
    where {{ date_column }} = current_date
)
select
    current_period.current_mean,
    baseline.baseline_mean,
    baseline.baseline_stddev
from current_period
cross join baseline
where abs(current_period.current_mean - baseline.baseline_mean) 
      > ({{ threshold_std }} * baseline.baseline_stddev)
  and baseline.baseline_stddev > 0
{% endtest %}
