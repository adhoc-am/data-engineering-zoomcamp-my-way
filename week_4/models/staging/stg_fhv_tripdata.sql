{{ config(materialized='view') }}

select * from {{ source('staging','fhv_trips_all') }}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}