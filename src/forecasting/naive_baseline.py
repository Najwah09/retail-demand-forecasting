from pathlib import Path

import numpy as np
import pandas as pd
from google.cloud import bigquery
from sklearn.metrics import mean_absolute_error, mean_squared_error


PROJECT_ID = "retail-demand-forecasting-2026"
DATASET = "retail_demand"

VALIDATION_TABLE = (
    f"{PROJECT_ID}.{DATASET}.forecasting_validation"
)

OUTPUT_PATH = Path("models") / "naive_baseline_metrics.csv"


def main():

    print("=" * 60)
    print("RETAIL DEMAND FORECASTING - NAIVE BASELINE")
    print("=" * 60)

    client = bigquery.Client(
        project=PROJECT_ID
    )

    query = f"""
        SELECT
            date,
            store_id,
            dept_id,
            total_sales,
            sales_lag_7
        FROM `{VALIDATION_TABLE}`
        WHERE sales_lag_7 IS NOT NULL
        ORDER BY date, store_id, dept_id
    """

    print("\nLoading validation data...")

    df = client.query(
        query
    ).to_dataframe()

    print(
        f"Validation rows: {len(df):,}"
    )

    y_true = df["total_sales"]
    y_pred = df["sales_lag_7"]

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    mask = y_true != 0

    mape = (
        np.mean(
            np.abs(
                (
                    y_true[mask]
                    - y_pred[mask]
                )
                / y_true[mask]
            )
        )
        * 100
    )

    print("\n" + "=" * 60)
    print("NAIVE BASELINE PERFORMANCE")
    print("=" * 60)

    print(f"MAE  : {mae:,.2f}")
    print(f"RMSE : {rmse:,.2f}")
    print(f"MAPE : {mape:.2f}%")

    metrics = pd.DataFrame(
        [
            {
                "model": "Naive Lag-7",
                "mae": mae,
                "rmse": rmse,
                "mape": mape,
                "validation_rows": len(df),
            }
        ]
    )

    metrics.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nMetrics saved to: {OUTPUT_PATH}"
    )

    print("\nFirst 10 predictions:")

    preview = df[
        [
            "date",
            "store_id",
            "dept_id",
            "total_sales",
            "sales_lag_7",
        ]
    ].head(10)

    print(
        preview.to_string(
            index=False
        )
    )

    print(
        "\nNaive baseline completed successfully."
    )


if __name__ == "__main__":
    main()