CREATE OR REPLACE TABLE
`retail-demand-forecasting-2026.retail_demand.forecasting_train`
CLUSTER BY store_id, dept_id
AS
SELECT *
FROM
`retail-demand-forecasting-2026.retail_demand.forecasting_features`
WHERE date <= DATE '2016-01-31';

CREATE OR REPLACE TABLE
`retail-demand-forecasting-2026.retail_demand.forecasting_validation`
CLUSTER BY store_id, dept_id
AS
SELECT *
FROM
`retail-demand-forecasting-2026.retail_demand.forecasting_features`
WHERE date > DATE '2016-01-31';