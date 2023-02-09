CREATE OR REPLACE EXTERNAL TABLE `dataset.ext03`
OPTIONS (
  format = 'CSV',
  compression='GZIP',
  uris = ['gs://prefect-dez-bucket/fhv_tripdata_2019-03.csv.gz']
);

SELECT COUNT (DISTINCT Affiliated_base_number)
FROM dataset.ext03;

CREATE OR REPLACE TABLE dataset.nonp03 AS
SELECT * FROM dataset.ext03;

SELECT COUNT (DISTINCT Affiliated_base_number)
FROM dataset.*;

SELECT DISTINCT(Affiliated_base_number)
FROM dataset.nonp03
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

CREATE OR REPLACE TABLE dataset.pc03
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM dataset.nonp03;

SELECT DISTINCT(Affiliated_base_number)
FROM dataset.pc03
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';