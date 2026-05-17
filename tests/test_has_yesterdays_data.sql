{% test has_yesterdays_data(model, date_column) %}
/*
  Fails if the most recent date in the table is older than yesterday.
  Usage in schema.yml:
    tests:
      - has_yesterdays_data:
          date_column: event_date
*/
select
    max({{ date_column }}) as max_date
from {{ model }}
having max({{ date_column }}) < current_date - interval '1 day'
{% endtest %}
