from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    gcs_path = Path(f"data/{color}/{dataset_file}.parquet")
    gcs_block = GcsBucket.load("de-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./")
    return Path(f"{gcs_path}")


@task()
def extract_from_file(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame, table_name) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("de-gcp-creds")

    df.to_gbq(
        destination_table=f"dezoomcamp.{table_name}",
        project_id="endless-bonus-375606",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(color: str, year: int, month):
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    df = extract_from_file(path)
    table_name = f"{color}_tripdata_{year}-{month:02}"

    write_bq(df, table_name)

    return len(df)


@flow(log_prints=True)
def etl_to_bq_parent_flow(months: list[int], year: int, color: str):
    total_rows = 0
    
    for month in months:
        total_rows += etl_gcs_to_bq(color, year, month)
    
    print(f"total loaded rows: {total_rows}")

if __name__ == "__main__":
    color = "yellow"
    year = 2019
    months = [ 2, 3 ]

    etl_to_bq_parent_flow(months, year, color)