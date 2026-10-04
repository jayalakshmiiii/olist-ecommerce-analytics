
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

# Load database credentials
load_dotenv()

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "olist_analytics"),
    port=int(os.getenv("DB_PORT", "3306")),
)

engine = create_engine(connection_url)

query = """
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%%Y-%%m'
    ) AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS product_sales,
    ROUND(SUM(oi.freight_value), 2) AS freight_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY DATE_FORMAT(
    o.order_purchase_timestamp,
    '%%Y-%%m'
)
ORDER BY sales_month;
"""

df = pd.read_sql(query, engine)

# Create the Power BI output folder
project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / "powerbi"
output_dir.mkdir(parents=True, exist_ok=True)

# Export monthly sales data
output_file = output_dir / "monthly_sales.csv"
df.to_csv(output_file, index=False)

print("MONTHLY SALES EXPORT")
print("====================")
print(f"Months exported: {len(df)}")
print(f"Total orders across monthly groups: {df['total_orders'].sum():,}")
print(f"Total product sales: R${df['product_sales'].sum():,.2f}")
print(f"Total freight revenue: R${df['freight_revenue'].sum():,.2f}")
print(f"\nSaved to: {output_file}")

engine.dispose()
