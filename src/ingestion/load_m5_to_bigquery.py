from pathlib import Path

from google.cloud import bigquery


PROJECT_ID = "retail-demand-forecasting-2026"
DATASET_ID = "retail_demand"

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


def main():
    client = bigquery.Client(project=PROJECT_ID)

    print(f"Connected to BigQuery project: {PROJECT_ID}")
    print(f"Raw data folder: {RAW_DIR}")

    files = list(RAW_DIR.glob("*.csv"))

    print(f"Found {len(files)} CSV files:")

    for file in files:
        print(f" - {file.name}")


if __name__ == "__main__":
    main()