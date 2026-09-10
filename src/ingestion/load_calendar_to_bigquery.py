from pathlib import Path

from google.cloud import bigquery


PROJECT_ID = "retail-demand-forecasting-2026"
DATASET_ID = "retail_demand"
TABLE_ID = "calendar"

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "raw" / "calendar.csv"


def main():
    client = bigquery.Client(project=PROJECT_ID)

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(f"Loading: {CSV_FILE}")
    print(f"Destination: {table_ref}")

    with open(CSV_FILE, "rb") as source_file:
        load_job = client.load_table_from_file(
            source_file,
            table_ref,
            job_config=job_config,
        )

    load_job.result()

    table = client.get_table(table_ref)

    print("Calendar table loaded successfully.")
    print(f"Rows: {table.num_rows}")
    print(f"Columns: {len(table.schema)}")


if __name__ == "__main__":
    main()