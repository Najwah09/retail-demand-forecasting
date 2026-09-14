CREATE OR REPLACE TABLE `retail-demand-forecasting-2026.retail_demand.sales_daily_enriched` AS
SELECT
  s.id,
  s.item_id,
  s.dept_id,
  s.cat_id,
  s.store_id,
  s.state_id,
  s.d,
  s.date,
  s.wm_yr_wk,
  s.sales,
  p.sell_price
FROM `retail-demand-forecasting-2026.retail_demand.sales_daily_calendar` AS s
LEFT JOIN `retail-demand-forecasting-2026.retail_demand.sell_prices` AS p
  ON s.store_id = p.store_id
  AND s.item_id = p.item_id
  AND s.wm_yr_wk = p.wm_yr_wk;