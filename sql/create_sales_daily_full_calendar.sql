CREATE OR REPLACE TABLE `retail-demand-forecasting-2026.retail_demand.sales_daily_full_calendar` AS
SELECT
  s.id,
  s.item_id,
  s.dept_id,
  s.cat_id,
  s.store_id,
  s.state_id,
  s.d,
  c.date,
  c.wm_yr_wk,
  s.sales
FROM `retail-demand-forecasting-2026.retail_demand.sales_daily_full` AS s
LEFT JOIN `retail-demand-forecasting-2026.retail_demand.calendar` AS c
  ON s.d = c.d;