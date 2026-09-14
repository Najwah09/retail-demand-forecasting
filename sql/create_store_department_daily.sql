CREATE OR REPLACE TABLE
`retail-demand-forecasting-2026.retail_demand.store_department_daily`
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
  item_rows
FROM
`retail-demand-forecasting-2026.retail_demand.store_department_test`;