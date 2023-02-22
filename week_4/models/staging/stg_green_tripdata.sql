{{ config(materialized='view') }}

select * from {{ source("staging", "green_trips_all") }} LIMIT 100