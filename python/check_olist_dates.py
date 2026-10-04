
from sqlalchemy import text
from test_connection import engine

query = """
SELECT
    order_purchase_timestamp,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    STR_TO_DATE(
        order_purchase_timestamp,
        '%%Y-%%m-%%d %%H:%%i:%%s'
    ) AS parsed_purchase_date,
    STR_TO_DATE(
        order_delivered_customer_date,
        '%%Y-%%m-%%d %%H:%%i:%%s'
    ) AS parsed_delivery_date
FROM orders
WHERE order_status = 'delivered'
LIMIT 5
"""

try:
    with engine.connect() as connection:
        rows = connection.execute(text(query)).fetchall()

        for row in rows:
            print(row)

finally:
    engine.dispose()
