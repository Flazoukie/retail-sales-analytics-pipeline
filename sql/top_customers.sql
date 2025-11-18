SELECT
    customer_id,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_order_value
FROM retail_curated_db.online_retail_curated
WHERE customer_id <> 'UNKNOWN'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
