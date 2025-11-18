SELECT 
    description,
    SUM(revenue) AS total_sales
FROM retail_curated_db.online_retail_curated
GROUP BY description
ORDER BY total_sales DESC
LIMIT 10;
