
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from scipy.stats import mannwhitneyu

# Load database credentials from .env
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
WITH delivered_orders AS (
    SELECT
        order_id,
        STR_TO_DATE(
            order_delivered_customer_date,
            '%%Y-%%m-%%d %%H:%%i:%%s'
        ) AS delivered_date,
        STR_TO_DATE(
            order_estimated_delivery_date,
            '%%Y-%%m-%%d %%H:%%i:%%s'
        ) AS estimated_date
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
),
reviews_by_order AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM order_reviews
    GROUP BY order_id
)
SELECT
    CASE
        WHEN d.delivered_date > d.estimated_date THEN 'Late'
        ELSE 'On time or early'
    END AS delivery_status,
    r.review_score
FROM delivered_orders AS d
JOIN reviews_by_order AS r
    ON d.order_id = r.order_id;
"""

df = pd.read_sql(query, engine)

on_time_scores = df.loc[
    df["delivery_status"] == "On time or early", "review_score"
].dropna()

late_scores = df.loc[
    df["delivery_status"] == "Late", "review_score"
].dropna()

print("DELIVERY AND CUSTOMER REVIEW ANALYSIS")
print("-------------------------------------")
print(f"On-time/early orders: {len(on_time_scores):,}")
print(f"Late orders:          {len(late_scores):,}")
print(f"On-time average score: {on_time_scores.mean():.2f}")
print(f"Late average score:    {late_scores.mean():.2f}")

statistic, p_value = mannwhitneyu(
    on_time_scores,
    late_scores,
    alternative="two-sided"
)

print("\nMANN-WHITNEY U TEST")
print("-------------------")
print(f"U statistic: {statistic:.2f}")
print(f"P-value:     {p_value:.3e}")

if p_value < 0.05:
    print(
        "Conclusion: The review-score distributions differ "
        "statistically significantly between the two groups."
    )
else:
    print(
        "Conclusion: There is insufficient evidence of a "
        "statistically significant difference between the groups."
    )

engine.dispose()
