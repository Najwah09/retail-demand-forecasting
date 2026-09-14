-- Retail Demand Forecasting
-- M5 Dataset - Data Quality Checks
-- Project: retail-demand-forecasting-2026

-- ============================================================
-- 1. CALENDAR QUALITY CHECKS
-- ============================================================

-- Check row count and NULL values
SELECT
    COUNT(*) AS total_rows,
    COUNTIF(d IS NULL) AS null_day_ids,
    COUNTIF(wm_yr_wk IS NULL) AS null_week_keys
FROM `retail-demand-forecasting-2026.retail_demand.calendar`;


-- Check date range
SELECT
    MIN(date) AS min_date,
    MAX(date) AS max_date,
    COUNT(*) AS total_days
FROM `retail-demand-forecasting-2026.retail_demand.calendar`;


-- Check duplicate dates
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT date) AS unique_dates,
    COUNT(*) - COUNT(DISTINCT date) AS duplicate_dates
FROM `retail-demand-forecasting-2026.retail_demand.calendar`;


-- ============================================================
-- 2. SELL PRICES QUALITY CHECKS
-- ============================================================

-- Check NULL values
SELECT
    COUNT(*) AS total_rows,
    COUNTIF(store_id IS NULL) AS null_stores,
    COUNTIF(item_id IS NULL) AS null_items,
    COUNTIF(wm_yr_wk IS NULL) AS null_weeks,
    COUNTIF(sell_price IS NULL) AS null_prices
FROM `retail-demand-forecasting-2026.retail_demand.sell_prices`;


-- Check invalid prices
SELECT
    COUNT(*) AS invalid_prices
FROM `retail-demand-forecasting-2026.retail_demand.sell_prices`
WHERE sell_price <= 0;


-- ============================================================
-- 3. SALES TRAIN VALIDATION QUALITY CHECKS
-- ============================================================

-- Check NULL identifier values
SELECT
    COUNT(*) AS total_rows,
    COUNTIF(id IS NULL) AS null_ids,
    COUNTIF(item_id IS NULL) AS null_items,
    COUNTIF(dept_id IS NULL) AS null_departments,
    COUNTIF(store_id IS NULL) AS null_stores,
    COUNTIF(state_id IS NULL) AS null_states
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_validation`;


-- Check duplicate IDs
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT id) AS unique_ids,
    COUNT(*) - COUNT(DISTINCT id) AS duplicate_rows
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_validation`;


-- Check negative sales in first 10 daily columns
SELECT
    COUNT(*) AS negative_sales_values
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_validation`,
UNNEST([
    d_1, d_2, d_3, d_4, d_5,
    d_6, d_7, d_8, d_9, d_10
]) AS sales
WHERE sales < 0;


-- ============================================================
-- 4. SALES TRAIN EVALUATION QUALITY CHECKS
-- ============================================================

-- Check NULL identifier values
SELECT
    COUNT(*) AS total_rows,
    COUNTIF(id IS NULL) AS null_ids,
    COUNTIF(item_id IS NULL) AS null_items,
    COUNTIF(dept_id IS NULL) AS null_departments,
    COUNTIF(store_id IS NULL) AS null_stores,
    COUNTIF(state_id IS NULL) AS null_states
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_evaluation`;


-- Check duplicate IDs
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT id) AS unique_ids,
    COUNT(*) - COUNT(DISTINCT id) AS duplicate_rows
FROM `retail-demand-forecasting-2026.retail_demand.sales_train_evaluation`;