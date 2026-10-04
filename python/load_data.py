
from pathlib import Path
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load database credentials
load_dotenv(project_folder / ".env")

# Create MySQL connection
connection_url = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(connection_url)

# CSV filename -> MySQL table name
files = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_customers_dataset.csv": "customers",
    "olist_sellers_dataset.csv": "sellers",
    "olist_products_dataset.csv": "products",
    "product_category_name_translation.csv": "category_translation",
}

try:
    for filename, table_name in files.items():
        file_path = data_folder / filename

        print(f"\nLoading {filename} into {table_name}...")

        first_chunk = True
        total_rows = 0

        # Read in smaller batches to limit memory use
        for chunk in pd.read_csv(file_path, chunksize=20000):
            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace" if first_chunk else "append",
                index=False,
                method="multi",
                chunksize=1000,
            )

            total_rows += len(chunk)
            first_chunk = False

        print(f"Loaded {total_rows:,} rows.")

    print("\nVerifying imported tables...")

    with engine.connect() as connection:
        for table_name in files.values():
            result = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table_name}`")
            )
            print(f"{table_name}: {result.scalar():,} rows")

    print("\nData import completed successfully!")

except Exception as error:
    print("\nImport failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))

finally:
    engine.dispose()
