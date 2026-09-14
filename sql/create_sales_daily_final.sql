CREATE OR REPLACE TABLE `retail-demand-forecasting-2026.retail_demand.sales_daily_final` AS
SELECT
  id,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  d,
  date,
  wm_yr_wk,
  sales,
  sell_price,
  CASE
    WHEN sell_price IS NULL THEN FALSE
    ELSE TRUE
  END AS has_price
FROM `retail-demand-forecasting-2026.retail_demand.sales_daily_enriched`;