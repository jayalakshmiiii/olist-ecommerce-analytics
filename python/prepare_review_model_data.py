
import pandas as pd
from sqlalchemy import text
from test_connection import engine

query = """
SELECT
    o.order_id,
    AVG(r.review_score) AS review_score,

    TIMESTAMPDIFF(
        HOUR,
        CAST(o.order_purchase_timestamp AS DATETIME),
        CAST(o.order_delivered_customer_date AS DATETIME)
    ) / 24.0 AS delivery_duration_days,

    GREATEST(
        TIMESTAMPDIFF(
            HOUR,
            CAST(o.order_estimated_delivery_date AS DATETIME),
            CAST(o.order_delivered_customer_date AS DATETIME)
        ) / 24.0,
        0
    ) AS delay_days,

    i.total_price,
    i.total_freight,
    p.payment_type

FROM orders o

JOIN (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM order_reviews
    GROUP BY order_id
) r ON o.order_id = r.order_id

JOIN (
    SELECT
        order_id,
        SUM(price) AS total_price,
        SUM(freight_value) AS total_freight
    FROM order_items
    GROUP BY order_id
) i ON o.order_id = i.order_id

JOIN (
    SELECT
        order_id,
        GROUP_CONCAT(
            DISTINCT payment_type
            ORDER BY payment_type
            SEPARATOR ', '
        ) AS payment_type
    FROM order_payments
    GROUP BY order_id
) p ON o.order_id = p.order_id

WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL

GROUP BY
    o.order_id,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    i.total_price,
    i.total_freight,
    p.payment_type
"""

try:
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)

    # Define the prediction target: 1–2 star reviews
    df["low_review"] = (df["review_score"] <= 2).astype(int)

    print("Dataset prepared successfully!")
    print("Number of orders:", len(df))

    print("\nLow-review distribution:")
    print(df["low_review"].value_counts())

    print("\nLow-review percentages:")
    print(
        (df["low_review"].value_counts(normalize=True) * 100)
        .round(2)
    )

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nSample records:")
    print(df.head())

    # Save locally; do not upload this generated data file to GitHub
    df.to_csv(
        "powerbi/review_prediction_data.csv",
        index=False
    )

    print("\nSaved to powerbi/review_prediction_data.csv")

except Exception as error:
    print("Data preparation failed:")
    print(error)

finally:
    engine.dispose()
