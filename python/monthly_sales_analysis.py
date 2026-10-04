
import os

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

# Calculate month-over-month product sales growth
df["product_sales_growth_pct"] = (
    df["product_sales"].pct_change() * 100
).round(2)

print("MONTHLY SALES ANALYSIS")
print("======================")
print(df.to_string(index=False))

# Identify the month with the highest product sales
best_month = df.loc[df["product_sales"].idxmax()]

print("\nBEST SALES MONTH")
print("================")
print(f"Month: {best_month['sales_month']}")
print(f"Product sales: R${best_month['product_sales']:,.2f}")
print(f"Orders: {int(best_month['total_orders']):,}")

engine.dispose()
