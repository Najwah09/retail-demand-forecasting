\# Retail Demand Forecasting \& Inventory Optimization



An end-to-end retail analytics platform for demand forecasting and inventory optimization using the M5 Walmart historical sales dataset.



\## Project Objective



The project forecasts future retail demand at store and department levels and supports data-driven inventory replenishment and restocking decisions.



\## Tech Stack



\* Python

\* SQL

\* Google BigQuery

\* dbt

\* Scikit-learn

\* Random Forest

\* Prophet / ARIMA / LightGBM

\* Streamlit

\* Git \& GitHub



\## Project Architecture



M5 Dataset → Python ETL → BigQuery → Feature Engineering → Forecasting → Inventory Optimization → Streamlit Dashboard



\## Data Pipeline



The current pipeline includes:



1\. M5 historical sales data ingestion

2\. Daily store-department sales aggregation

3\. Calendar and pricing integration

4\. Forecasting feature engineering

5\. Time-based train/validation split

6\. Baseline demand forecasting models

7\. Model performance evaluation



\## Forecasting Dataset



The forecasting feature table contains store-department level daily observations with:



\* Total sales

\* Average selling price

\* Item counts

\* Calendar features

\* 1-day sales lag

\* 7-day sales lag

\* 28-day sales lag

\* 7-day rolling sales

\* 28-day rolling sales



\### Train / Validation Split



| Dataset    |    Rows |  Days | Date Range              |

| ---------- | ------: | ----: | ----------------------- |

| Training   | 128,030 | 1,829 | 2011-01-29 → 2016-01-31 |

| Validation |   5,880 |    84 | 2016-02-01 → 2016-04-24 |



\## Baseline Models



Two forecasting baselines have been implemented.



\### Naive Baseline



The naive model uses sales from the same store and department seven days earlier as the prediction.



| Metric | Result |

| ------ | -----: |

| MAE    |  88.44 |

| RMSE   | 160.79 |

| MAPE   | 21.48% |



\### Random Forest Baseline



A Random Forest regression model uses historical sales, rolling statistics, pricing, calendar variables, and store/department identifiers.



| Metric |     Result |

| ------ | ---------: |

| MAE    |  \*\*54.62\*\* |

| RMSE   |  \*\*95.39\*\* |

| MAPE   | \*\*14.12%\*\* |



The Random Forest baseline substantially outperformed the naive weekly-lag baseline on the validation period.



\### Important Features



The strongest model features were:



1\. `sales\_rolling\_7d` — 82.67%

2\. `sales\_lag\_28` — 12.22%

3\. `sales\_lag\_7` — 2.22%

4\. `sales\_lag\_1` — 0.93%



This indicates that recent sales trends and historical seasonal demand are highly important for forecasting store-department demand.



\## Project Structure



```text

retail-demand-forecasting/

│

├── dashboard/

├── data/

│   ├── raw/

│   └── processed/

│

├── dbt/

├── models/

├── notebooks/

├── sql/

│

├── src/

│   ├── forecasting/

│   │   ├── baseline\_model.py

│   │   └── naive\_baseline.py

│   │

│   ├── ingestion/

│   └── transformation/

│

├── tests/

├── .gitignore

├── README.md

├── requirements.txt

└── requirements.txt

```



\## Project Status



🚀 In Development



\### Completed



\* BigQuery project and dataset setup

\* Sales aggregation pipeline

\* Calendar and pricing integration

\* Forecasting feature engineering

\* Train/validation dataset creation

\* Naive baseline model

\* Random Forest baseline model

\* Model evaluation using MAE, RMSE and MAPE



\### Next Steps



\* Improve forecasting models

\* Test LightGBM / time-series approaches

\* Hyperparameter tuning

\* Forecast future demand

\* Develop inventory optimization logic

\* Generate replenishment recommendations

\* Build Streamlit forecasting dashboard

\* Add automated pipeline execution



