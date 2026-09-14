from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from google.cloud import bigquery
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor


PROJECT_ID = "retail-demand-forecasting-2026"
DATASET = "retail_demand"

TRAIN_TABLE = f"{PROJECT_ID}.{DATASET}.forecasting_train"
VALIDATION_TABLE = f"{PROJECT_ID}.{DATASET}.forecasting_validation"

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "baseline_random_forest.joblib"
PREDICTIONS_PATH = MODEL_DIR / "baseline_predictions.csv"
METRICS_PATH = MODEL_DIR / "baseline_metrics.csv"


FEATURES = [
    "avg_sell_price",
    "item_count",
    "priced_item_rows",
    "item_rows",
    "day_of_week",
    "day_of_month",
    "month",
    "year",
    "is_weekend",
    "sales_lag_1",
    "sales_lag_7",
    "sales_lag_28",
    "sales_rolling_7d",
    "sales_rolling_28d",
]

TARGET = "total_sales"

ID_COLUMNS = [
    "store_id",
    "dept_id",
    "state_id",
]


def load_data(client, table):
    query = f"""
        SELECT
            date,
            store_id,
            state_id,
            dept_id,
            {", ".join(FEATURES)},
            {TARGET}
        FROM `{table}`
        ORDER BY date, store_id, dept_id
    """

    print(f"Loading data from: {table}")
    df = client.query(query).to_dataframe()

    print(f"Rows loaded: {len(df):,}")

    return df


def create_category_mappings(train):
    mappings = {}

    for column in ID_COLUMNS:
        categories = sorted(train[column].dropna().unique())

        mappings[column] = {
            value: index
            for index, value in enumerate(categories)
        }

    return mappings


def apply_category_mappings(df, mappings):
    df = df.copy()

    for column in ID_COLUMNS:
        df[f"{column}_code"] = (
            df[column]
            .map(mappings[column])
            .astype("float")
        )

    return df


def prepare_data(df):
    df = df.copy()

    model_features = FEATURES + [
        "store_id_code",
        "dept_id_code",
        "state_id_code",
    ]

    # Remove rows where model features or target are unavailable.
    df = df.dropna(subset=model_features + [TARGET])

    return df, model_features


def calculate_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)

    rmse = np.sqrt(
        mean_squared_error(y_true, y_pred)
    )

    # Avoid division by zero for MAPE.
    mask = y_true != 0

    if mask.sum() > 0:
        mape = (
            np.mean(
                np.abs(
                    (y_true[mask] - y_pred[mask])
                    / y_true[mask]
                )
            )
            * 100
        )
    else:
        mape = np.nan

    return mae, rmse, mape


def main():

    print("=" * 60)
    print("RETAIL DEMAND FORECASTING - BASELINE MODEL")
    print("=" * 60)

    client = bigquery.Client(project=PROJECT_ID)

    # ---------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------

    train = load_data(client, TRAIN_TABLE)
    validation = load_data(client, VALIDATION_TABLE)

    # ---------------------------------------------------------
    # 2. Create category mappings using TRAINING data only
    # ---------------------------------------------------------

    print("\nCreating category mappings...")

    mappings = create_category_mappings(train)

    # Apply the SAME mappings to both datasets.
    train = apply_category_mappings(train, mappings)
    validation = apply_category_mappings(validation, mappings)

    # ---------------------------------------------------------
    # 3. Prepare data
    # ---------------------------------------------------------

    print("\nPreparing data...")

    train, model_features = prepare_data(train)
    validation, _ = prepare_data(validation)

    print(
        f"Training rows after cleaning: "
        f"{len(train):,}"
    )

    print(
        f"Validation rows after cleaning: "
        f"{len(validation):,}"
    )

    # ---------------------------------------------------------
    # 4. Train model
    # ---------------------------------------------------------

    X_train = train[model_features]
    y_train = train[TARGET]

    X_validation = validation[model_features]
    y_validation = validation[TARGET]

    print("\nTraining Random Forest model...")

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    print("Model training complete.")

    # ---------------------------------------------------------
    # 5. Validation predictions
    # ---------------------------------------------------------

    print("\nGenerating validation predictions...")

    predictions = model.predict(X_validation)

    mae, rmse, mape = calculate_metrics(
        y_validation,
        predictions,
    )

    # ---------------------------------------------------------
    # 6. Display metrics
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"MAE  : {mae:,.2f}")
    print(f"RMSE : {rmse:,.2f}")
    print(f"MAPE : {mape:.2f}%")

    # ---------------------------------------------------------
    # 7. Feature importance
    # ---------------------------------------------------------

    importance = pd.DataFrame(
        {
            "feature": model_features,
            "importance": model.feature_importances_,
        }
    ).sort_values(
        "importance",
        ascending=False,
    )

    print("\nTop Feature Importances:")
    print(
        importance.head(10).to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # 8. Save model + mappings
    # ---------------------------------------------------------

    joblib.dump(
        {
            "model": model,
            "features": model_features,
            "category_mappings": mappings,
        },
        MODEL_PATH,
    )

    print(
        f"\nModel saved to: {MODEL_PATH}"
    )

    # ---------------------------------------------------------
    # 9. Save predictions
    # ---------------------------------------------------------

    results = validation[
        [
            "date",
            "store_id",
            "state_id",
            "dept_id",
            TARGET,
        ]
    ].copy()

    results["predicted_sales"] = predictions

    results["absolute_error"] = (
        results[TARGET]
        - results["predicted_sales"]
    ).abs()

    results.to_csv(
        PREDICTIONS_PATH,
        index=False,
    )

    print(
        f"Predictions saved to: "
        f"{PREDICTIONS_PATH}"
    )

    # ---------------------------------------------------------
    # 10. Save metrics
    # ---------------------------------------------------------

    metrics = pd.DataFrame(
        [
            {
                "model": "Random Forest Baseline",
                "mae": mae,
                "rmse": rmse,
                "mape": mape,
                "training_rows": len(train),
                "validation_rows": len(validation),
            }
        ]
    )

    metrics.to_csv(
        METRICS_PATH,
        index=False,
    )

    print(
        f"Metrics saved to: "
        f"{METRICS_PATH}"
    )

    # ---------------------------------------------------------
    # 11. Show predictions
    # ---------------------------------------------------------

    print("\nFirst 10 predictions:")

    print(
        results.head(10).to_string(
            index=False
        )
    )

    print("\nBaseline model completed successfully.")


if __name__ == "__main__":
    main()
