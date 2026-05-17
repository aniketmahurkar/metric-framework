{% test anomaly_zscore(model, metric_column, date_column, window_days=30, z_threshold=3) %}
/*
  Flags metric values where the z-score exceeds threshold against a rolling window.
  Returns rows that are anomalous.
*/
with stats as (
    select
        avg({{ metric_column }}) as rolling_mean,
        stddev({{ metric_column }}) as rolling_stddev
    from {{ model }}
    where {{ date_column }} >= current_date - interval '{{ window_days }} days'
      and {{ date_column }} < current_date
),
latest as (
    select {{ metric_column }} as metric_value
    from {{ model }}
    where {{ date_column }} = current_date
)
select
    latest.metric_value,
    stats.rolling_mean,
    stats.rolling_stddev,
    (latest.metric_value - stats.rolling_mean) / nullif(stats.rolling_stddev, 0) as z_score
from latest
cross join stats
where abs((latest.metric_value - stats.rolling_mean) / nullif(stats.rolling_stddev, 0)) > {{ z_threshold }}
{% endtest %}
