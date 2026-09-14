CREATE OR REPLACE TABLE `retail-demand-forecasting-2026.retail_demand.sales_daily` AS
SELECT
  id,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  d,
  sales
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_validation`
UNPIVOT(
  sales FOR d IN (
    d_1, d_2, d_3, d_4, d_5,
    d_6, d_7, d_8, d_9, d_10
  )
);