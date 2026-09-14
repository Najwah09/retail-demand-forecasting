from pathlib import Path

PROJECT = "retail-demand-forecasting-2026"
DATASET = "retail_demand"

days = [f"d_{i}" for i in range(1, 1914)]

day_list = ", ".join(days)

sql = f"""CREATE OR REPLACE TABLE `{PROJECT}.{DATASET}.sales_daily_full` AS
SELECT
  id,
  item_id,
  dept_id,
  cat_id,
  store_id,
  state_id,
  d,
  sales
FROM `{PROJECT}.{DATASET}.sales_train_validation`
UNPIVOT(
  sales FOR d IN ({day_list})
);
"""

output = Path("sql/create_sales_daily_full.sql")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(sql, encoding="utf-8")

print(f"Created: {output}")
print(f"Day columns: {len(days)}")
print(f"SQL size: {output.stat().st_size:,} bytes")