
USE olist_analytics;

WITH delivered_orders AS (
    SELECT
        order_id,
        STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s') AS purchase_date,
        STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s') AS delivered_date,
        STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s') AS estimated_date
    FROM orders
    WHERE order_status = 'delivered'
      AND order_purchase_timestamp IS NOT NULL
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
)
SELECT
    COUNT(*) AS delivered_orders,
    ROUND(
        AVG(TIMESTAMPDIFF(DAY, purchase_date, delivered_date)),
        2
    ) AS average_delivery_days,
    SUM(
        CASE
            WHEN delivered_date > estimated_date THEN 1
            ELSE 0
        END
    ) AS late_orders,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN delivered_date > estimated_date THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage,
    SUM(
        CASE
            WHEN delivered_date <= estimated_date THEN 1
            ELSE 0
        END
    ) AS on_time_or_early_orders
FROM delivered_orders;
