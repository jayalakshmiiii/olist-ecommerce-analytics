
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

orders = pd.read_csv(data_folder / "olist_orders_dataset.csv")

print("ORDER STATUS VS MISSING DELIVERY DATE")
print("-" * 55)

orders["delivery_date_missing"] = (
    orders["order_delivered_customer_date"].isnull()
)

summary = (
    orders.groupby("order_status")
    .agg(
        total_orders=("order_id", "count"),
        missing_delivery_dates=("delivery_date_missing", "sum")
    )
)

summary["missing_percentage"] = (
    summary["missing_delivery_dates"]
    / summary["total_orders"] * 100
).round(2)

print(summary.to_string())

print("\nDELIVERED ORDERS WITH MISSING DELIVERY DATES")

problem_orders = orders[
    (orders["order_status"] == "delivered")
    & (orders["delivery_date_missing"])
]

print("Count:", len(problem_orders))

print("\nInvestigation completed.")
