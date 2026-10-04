
USE olist_analytics;

-- Business Question 3:
-- Which product categories generate the most sales?

SELECT
    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS product_category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(oi.price), 2) AS product_sales
FROM order_items AS oi
JOIN products AS p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation AS ct
    ON p.product_category_name = ct.product_category_name
GROUP BY
    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    )
ORDER BY product_sales DESC
LIMIT 10;
