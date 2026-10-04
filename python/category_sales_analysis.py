
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
    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS product_category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(oi.price), 2) AS product_sales,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM order_items AS oi
JOIN products AS p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation AS ct
    ON p.product_category_name = ct.product_category_name
GROUP BY
    COALESCE(ct.product_category_name_english, 'Unknown')
ORDER BY product_sales DESC;
"""

df = pd.read_sql(query, engine)

# Display the top 10 categories
top_categories = df.head(10)

print("TOP 10 PRODUCT CATEGORIES")
print("=========================")
print(top_categories.to_string(index=False))

# Save the full category analysis for Power BI
project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / "powerbi"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "category_sales.csv"
df.to_csv(output_file, index=False)

print(f"\nTotal categories analysed: {len(df)}")
print(f"Full category results saved to: {output_file}")

engine.dispose()
