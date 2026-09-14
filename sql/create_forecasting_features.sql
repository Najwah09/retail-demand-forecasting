CREATE OR REPLACE TABLE
`retail-demand-forecasting-2026.retail_demand.forecasting_features`
AS

SELECT
  date,
  store_id,
  state_id,
  dept_id,

  total_sales,
  avg_sell_price,
  item_count,
  priced_item_rows,
  item_rows,

  -- Calendar features
  EXTRACT(DAYOFWEEK FROM date) AS day_of_week,
  EXTRACT(DAY FROM date) AS day_of_month,
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(YEAR FROM date) AS year,

  CASE
    WHEN EXTRACT(DAYOFWEEK FROM date) IN (1, 7)
    THEN 1
    ELSE 0
  END AS is_weekend,

  -- Lag features
  LAG(total_sales, 1) OVER (
    PARTITION BY store_id, dept_id
    ORDER BY date
  ) AS sales_lag_1,

  LAG(total_sales, 7) OVER (
    PARTITION BY store_id, dept_id
    ORDER BY date
  ) AS sales_lag_7,

  LAG(total_sales, 28) OVER (
    PARTITION BY store_id, dept_id
    ORDER BY date
  ) AS sales_lag_28,

  -- Rolling averages
  AVG(total_sales) OVER (
    PARTITION BY store_id, dept_id
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS sales_rolling_7d,

  AVG(total_sales) OVER (
    PARTITION BY store_id, dept_id
    ORDER BY date
    ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
  ) AS sales_rolling_28d

FROM
`retail-demand-forecasting-2026.retail_demand.store_department_daily`;