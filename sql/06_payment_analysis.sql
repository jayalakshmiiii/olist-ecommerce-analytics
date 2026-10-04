
USE olist_analytics;

SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS payment_records,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_value,
    ROUND(AVG(payment_installments), 2) AS average_installments
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;
