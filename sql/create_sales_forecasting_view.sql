CREATE OR REPLACE VIEW `retail-demand-forecasting-2026.retail_demand.sales_forecasting` AS
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
  s.sales,
  p.sell_price,
  CASE
    WHEN p.sell_price IS NULL THEN FALSE
    ELSE TRUE
  END AS has_price
FROM `retail-demand-forecasting-2026.retail_demand.sales_daily_full` AS s
LEFT JOIN `retail-demand-forecasting-2026.retail_demand.calendar` AS c
  ON s.d = c.d
LEFT JOIN `retail-demand-forecasting-2026.retail_demand.sell_prices` AS p
  ON s.store_id = p.store_id
  AND s.item_id = p.item_id
  AND c.wm_yr_wk = p.wm_yr_wk;