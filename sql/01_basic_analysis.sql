
USE olist_analytics;

-- Business Question 1:
-- What are the total product sales and number of orders?

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_order_items,
    ROUND(SUM(price), 2) AS total_product_sales,
    ROUND(SUM(freight_value), 2) AS total_freight
FROM order_items;
