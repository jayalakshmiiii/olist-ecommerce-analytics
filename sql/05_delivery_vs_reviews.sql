
USE olist_analytics;

WITH delivered_orders AS (
    SELECT
        order_id,
        STR_TO_DATE(
            order_delivered_customer_date,
            '%Y-%m-%d %H:%i:%s'
        ) AS delivered_date,
        STR_TO_DATE(
            order_estimated_delivery_date,
            '%Y-%m-%d %H:%i:%s'
        ) AS estimated_date
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
),
reviews_by_order AS (
    SELECT
        order_id,
        AVG(review_score) AS average_review_score
    FROM order_reviews
    GROUP BY order_id
)
SELECT
    CASE
        WHEN d.delivered_date > d.estimated_date THEN 'Late'
        ELSE 'On time or early'
    END AS delivery_status,
    COUNT(*) AS orders_with_reviews,
    ROUND(AVG(r.average_review_score), 2) AS average_review_score
FROM delivered_orders AS d
JOIN reviews_by_order AS r
    ON d.order_id = r.order_id
GROUP BY
    CASE
        WHEN d.delivered_date > d.estimated_date THEN 'Late'
        ELSE 'On time or early'
    END
ORDER BY average_review_score DESC;
